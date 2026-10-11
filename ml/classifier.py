"""Vision Transformer food classifier.

The production model is a ViT-Base image classifier trained on the Kaggle
Indian Food Images Dataset (80 classes). A locally fine-tuned checkpoint
from `ml/train.py` is preferred when present.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

ROOT = Path(__file__).resolve().parent.parent
LOCAL_MODEL_DIR = ROOT / "models" / "nutrisnap_vit"
HUB_MODEL_ID = "dima806/indian_food_image_detection"
LABELS_PATH = Path(__file__).resolve().parent / "labels.json"

_processor = None
_model = None
_device = None
_source = None
_error = None
_lock = threading.Lock()


def _device_name() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def is_loaded() -> bool:
    return _model is not None


def last_error() -> str | None:
    return _error


def model_source() -> str:
    return _source or "not-loaded"


def load_model():
    global _processor, _model, _device, _source, _error
    if _model is not None:
        return _processor, _model
    with _lock:
        if _model is not None:
            return _processor, _model
        try:
            _device = _device_name()
            model_id = str(LOCAL_MODEL_DIR) if (LOCAL_MODEL_DIR / "config.json").exists() else HUB_MODEL_ID
            _source = "local-finetuned" if model_id == str(LOCAL_MODEL_DIR) else "huggingface-vit"
            _processor = AutoImageProcessor.from_pretrained(model_id)
            _model = AutoModelForImageClassification.from_pretrained(model_id)
            _model.to(_device)
            _model.eval()
            _error = None
        except Exception as exc:
            _error = str(exc)
            raise
    return _processor, _model


def class_names() -> list[str]:
    with LABELS_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["classes"]


def predict_image(image_path: str | Path, top_k: int = 4) -> dict:
    processor, model = load_model()
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    inputs = {key: value.to(_device) for key, value in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]

    k = min(top_k, probs.shape[0])
    scores, indices = torch.topk(probs, k)
    predictions = []
    for score, index in zip(scores.tolist(), indices.tolist()):
        label = model.config.id2label[int(index)]
        predictions.append({"class_name": label, "confidence": round(float(score), 4)})

    best = predictions[0]
    return {
        "food_class": best["class_name"],
        "confidence": best["confidence"],
        "top_predictions": predictions,
        "model": {
            "name": "NutriSnap-ViT",
            "architecture": "ViTForImageClassification",
            "source": model_source(),
            "device": str(_device),
            "num_classes": int(getattr(model.config, "num_labels", 80)),
        },
    }
