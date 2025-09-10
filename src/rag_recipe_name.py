from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from local_llm import LocalLLM

DB_DIR = "artifacts/chroma"

# Load embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Load vectorstore with embeddings
db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

# Instantiate LLM
llm = LocalLLM(model_name="google/flan-t5-base")

def get_recipe_name(user_input: str, k=5):
    # Retrieve top-k recipes based on embeddings
    results = db.similarity_search(user_input, k=k)

    # Extract only recipe titles
    recipe_titles = [doc.page_content.split("\n")[0].replace("Recipe: ", "") for doc in results]

    # Number the options
    options_text = "\n".join([f"{i+1}. {title}" for i, title in enumerate(recipe_titles)])

    # Build prompt instructing model to pick a number
    prompt = f"""
The user wants a recipe for: "{user_input}"

From the following recipe options, return ONLY the number of the recipe that best matches the user's request. 
Do NOT write anything else.

{options_text}
"""

    # Generate response
    response = llm.generate(prompt, max_new_tokens=10).strip()

    # Map number to recipe name
    try:
        choice = int(response) - 1
        return recipe_titles[choice]
    except:
        # fallback: first option
        return recipe_titles[0]

if __name__ == "__main__":
    user_input = "I am craving oatmeal. What can I cook?"
    print("User:", user_input)
    recipe_name = get_recipe_name(user_input)
    print("Suggested Recipe Name:", recipe_name)
