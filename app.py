from flask import Flask, render_template, request
import json
import re

app = Flask(__name__)

with open("recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file) 

def clean_ingredient(text):
    """Убирает вес, количество и скобки для корректного сравнения"""
    return re.sub(r'\s*\(.*?\)', '', text).strip().lower() 

def is_match(user_ing, recipe_ing):
    """Гибкое сравнение: учитывает вложенность и основные слова"""
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
        user_input = request.form["ingredients"]
        mode = request.form["mode"] 

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

if __name__ == "__main__":
    app.run(debug=True)