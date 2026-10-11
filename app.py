"""NutriSnap Flask backend + static frontend.

API:
  GET  /api/health
  GET  /api/ready
  GET  /api/model
  GET  /api/foods
  POST /api/analyze
  POST /api/log
  GET  /api/dashboard
  GET  /api/history
  DELETE /api/log/<id>
"""

from __future__ import annotations

import os
import sys
import threading
import traceback
import uuid
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from ml import database, nutrition, openrouter_client
from ml.classifier import (
    class_names,
    is_loaded,
    last_error,
    load_model,
    model_source,
    predict_image,
)

UPLOAD_DIR = ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}
CONFIDENCE_THRESHOLD = 0.45

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)
database.init_db()


def _openrouter_on() -> bool:
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    return bool(key) and not key.startswith("your_openrouter")


def _model_payload() -> dict:
    return {
        "name": "NutriSnap-ViT",
        "architecture": "Vision Transformer (ViT-Base, 16x16 patches, 224px)",
        "dataset": "Kaggle Indian Food Images Dataset — 80 classes",
        "nutrition_dataset": "Indian Food Nutritional Values Dataset (2025)",
        "loaded": is_loaded(),
        "source": model_source(),
        "error": last_error(),
        "classes": class_names(),
        "openrouter_enabled": _openrouter_on(),
    }


def _warmup() -> None:
    try:
        load_model()
        print(f"ViT ready ({model_source()}).")
    except Exception:
        traceback.print_exc()
        print("ViT failed to load. Check the terminal error and try again.")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "app": "NutriSnap", "backend": "flask", "frontend": "static-spa"})


@app.get("/api/ready")
def ready():
    return jsonify({"loaded": is_loaded(), "source": model_source(), "error": last_error()})


@app.get("/api/model")
def model_info():
    if not is_loaded():
        try:
            load_model()
        except Exception as exc:
            return jsonify({**_model_payload(), "error": str(exc)}), 503
    return jsonify(_model_payload())


@app.get("/api/foods")
def foods():
    return jsonify({"foods": nutrition.catalog(), "count": len(nutrition.FOODS)})


@app.post("/api/analyze")
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "Upload an image as form field 'image'."}), 400
    file = request.files["image"]
    if not file.filename:
        return jsonify({"error": "Empty filename."}), 400
    suffix = Path(secure_filename(file.filename)).suffix.lower()
    if suffix not in ALLOWED:
        return jsonify({"error": "Use a JPG, PNG, or WEBP image."}), 400

    saved = UPLOAD_DIR / f"{uuid.uuid4().hex}{suffix}"
    file.save(saved)

    try:
        prediction = predict_image(saved)
    except Exception as exc:
        traceback.print_exc()
        return jsonify({"error": f"Model inference failed: {exc}"}), 500

    food_class = prediction["food_class"]
    confidence = prediction["confidence"]
    used_vision_check = False

    if confidence < CONFIDENCE_THRESHOLD or _openrouter_on():
        confirmed = openrouter_client.vision_confirm(saved, class_names())
        if confirmed:
            food_class = confirmed["class_name"]
            confidence = max(confidence, confirmed["confidence"])
            used_vision_check = True
            prediction["food_class"] = food_class
            prediction["confidence"] = round(confidence, 4)

    food = nutrition.lookup(food_class)
    if used_vision_check and "calories" in confirmed:
        food = {
            "class_name": food_class,
            "display_name": confirmed.get("display_name", food["display_name"]),
            "serving": confirmed.get("serving", food["serving"]),
            "grams": 150,
            "calories": confirmed.get("calories", food["calories"]),
            "protein": confirmed.get("protein", food["protein"]),
            "carbs": confirmed.get("carbs", food["carbs"]),
            "fat": confirmed.get("fat", food["fat"]),
            "fiber": confirmed.get("fiber", food["fiber"]),
            "category": "Fruit / General",
        }

    out_of_vocabulary_warning = None
    if not _openrouter_on() and confidence < CONFIDENCE_THRESHOLD:
        out_of_vocabulary_warning = (
            "Note: The local ViT model is trained specifically on 80 prepared Indian dishes. "
            "Raw fruits, vegetables, or unlisted foods may be misclassified into the nearest Indian sweet/dish class (e.g., Gulab Jamun)."
        )

    insight = openrouter_client.nutrition_insight(food["display_name"], food, confidence)

    return jsonify(
        {
            "image_url": f"/uploads/{saved.name}",
            "image_path": saved.name,
            "prediction": prediction,
            "nutrition": food,
            "insight": insight,
            "vision_check": used_vision_check,
            "out_of_vocabulary_warning": out_of_vocabulary_warning,
        }
    )


@app.post("/api/log")
def log_meal():
    data = request.get_json(force=True, silent=True) or {}
    food_class = data.get("food_class")
    meal_type = data.get("meal_type")
    if not food_class or meal_type not in {"Breakfast", "Lunch", "Dinner", "Snack"}:
        return jsonify({"error": "food_class and meal_type (Breakfast/Lunch/Dinner/Snack) are required."}), 400

    multiplier = float(data.get("serving_multiplier") or 1)
    food = nutrition.scale(nutrition.lookup(food_class), multiplier)
    meal_id = database.add_meal(
        {
            "food_class": food_class,
            "food_name": food["display_name"],
            "meal_type": meal_type,
            "serving_label": food["serving"],
            "serving_multiplier": food["serving_multiplier"],
            "calories": food["calories"],
            "protein": food["protein"],
            "carbs": food["carbs"],
            "fat": food["fat"],
            "fiber": food["fiber"],
            "confidence": data.get("confidence"),
            "insight": data.get("insight"),
            "image_path": data.get("image_path"),
        }
    )
    return jsonify({"ok": True, "id": meal_id, "summary": database.daily_summary()})


@app.get("/api/dashboard")
def dashboard():
    day = request.args.get("date")
    payload = database.daily_summary(day)
    payload["week"] = database.week_history()
    payload["goal_calories"] = 2000
    return jsonify(payload)


@app.get("/api/history")
def history():
    return jsonify({"week": database.week_history()})


@app.delete("/api/log/<int:meal_id>")
def remove_meal(meal_id: int):
    if not database.delete_meal(meal_id):
        return jsonify({"error": "Meal not found."}), 404
    return jsonify({"ok": True, "summary": database.daily_summary()})


@app.get("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(UPLOAD_DIR, filename)


if __name__ == "__main__":
    print("Starting Flask frontend+backend on http://127.0.0.1:5000")
    print("Warming Vision Transformer in the background (first run downloads weights)...")
    threading.Thread(target=_warmup, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
