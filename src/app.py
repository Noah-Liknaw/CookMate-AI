import streamlit as st
from rag_recipe_name import get_recipe_name
from load_recipes import load_recipes

# Load recipes into memory
recipes_list = load_recipes("data/recipes.txt")
recipe_dict = {r.split("\n")[0].replace("Recipe: ", ""): r for r in recipes_list}

# Streamlit page config
st.set_page_config(page_title="🍳 Recipe RAG Assistant", page_icon="🍽️", layout="wide")

# CSS Styling
st.markdown(
    """
    <style>

    .stApp {
        background-image: url("https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=1470&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stTextInput>div>div>input {
        background-color: rgba(255,255,255,0.9);
        color: black;
    }
    .stButton>button {
        background-color: #FF6347;
        color: white;
    }
    .recipe-card, .ingredients-card, .steps-card {
        color: black;
        padding: 20px;
        border-radius: 15px;
        max-width: 700px;
        margin: 20px auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .recipe-card {
        background-color: rgba(255, 250, 240, 0.9);
    }
    .ingredients-card {
        background-color: rgba(255, 228, 196, 0.9);
        max-width: 500px;
    }
    .steps-card {
        background-color: rgba(224, 255, 255, 0.9);
        max-width: 500px;
    }
    .recipe-card:hover, .ingredients-card:hover, .steps-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }

    /* Center the title */
    .center-title {
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        margin-top: 20px;
    }

    /* Card for description + input */
    .input-card {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 15px;
        max-width: 800px;
        margin: 20px auto;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        color: black
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered title
st.markdown('<div class="center-title">🍳 CookMate AI 🍳</div>', unsafe_allow_html=True)

# Description + input inside a card
st.markdown(
    '<div class="input-card">'
    'Tell me what ingredients you have or what you\'re in the mood for, and I\'ll find the perfect recipe for you!<br><br>'
    '</div>',
    unsafe_allow_html=True
)

# User input outside the card
user_input = st.text_input("What do you want to cook today?", "")

if user_input:
    with st.spinner("Finding the perfect recipe..."):
        recipe_name = get_recipe_name(user_input)
        full_recipe = recipe_dict.get(recipe_name, "Recipe not found....")

    # Split recipe into sections
    lines = full_recipe.split("\n")
    recipe_title = lines[0].replace("Recipe: ", "")
    ingredients = []
    steps = []
    current_section = None
    for line in lines[1:]:
        if line.startswith("Ingredients:"):
            current_section = "ingredients"
            continue
        elif line.startswith("Steps:"):
            current_section = "steps"
            continue
        if current_section == "ingredients" and line.strip():
            ingredients.append(line.strip())
        elif current_section == "steps" and line.strip():
            steps.append(line.strip())

    # Display recipe in cards
    st.markdown(f'<div class="recipe-card"><h2 style="text-align:center;">{recipe_title}</h2></div>', unsafe_allow_html=True)

    # Ingredients card
    ingredients_html = "<ul>"
    for item in ingredients:
        ingredients_html += f"<li>{item}</li>"
    ingredients_html += "</ul>"
    st.markdown(f'<div class="ingredients-card"><h3 style="text-align:center;">Ingredients</h3>{ingredients_html}</div>', unsafe_allow_html=True)

    # Steps card
    steps_html = "<ol>"
    for step in steps:
        steps_html += f"<li>{step}</li>"
    steps_html += "</ol>"
    st.markdown(f'<div class="steps-card"><h3 style="text-align:center;">Steps</h3>{steps_html}</div>', unsafe_allow_html=True)
