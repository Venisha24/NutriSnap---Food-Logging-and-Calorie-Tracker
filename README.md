# NutriSnap – Food Logging and Calorie Tracker

College Deep Learning project: take a photo of food, classify it with a **Vision Transformer**, look up nutrition, and log the meal.

## What it does

1. Open **Snap Food** and upload or capture a plate photo.
2. Flask preprocesses the image (RGB, 224×224 via the ViT processor).
3. A **ViT-Base** model predicts one of **80 Indian food classes**.
4. Calories, protein, carbs, fat, and serving size come from an Indian food nutrition table.
5. You adjust the serving, pick Breakfast / Lunch / Dinner / Snack, and **Add to Log**.
6. SQLite stores the meal and the dashboard updates.

OpenRouter is the **only** external API. It writes a short nutrition note and, if the ViT is unsure, can confirm the dish from the photo.

## Deep Learning model

| Item | Detail |
| --- | --- |
| Architecture | Vision Transformer (`ViTForImageClassification`, patch size 16, 224px) |
| Task | Image classification, 80 classes |
| Image dataset | [Indian Food Images Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/indian-food-images-dataset) (4,000 images) |
| Nutrition dataset | [Indian Food Nutritional Values Dataset (2025)](https://www.kaggle.com/datasets/batthulavinay/indian-food-nutrition) |
| Default weights | Fine-tuned ViT on that image dataset (`dima806/indian_food_image_detection`) |
| Your own training | `python ml/train.py` saves `models/nutrisnap_vit/` |

The app **prefers your fine-tuned folder** if it exists. Otherwise it downloads the public ViT trained on the same Kaggle classes.

This is not a keyword search. The backend runs a real transformer on the pixels, then maps the predicted class to macros.

## Setup

```powershell
cd C:\Users\LENOVO\NutriSnap
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Put your OpenRouter key in `.env`:

```
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=google/gemini-2.0-flash-001
```

The app still classifies food **without** the key. The key is only for the AI note and low-confidence vision check.

Run:

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). The first start downloads ViT weights (a few hundred MB).

## Train on the Kaggle datasets (optional, recommended for the report)

KaggleHub will prompt for a Kaggle account the first time.

```powershell
python ml/train.py --epochs 3
python ml/train.py --epochs 5 --subset 16
```

`--subset 16` trains a smaller, usually more accurate set of popular classes. After training, restart `python app.py` so it loads `models/nutrisnap_vit`.

## Project layout

```
app.py                 Flask API + static frontend
frontend/              Snap Food UI, dashboard, How It Works
ml/classifier.py       ViT inference
ml/train.py            Fine-tune on the Kaggle image dataset
ml/nutrition.py        Macros for all 80 classes
ml/database.py         SQLite meal log
ml/openrouter_client.py
```

## Report talking points

- Transfer learning: ImageNet-21k ViT, then Indian food fine-tuning.
- Softmax confidence and top-4 alternatives in the UI.
- Serving-size scaling is linear on the nutrition table, not a second network.
- OpenRouter is coaching / fallback, not a replacement for the classifier.
