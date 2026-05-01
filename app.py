from flask import Flask, render_template, request, redirect, url_for
import json
import re
import os
from datetime import datetime

app = Flask(__name__)

RECIPES_FILE = "recipes.json"
REVIEWS_FILE = "reviews.json"

BANNED_WORDS = ["мат1", "мат2", "плохоеслово", "реклама"]

try:
    with open(RECIPES_FILE, "r", encoding="utf-8") as file:
        recipes = json.load(file)
except FileNotFoundError:
    recipes = []
    print(f"Внимание: Файл {RECIPES_FILE} не найден!")


def load_reviews():
    """Загружает отзывы из файла"""
    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_reviews(reviews):
    """Сохраняет отзывы в файл"""
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)


def clean_ingredient(text):
    """Очистка строки ингредиента от веса и скобок"""
    return re.sub(r'\s*\(.*?\)', '', text).strip().lower()

def is_match(user_ing, recipe_ing):
    """Сравнение ингредиента пользователя и рецепта"""
    u = clean_ingredient(user_ing)
    r = clean_ingredient(recipe_ing)
    if not u or not r:
        return False
    if u in r or r in u:
        return True
    if u.split()[0] == r.split()[0]:
        return True
    return False


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    user_input = ""
    mode = "flexible"

    if request.method == "POST":
        user_input = request.form.get("ingredients", "")
        mode = request.form.get("mode", "flexible")

        user_ingredients = [i.strip() for i in user_input.split(",") if i.strip()]

        for recipe in recipes:
            recipe_ings = recipe["ingredients"]
            matches = []
            missing = []

            for recipe_ing in recipe_ings:
                found = False
                for user_ing in user_ingredients:
                    if is_match(user_ing, recipe_ing):
                        found = True
                        break
                if found:
                    matches.append(recipe_ing)
                else:
                    missing.append(recipe_ing)

            if mode == "strict":
                if not missing:
                    results.append({
                        "name": recipe["name"],
                        "percent": 100,
                        "missing": [],
                        "instructions": recipe["instructions"]
                    })
            else:
                if matches:
                    percent = int(len(matches) / len(recipe_ings) * 100)
                    results.append({
                        "name": recipe["name"],
                        "percent": percent,
                        "missing": missing,
                        "instructions": recipe["instructions"]
                    })
        results.sort(key=lambda x: x["percent"], reverse=True)

    return render_template("index.html", results=results, user_input=user_input, mode=mode)

@app.route("/reviews", methods=["GET", "POST"])
def reviews_page():
    all_reviews = load_reviews()
    error = None

    if request.method == "POST":
        name = request.form.get("name", "Аноним").strip()
        text = request.form.get("text", "").strip()

        found_bad_words = [word for word in BANNED_WORDS if word.lower() in text.lower()]
        
        if found_bad_words:
            error = "Ошибка: Сообщение содержит недопустимые выражения."
        elif len(text) < 5:
            error = "Ошибка: Отзыв слишком короткий."
        else:

            new_review = {
                "name": name if name else "Аноним",
                "text": text,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M")
            }
            all_reviews.insert(0, new_review) 
            save_reviews(all_reviews)
          
            return redirect(url_for("reviews_page"))

    return render_template("reviews.html", reviews=all_reviews, error=error)

if __name__ == "__main__":
    app.run(debug=True)