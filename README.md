# NutriSnap – Food Logging and Calorie Tracker

A Deep Learning project that identifies Indian food from an image, estimates its nutritional values, and helps users track their daily meals.

## What It Does

1. Upload or capture a food image using **Snap Food**.
2. Flask preprocesses the image into RGB format at 224 × 224 pixels.
3. A **Vision Transformer (ViT-Base)** predicts one of 80 Indian food classes.
4. Nutritional values—including calories, protein, carbohydrates, fat, and serving size—are retrieved from a nutrition dataset.
5. Adjust the serving size, select a meal category (Breakfast, Lunch, Dinner, or Snack), and add the meal to your log.
6. SQLite stores meal records and updates the dashboard.

OpenRouter provides an optional AI-generated nutrition note and a fallback dish verification feature when the image classifier has low confidence.

## Deep Learning Model

| Item | Details |
|---|---|
| Architecture | Vision Transformer (ViTForImageClassification), patch size 16, 224 × 224 input |
| Task | Image classification across 80 classes |
| Image dataset | [Indian Food Images Dataset – Kaggle](https://www.kaggle.com/datasets/iamsouravbanerjee/indian-food-images-dataset) |
| Nutrition dataset | [Indian Food Nutrition Dataset – Kaggle](https://www.kaggle.com/datasets/batthulavinay/indian-food-nutrition) |
| Pretrained weights | [dima806/indian_food_image_detection](https://huggingface.co/dima806/indian_food_image_detection) |
| Optional training | `python ml/train.py` |

The application prefers locally fine-tuned model weights when available. Otherwise, it attempts to load the configured pretrained model.

The classifier processes image pixels rather than relying on keyword search. Predicted food classes are mapped to nutritional information from the nutrition table.

## Setup

Open a terminal in the project directory and run:

```powershell
cd C:\Users\LENOVO\NutriSnap
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Add your OpenRouter credentials to `.env` if you want to use the optional AI features:

```text
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=google/gemini-2.0-flash-001
```

Food classification should work without an OpenRouter API key if the configured model and required dependencies are available.

Run the application:

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser.

The first launch may download model weights if they are not available locally.

## Optional Model Training

Training depends on the dataset setup and the arguments supported by `ml/train.py`.

```powershell
python ml/train.py --epochs 3
```

After training, restart the application if it is configured to load the newly saved model.

## Project Structure

```text
NutriSnap/
├── app.py
├── frontend/
├── ml/
│   ├── classifier.py
│   ├── train.py
│   ├── nutrition.py
│   ├── database.py
│   └── openrouter_client.py
├── models/
├── uploads/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Key Concepts

- Transfer learning using a Vision Transformer.
- Image preprocessing and food classification.
- Prediction confidence and alternative class predictions.
- Serving-size-based nutritional estimates.
- SQLite-based meal logging.
- Optional AI-generated nutrition notes and fallback verification.

## Disclaimer

Nutritional values are estimates based on the available dataset and selected serving size. Actual nutritional content can vary with ingredients, preparation methods, and portion sizes.
