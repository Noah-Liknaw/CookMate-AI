import os

def load_recipes(file_path=None):
    # Always resolve relative to this file's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if file_path is None:
        file_path = os.path.join(base_dir, "data", "recipes.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    recipes = content.split("\n\n")
    return [r.strip() for r in recipes if r.strip()]
