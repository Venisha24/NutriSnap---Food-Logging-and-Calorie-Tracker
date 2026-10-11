"""Lookup table aligned with Indian Food Nutritional Values Dataset (2025).

Values are typical cooked servings (not always per 100g) so the UI can show a
realistic plate. Calories/macros scale linearly with the serving multiplier.
"""

from __future__ import annotations

FOODS: dict[str, dict] = {
    "adhirasam": {"display_name": "Adhirasam", "serving": "2 pieces (60g)", "grams": 60, "calories": 240, "protein": 3.0, "carbs": 38.0, "fat": 8.5, "fiber": 1.2, "category": "Dessert"},
    "aloo_gobi": {"display_name": "Aloo Gobi", "serving": "1 bowl (200g)", "grams": 200, "calories": 180, "protein": 4.0, "carbs": 25.0, "fat": 8.0, "fiber": 5.0, "category": "Main"},
    "aloo_matar": {"display_name": "Aloo Matar", "serving": "1 bowl (200g)", "grams": 200, "calories": 190, "protein": 6.0, "carbs": 26.0, "fat": 7.0, "fiber": 6.0, "category": "Main"},
    "aloo_methi": {"display_name": "Aloo Methi", "serving": "1 bowl (180g)", "grams": 180, "calories": 170, "protein": 4.5, "carbs": 22.0, "fat": 7.5, "fiber": 4.5, "category": "Main"},
    "aloo_shimla_mirch": {"display_name": "Aloo Shimla Mirch", "serving": "1 bowl (180g)", "grams": 180, "calories": 165, "protein": 3.5, "carbs": 23.0, "fat": 7.0, "fiber": 4.0, "category": "Main"},
    "aloo_tikki": {"display_name": "Aloo Tikki", "serving": "2 pieces (120g)", "grams": 120, "calories": 260, "protein": 4.0, "carbs": 32.0, "fat": 13.0, "fiber": 3.5, "category": "Snack"},
    "anarsa": {"display_name": "Anarsa", "serving": "2 pieces (50g)", "grams": 50, "calories": 210, "protein": 2.5, "carbs": 34.0, "fat": 7.0, "fiber": 1.0, "category": "Dessert"},
    "ariselu": {"display_name": "Ariselu", "serving": "2 pieces (60g)", "grams": 60, "calories": 250, "protein": 3.0, "carbs": 36.0, "fat": 10.0, "fiber": 1.2, "category": "Dessert"},
    "bandar_laddu": {"display_name": "Bandar Laddu", "serving": "1 piece (40g)", "grams": 40, "calories": 170, "protein": 3.0, "carbs": 24.0, "fat": 7.0, "fiber": 0.8, "category": "Dessert"},
    "basundi": {"display_name": "Basundi", "serving": "1 bowl (150g)", "grams": 150, "calories": 280, "protein": 8.0, "carbs": 32.0, "fat": 13.0, "fiber": 0.2, "category": "Dessert"},
    "bhatura": {"display_name": "Bhatura", "serving": "1 piece (90g)", "grams": 90, "calories": 300, "protein": 7.0, "carbs": 42.0, "fat": 12.0, "fiber": 2.0, "category": "Bread"},
    "bhindi_masala": {"display_name": "Bhindi Masala", "serving": "1 bowl (180g)", "grams": 180, "calories": 150, "protein": 4.0, "carbs": 14.0, "fat": 9.0, "fiber": 5.5, "category": "Main"},
    "biryani": {"display_name": "Biryani", "serving": "1 plate (250g)", "grams": 250, "calories": 400, "protein": 20.0, "carbs": 50.0, "fat": 15.0, "fiber": 3.0, "category": "Main"},
    "boondi": {"display_name": "Boondi", "serving": "1 bowl (40g)", "grams": 40, "calories": 180, "protein": 3.5, "carbs": 22.0, "fat": 9.0, "fiber": 1.5, "category": "Snack"},
    "butter_chicken": {"display_name": "Butter Chicken", "serving": "1 bowl (200g)", "grams": 200, "calories": 350, "protein": 20.0, "carbs": 10.0, "fat": 25.0, "fiber": 1.5, "category": "Main"},
    "chak_hao_kheer": {"display_name": "Chak Hao Kheer", "serving": "1 bowl (150g)", "grams": 150, "calories": 220, "protein": 5.0, "carbs": 38.0, "fat": 5.0, "fiber": 1.0, "category": "Dessert"},
    "cham_cham": {"display_name": "Cham Cham", "serving": "2 pieces (80g)", "grams": 80, "calories": 230, "protein": 6.0, "carbs": 34.0, "fat": 8.0, "fiber": 0.3, "category": "Dessert"},
    "chana_masala": {"display_name": "Chana Masala", "serving": "1 bowl (200g)", "grams": 200, "calories": 220, "protein": 8.0, "carbs": 30.0, "fat": 9.0, "fiber": 8.0, "category": "Main"},
    "chapati": {"display_name": "Chapati", "serving": "1 piece (40g)", "grams": 40, "calories": 120, "protein": 3.5, "carbs": 22.0, "fat": 1.5, "fiber": 3.0, "category": "Bread"},
    "chhena_kheeri": {"display_name": "Chhena Kheeri", "serving": "1 bowl (140g)", "grams": 140, "calories": 250, "protein": 7.0, "carbs": 30.0, "fat": 11.0, "fiber": 0.2, "category": "Dessert"},
    "chicken_razala": {"display_name": "Chicken Razala", "serving": "1 bowl (200g)", "grams": 200, "calories": 320, "protein": 24.0, "carbs": 8.0, "fat": 20.0, "fiber": 1.0, "category": "Main"},
    "chicken_tikka": {"display_name": "Chicken Tikka", "serving": "4 pieces (120g)", "grams": 120, "calories": 220, "protein": 25.0, "carbs": 5.0, "fat": 12.0, "fiber": 0.5, "category": "Main"},
    "chicken_tikka_masala": {"display_name": "Chicken Tikka Masala", "serving": "1 bowl (200g)", "grams": 200, "calories": 340, "protein": 22.0, "carbs": 12.0, "fat": 22.0, "fiber": 2.0, "category": "Main"},
    "chikki": {"display_name": "Chikki", "serving": "1 bar (30g)", "grams": 30, "calories": 140, "protein": 3.5, "carbs": 18.0, "fat": 6.5, "fiber": 1.5, "category": "Snack"},
    "daal_baati_churma": {"display_name": "Dal Baati Churma", "serving": "1 plate (250g)", "grams": 250, "calories": 480, "protein": 14.0, "carbs": 58.0, "fat": 20.0, "fiber": 8.0, "category": "Main"},
    "daal_puri": {"display_name": "Dal Puri", "serving": "2 pieces (120g)", "grams": 120, "calories": 310, "protein": 8.0, "carbs": 40.0, "fat": 13.0, "fiber": 4.0, "category": "Bread"},
    "dal_makhani": {"display_name": "Dal Makhani", "serving": "1 bowl (200g)", "grams": 200, "calories": 240, "protein": 12.0, "carbs": 22.0, "fat": 12.0, "fiber": 8.0, "category": "Main"},
    "dal_tadka": {"display_name": "Dal Tadka", "serving": "1 bowl (200g)", "grams": 200, "calories": 180, "protein": 9.0, "carbs": 20.0, "fat": 8.0, "fiber": 6.0, "category": "Main"},
    "dharwad_pedha": {"display_name": "Dharwad Pedha", "serving": "2 pieces (50g)", "grams": 50, "calories": 200, "protein": 5.0, "carbs": 26.0, "fat": 8.0, "fiber": 0.2, "category": "Dessert"},
    "doodhpak": {"display_name": "Doodhpak", "serving": "1 bowl (150g)", "grams": 150, "calories": 230, "protein": 7.0, "carbs": 32.0, "fat": 8.0, "fiber": 0.3, "category": "Dessert"},
    "double_ka_meetha": {"display_name": "Double Ka Meetha", "serving": "1 bowl (140g)", "grams": 140, "calories": 310, "protein": 6.0, "carbs": 42.0, "fat": 13.0, "fiber": 1.0, "category": "Dessert"},
    "dum_aloo": {"display_name": "Dum Aloo", "serving": "1 bowl (200g)", "grams": 200, "calories": 230, "protein": 4.0, "carbs": 26.0, "fat": 12.0, "fiber": 4.0, "category": "Main"},
    "gajar_ka_halwa": {"display_name": "Gajar Ka Halwa", "serving": "1 bowl (120g)", "grams": 120, "calories": 280, "protein": 5.0, "carbs": 36.0, "fat": 13.0, "fiber": 3.0, "category": "Dessert"},
    "gavvalu": {"display_name": "Gavvalu", "serving": "1 handful (40g)", "grams": 40, "calories": 180, "protein": 2.5, "carbs": 26.0, "fat": 7.5, "fiber": 1.0, "category": "Snack"},
    "ghevar": {"display_name": "Ghevar", "serving": "1 piece (80g)", "grams": 80, "calories": 320, "protein": 5.0, "carbs": 40.0, "fat": 16.0, "fiber": 0.8, "category": "Dessert"},
    "gulab_jamun": {"display_name": "Gulab Jamun", "serving": "2 pieces (80g)", "grams": 80, "calories": 280, "protein": 5.0, "carbs": 42.0, "fat": 10.0, "fiber": 0.5, "category": "Dessert"},
    "imarti": {"display_name": "Imarti", "serving": "2 pieces (70g)", "grams": 70, "calories": 260, "protein": 4.0, "carbs": 40.0, "fat": 9.0, "fiber": 1.5, "category": "Dessert"},
    "jalebi": {"display_name": "Jalebi", "serving": "3 pieces (75g)", "grams": 75, "calories": 300, "protein": 3.0, "carbs": 48.0, "fat": 11.0, "fiber": 0.5, "category": "Dessert"},
    "kachori": {"display_name": "Kachori", "serving": "2 pieces (100g)", "grams": 100, "calories": 290, "protein": 6.0, "carbs": 32.0, "fat": 16.0, "fiber": 3.0, "category": "Snack"},
    "kadai_paneer": {"display_name": "Kadai Paneer", "serving": "1 bowl (200g)", "grams": 200, "calories": 320, "protein": 14.0, "carbs": 14.0, "fat": 22.0, "fiber": 3.0, "category": "Main"},
    "kadhi_pakoda": {"display_name": "Kadhi Pakoda", "serving": "1 bowl (220g)", "grams": 220, "calories": 240, "protein": 8.0, "carbs": 20.0, "fat": 14.0, "fiber": 3.0, "category": "Main"},
    "kajjikaya": {"display_name": "Kajjikaya", "serving": "2 pieces (60g)", "grams": 60, "calories": 230, "protein": 4.0, "carbs": 30.0, "fat": 10.0, "fiber": 1.5, "category": "Dessert"},
    "kakinada_khaja": {"display_name": "Kakinada Khaja", "serving": "2 pieces (50g)", "grams": 50, "calories": 220, "protein": 3.0, "carbs": 32.0, "fat": 9.0, "fiber": 0.8, "category": "Dessert"},
    "kalakand": {"display_name": "Kalakand", "serving": "2 pieces (60g)", "grams": 60, "calories": 210, "protein": 8.0, "carbs": 24.0, "fat": 9.0, "fiber": 0.2, "category": "Dessert"},
    "karela_bharta": {"display_name": "Karela Bharta", "serving": "1 bowl (160g)", "grams": 160, "calories": 110, "protein": 3.0, "carbs": 12.0, "fat": 6.0, "fiber": 4.5, "category": "Main"},
    "kofta": {"display_name": "Kofta", "serving": "1 bowl (200g)", "grams": 200, "calories": 310, "protein": 10.0, "carbs": 18.0, "fat": 22.0, "fiber": 3.5, "category": "Main"},
    "kuzhi_paniyaram": {"display_name": "Kuzhi Paniyaram", "serving": "5 pieces (100g)", "grams": 100, "calories": 190, "protein": 5.0, "carbs": 28.0, "fat": 6.0, "fiber": 3.0, "category": "Snack"},
    "lassi": {"display_name": "Lassi", "serving": "1 glass (250ml)", "grams": 250, "calories": 180, "protein": 6.0, "carbs": 24.0, "fat": 6.0, "fiber": 0.0, "category": "Drink"},
    "ledikeni": {"display_name": "Ledikeni", "serving": "2 pieces (70g)", "grams": 70, "calories": 240, "protein": 5.0, "carbs": 36.0, "fat": 8.0, "fiber": 0.4, "category": "Dessert"},
    "litti_chokha": {"display_name": "Litti Chokha", "serving": "1 plate (220g)", "grams": 220, "calories": 350, "protein": 10.0, "carbs": 48.0, "fat": 13.0, "fiber": 7.0, "category": "Main"},
    "lyangcha": {"display_name": "Lyangcha", "serving": "2 pieces (70g)", "grams": 70, "calories": 250, "protein": 5.0, "carbs": 38.0, "fat": 8.5, "fiber": 0.4, "category": "Dessert"},
    "maach_jhol": {"display_name": "Maach Jhol", "serving": "1 bowl (200g)", "grams": 200, "calories": 220, "protein": 18.0, "carbs": 8.0, "fat": 12.0, "fiber": 1.5, "category": "Main"},
    "makki_di_roti_sarson_da_saag": {"display_name": "Makki Di Roti & Sarson Da Saag", "serving": "1 plate (250g)", "grams": 250, "calories": 330, "protein": 9.0, "carbs": 38.0, "fat": 16.0, "fiber": 8.0, "category": "Main"},
    "malapua": {"display_name": "Malapua", "serving": "2 pieces (90g)", "grams": 90, "calories": 310, "protein": 5.0, "carbs": 42.0, "fat": 13.0, "fiber": 1.0, "category": "Dessert"},
    "misi_roti": {"display_name": "Misi Roti", "serving": "1 piece (50g)", "grams": 50, "calories": 140, "protein": 5.0, "carbs": 22.0, "fat": 3.5, "fiber": 4.0, "category": "Bread"},
    "misti_doi": {"display_name": "Misti Doi", "serving": "1 bowl (120g)", "grams": 120, "calories": 160, "protein": 6.0, "carbs": 22.0, "fat": 5.0, "fiber": 0.0, "category": "Dessert"},
    "modak": {"display_name": "Modak", "serving": "2 pieces (60g)", "grams": 60, "calories": 200, "protein": 3.5, "carbs": 32.0, "fat": 7.0, "fiber": 1.5, "category": "Dessert"},
    "mysore_pak": {"display_name": "Mysore Pak", "serving": "2 pieces (50g)", "grams": 50, "calories": 250, "protein": 4.0, "carbs": 28.0, "fat": 14.0, "fiber": 1.0, "category": "Dessert"},
    "naan": {"display_name": "Naan", "serving": "1 piece (100g)", "grams": 100, "calories": 300, "protein": 7.0, "carbs": 50.0, "fat": 8.0, "fiber": 2.0, "category": "Bread"},
    "navrattan_korma": {"display_name": "Navrattan Korma", "serving": "1 bowl (200g)", "grams": 200, "calories": 280, "protein": 8.0, "carbs": 22.0, "fat": 18.0, "fiber": 4.0, "category": "Main"},
    "palak_paneer": {"display_name": "Palak Paneer", "serving": "1 bowl (200g)", "grams": 200, "calories": 250, "protein": 10.0, "carbs": 15.0, "fat": 18.0, "fiber": 4.0, "category": "Main"},
    "paneer_butter_masala": {"display_name": "Paneer Butter Masala", "serving": "1 bowl (200g)", "grams": 200, "calories": 300, "protein": 12.0, "carbs": 15.0, "fat": 22.0, "fiber": 2.5, "category": "Main"},
    "phirni": {"display_name": "Phirni", "serving": "1 bowl (130g)", "grams": 130, "calories": 210, "protein": 5.0, "carbs": 32.0, "fat": 7.0, "fiber": 0.4, "category": "Dessert"},
    "pithe": {"display_name": "Pithe", "serving": "2 pieces (70g)", "grams": 70, "calories": 200, "protein": 4.0, "carbs": 32.0, "fat": 6.0, "fiber": 1.5, "category": "Dessert"},
    "poha": {"display_name": "Poha", "serving": "1 plate (150g)", "grams": 150, "calories": 180, "protein": 4.0, "carbs": 30.0, "fat": 5.0, "fiber": 2.5, "category": "Breakfast"},
    "poornalu": {"display_name": "Poornalu", "serving": "2 pieces (70g)", "grams": 70, "calories": 240, "protein": 5.0, "carbs": 34.0, "fat": 9.0, "fiber": 2.0, "category": "Dessert"},
    "pootharekulu": {"display_name": "Pootharekulu", "serving": "2 sheets (40g)", "grams": 40, "calories": 160, "protein": 3.0, "carbs": 26.0, "fat": 5.0, "fiber": 0.5, "category": "Dessert"},
    "qubani_ka_meetha": {"display_name": "Qubani Ka Meetha", "serving": "1 bowl (120g)", "grams": 120, "calories": 200, "protein": 2.0, "carbs": 42.0, "fat": 3.5, "fiber": 3.0, "category": "Dessert"},
    "rabri": {"display_name": "Rabri", "serving": "1 bowl (120g)", "grams": 120, "calories": 260, "protein": 8.0, "carbs": 28.0, "fat": 13.0, "fiber": 0.1, "category": "Dessert"},
    "ras_malai": {"display_name": "Ras Malai", "serving": "2 pieces (120g)", "grams": 120, "calories": 250, "protein": 9.0, "carbs": 28.0, "fat": 11.0, "fiber": 0.2, "category": "Dessert"},
    "rasgulla": {"display_name": "Rasgulla", "serving": "2 pieces (80g)", "grams": 80, "calories": 180, "protein": 4.0, "carbs": 36.0, "fat": 2.0, "fiber": 0.1, "category": "Dessert"},
    "sandesh": {"display_name": "Sandesh", "serving": "2 pieces (50g)", "grams": 50, "calories": 150, "protein": 6.0, "carbs": 18.0, "fat": 6.0, "fiber": 0.2, "category": "Dessert"},
    "shankarpali": {"display_name": "Shankarpali", "serving": "1 handful (40g)", "grams": 40, "calories": 180, "protein": 3.0, "carbs": 24.0, "fat": 8.0, "fiber": 1.0, "category": "Snack"},
    "sheer_korma": {"display_name": "Sheer Korma", "serving": "1 bowl (150g)", "grams": 150, "calories": 270, "protein": 7.0, "carbs": 36.0, "fat": 11.0, "fiber": 1.5, "category": "Dessert"},
    "sheera": {"display_name": "Sheera", "serving": "1 bowl (130g)", "grams": 130, "calories": 290, "protein": 5.0, "carbs": 42.0, "fat": 11.0, "fiber": 1.5, "category": "Dessert"},
    "shrikhand": {"display_name": "Shrikhand", "serving": "1 bowl (120g)", "grams": 120, "calories": 220, "protein": 6.0, "carbs": 28.0, "fat": 9.0, "fiber": 0.2, "category": "Dessert"},
    "sohan_halwa": {"display_name": "Sohan Halwa", "serving": "1 piece (40g)", "grams": 40, "calories": 180, "protein": 2.5, "carbs": 28.0, "fat": 7.0, "fiber": 0.8, "category": "Dessert"},
    "sohan_papdi": {"display_name": "Sohan Papdi", "serving": "2 pieces (40g)", "grams": 40, "calories": 170, "protein": 3.0, "carbs": 24.0, "fat": 7.0, "fiber": 0.8, "category": "Dessert"},
    "sutar_feni": {"display_name": "Sutar Feni", "serving": "1 nest (40g)", "grams": 40, "calories": 190, "protein": 3.0, "carbs": 26.0, "fat": 8.0, "fiber": 0.6, "category": "Dessert"},
    "unni_appam": {"display_name": "Unni Appam", "serving": "4 pieces (80g)", "grams": 80, "calories": 240, "protein": 3.5, "carbs": 36.0, "fat": 9.0, "fiber": 2.0, "category": "Dessert"},
}


def lookup(class_name: str) -> dict:
    key = (class_name or "").strip().lower().replace(" ", "_")
    food = FOODS.get(key)
    if not food:
        food = {
            "display_name": class_name.replace("_", " ").title(),
            "serving": "1 serving (150g)",
            "grams": 150,
            "calories": 250,
            "protein": 8.0,
            "carbs": 30.0,
            "fat": 10.0,
            "fiber": 2.0,
            "category": "Main",
        }
    return {"class_name": key, **food}


def catalog() -> list[dict]:
    return [{"class_name": key, **value} for key, value in FOODS.items()]


def scale(food: dict, multiplier: float) -> dict:
    m = max(0.25, min(3.0, float(multiplier)))
    scaled = dict(food)
    for field in ("calories", "protein", "carbs", "fat", "fiber", "grams"):
        scaled[field] = round(float(food[field]) * m, 1)
    scaled["serving_multiplier"] = m
    return scaled
