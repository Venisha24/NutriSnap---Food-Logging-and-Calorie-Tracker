"""Fine-tune NutriSnap-ViT on the Kaggle Indian Food Images Dataset.

Downloads:
  https://www.kaggle.com/datasets/iamsouravbanerjee/indian-food-images-dataset

Optional nutrition CSV:
  https://www.kaggle.com/datasets/batthulavinay/indian-food-nutrition

Usage:
  python ml/train.py
  python ml/train.py --epochs 3 --subset 16
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LABELS_PATH = Path(__file__).resolve().parent / "labels.json"
OUTPUT_DIR = ROOT / "models" / "nutrisnap_vit"


def find_image_root(dataset_path: Path) -> Path:
    for candidate in dataset_path.rglob("*"):
        if candidate.is_dir() and any(p.is_dir() and any(p.glob("*.jpg")) for p in candidate.iterdir()):
            return candidate
    return dataset_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Train NutriSnap ViT on Indian food images")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--subset", type=int, default=0, help="Use only the first N classes (0 = all 80)")
    parser.add_argument("--model-id", default="google/vit-base-patch16-224-in21k")
    args = parser.parse_args()

    import kagglehub
    from datasets import Dataset, Image as HFImage
    from transformers import (
        AutoImageProcessor,
        AutoModelForImageClassification,
        Trainer,
        TrainingArguments,
    )
    import numpy as np

    print("Downloading Indian Food Images Dataset from Kaggle...")
    image_dataset_path = Path(kagglehub.dataset_download("iamsouravbanerjee/indian-food-images-dataset"))
    try:
        Path(kagglehub.dataset_download("batthulavinay/indian-food-nutrition"))
        print("Also downloaded Indian Food Nutritional Values Dataset (2025).")
    except Exception as exc:
        print(f"Nutrition dataset download skipped ({exc}). Bundled lookup table will be used.")

    image_root = find_image_root(image_dataset_path)
    print(f"Image root: {image_root}")

    with LABELS_PATH.open(encoding="utf-8") as handle:
        all_classes = json.load(handle)["classes"]
    class_names = all_classes[: args.subset] if args.subset else all_classes

    records = []
    for label_id, name in enumerate(class_names):
        folder = None
        for path in image_root.rglob("*"):
            if path.is_dir() and path.name.lower().replace(" ", "_") == name:
                folder = path
                break
        if not folder:
            print(f"Missing folder for class: {name}")
            continue
        for image_file in list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg")) + list(folder.glob("*.png")):
            records.append({"image": str(image_file), "label": label_id})

    if not records:
        raise SystemExit("No training images found. Check the Kaggle download path.")

    print(f"Collected {len(records)} images across {len(class_names)} classes.")
    dataset = Dataset.from_list(records).cast_column("image", HFImage())
    dataset = dataset.train_test_split(test_size=0.2, seed=42)

    processor = AutoImageProcessor.from_pretrained(args.model_id)

    def transform(batch):
        images = [image.convert("RGB") for image in batch["image"]]
        processed = processor(images, return_tensors="pt")
        processed["labels"] = batch["label"]
        return processed

    prepared = dataset.with_transform(transform)
    id2label = {i: name for i, name in enumerate(class_names)}
    label2id = {name: i for i, name in enumerate(class_names)}

    model = AutoModelForImageClassification.from_pretrained(
        args.model_id,
        num_labels=len(class_names),
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    training_args = TrainingArguments(
        output_dir=str(ROOT / "models" / "runs"),
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        logging_steps=20,
        remove_unused_columns=False,
        fp16=False,
        report_to=[],
    )

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        return {"accuracy": float((preds == labels).mean())}

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=prepared["train"],
        eval_dataset=prepared["test"],
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model(str(OUTPUT_DIR))
    processor.save_pretrained(str(OUTPUT_DIR))
    print(f"Saved fine-tuned model to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
