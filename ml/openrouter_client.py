"""OpenRouter is the only external API. Used for nutrition notes and optional
vision confirmation when the local ViT is uncertain.
"""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path

import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _headers() -> dict[str, str] | None:
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not key or key.startswith("your_openrouter"):
        return None
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "NutriSnap",
    }


def _model_name() -> str:
    return os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001").strip()


def _chat(messages: list[dict], max_tokens: int = 220) -> str | None:
    headers = _headers()
    if not headers:
        return None
    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json={"model": _model_name(), "messages": messages, "max_tokens": max_tokens, "temperature": 0.3},
        timeout=45,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def nutrition_insight(food_name: str, macros: dict, confidence: float) -> str | None:
    prompt = (
        f"You are a concise nutrition coach for Indian meals. "
        f"A Vision Transformer classified this photo as {food_name} "
        f"({round(confidence * 100)}% confidence). "
        f"Estimated serving macros: {macros['calories']} kcal, "
        f"{macros['protein']} g protein, {macros['carbs']} g carbs, {macros['fat']} g fat. "
        "Write exactly 2 short sentences: (1) the nutrition takeaway, "
        "(2) one practical portion or pairing tip. No markdown."
    )
    try:
        return _chat([{"role": "user", "content": prompt}], max_tokens=160)
    except Exception:
        return None


def vision_confirm(image_path: str | Path, candidate_classes: list[str]) -> dict | None:
    headers = _headers()
    if not headers:
        return None
    raw = Path(image_path).read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    suffix = Path(image_path).suffix.lower().replace(".", "") or "jpeg"
    if suffix == "jpg":
        suffix = "jpeg"
    
    prompt_text = (
        "Identify the food item in this photo with high accuracy. "
        "If it is an Indian prepared dish matching one of these categories: "
        f"[{', '.join(candidate_classes[:30])}...], use that exact snake_case name. "
        "If it is a fruit, vegetable, salad, or other general food item (e.g. apple, banana, fruit_salad, mango), "
        "identify it correctly. "
        "Reply ONLY with a JSON object: "
        '{"class_name":"...","display_name":"...","confidence":0.92,"calories":120,"protein":1.5,"carbs":25.0,"fat":0.3,"fiber":3.0,"serving":"1 medium fruit (150g)"}'
    )

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_text},
                {"type": "image_url", "image_url": {"url": f"data:image/{suffix};base64,{b64}"}},
            ],
        }
    ]
    try:
        text = _chat(messages, max_tokens=150) or ""
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end == -1:
            return None
        parsed = json.loads(text[start : end + 1])
        name = str(parsed.get("class_name", "")).strip().lower().replace(" ", "_")
        disp_name = str(parsed.get("display_name", name.replace("_", " ").title()))
        conf = float(parsed.get("confidence", 0.85))
        
        return {
            "class_name": name,
            "display_name": disp_name,
            "confidence": max(0.0, min(1.0, conf)),
            "calories": float(parsed.get("calories", 100)),
            "protein": float(parsed.get("protein", 2.0)),
            "carbs": float(parsed.get("carbs", 20.0)),
            "fat": float(parsed.get("fat", 1.0)),
            "fiber": float(parsed.get("fiber", 2.0)),
            "serving": str(parsed.get("serving", "1 serving (150g)")),
        }
    except Exception as exc:
        print("Vision confirm error:", exc)
        return None

