from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

DB_DIR = "artifacts/chroma"

# Load recipes from file
def load_recipes(file_path="data/recipes.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Split recipes by double newline, each is one doc
    recipes = [r.strip() for r in content.split("\n\n") if r.strip()]
    return recipes

# Embed recipes and create Chroma DB
def create_vectorstore(recipes):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_texts(
        texts=recipes,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    db.persist()
    return db

if __name__ == "__main__":
    recipes = load_recipes()
    db = create_vectorstore(recipes)
    print(f"Loaded and embedded {len(recipes)} recipes.")
