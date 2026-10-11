from __future__ import annotations

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "instance" / "nutrisnap.db"


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_class TEXT NOT NULL,
                food_name TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                serving_label TEXT,
                serving_multiplier REAL NOT NULL DEFAULT 1.0,
                calories REAL NOT NULL,
                protein REAL NOT NULL,
                carbs REAL NOT NULL,
                fat REAL NOT NULL,
                fiber REAL,
                confidence REAL,
                insight TEXT,
                image_path TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def add_meal(payload: dict) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO meals (
                food_class, food_name, meal_type, serving_label, serving_multiplier,
                calories, protein, carbs, fat, fiber, confidence, insight, image_path, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["food_class"],
                payload["food_name"],
                payload["meal_type"],
                payload.get("serving_label"),
                payload.get("serving_multiplier", 1.0),
                payload["calories"],
                payload["protein"],
                payload["carbs"],
                payload["fat"],
                payload.get("fiber"),
                payload.get("confidence"),
                payload.get("insight"),
                payload.get("image_path"),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        return int(cur.lastrowid)


def list_meals(day: str | None = None) -> list[dict]:
    query = "SELECT * FROM meals"
    args: tuple = ()
    if day:
        query += " WHERE date(created_at) = ?"
        args = (day,)
    query += " ORDER BY created_at DESC"
    with get_conn() as conn:
        rows = conn.execute(query, args).fetchall()
    return [dict(row) for row in rows]


def daily_summary(day: str | None = None) -> dict:
    day = day or date.today().isoformat()
    meals = list_meals(day)
    totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0, "fiber": 0.0, "count": len(meals)}
    by_type: dict[str, float] = {}
    for meal in meals:
        for key in ("calories", "protein", "carbs", "fat", "fiber"):
            totals[key] += float(meal.get(key) or 0)
        meal_type = meal["meal_type"]
        by_type[meal_type] = by_type.get(meal_type, 0) + float(meal["calories"])
    return {"date": day, "totals": totals, "by_meal_type": by_type, "meals": meals}


def week_history() -> list[dict]:
    days = []
    today = date.today()
    for offset in range(6, -1, -1):
        day = (today - timedelta(days=offset)).isoformat()
        summary = daily_summary(day)
        days.append(
            {
                "date": day,
                "label": (today - timedelta(days=offset)).strftime("%a"),
                "calories": round(summary["totals"]["calories"], 1),
                "count": summary["totals"]["count"],
            }
        )
    return days


def delete_meal(meal_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
        return cur.rowcount > 0
