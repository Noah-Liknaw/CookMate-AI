from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from local_llm import LocalLLM
import os
import streamlit as st

DB_DIR = "artifacts/chroma"

@st.cache_resource
def get_db():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    os.makedirs(DB_DIR, exist_ok=True)
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
        client_settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )

@st.cache_resource
def get_llm():
    return LocalLLM(model_name="google/flan-t5-base")

def get_recipe_name(user_input: str, k=5):
    db = get_db()
    llm = get_llm()

    results = db.similarity_search(user_input, k=k)
    recipe_titles = [doc.page_content.split("\n")[0].replace("Recipe: ", "") for doc in results]

    options_text = "\n".join([f"{i+1}. {title}" for i, title in enumerate(recipe_titles)])

    prompt = f"""
The user wants a recipe for: "{user_input}"

From the following recipe options, return ONLY the number of the recipe that best matches the user's request. 
Do NOT write anything else.

{options_text}
"""
    response = llm.generate(prompt, max_new_tokens=10).strip()

    try:
        choice = int(response) - 1
        return recipe_titles[choice]
    except:
        return recipe_titles[0]
