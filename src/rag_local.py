from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from local_llm import LocalLLM

DB_DIR = "artifacts/chroma"

# Load embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Load vectorstore with embeddings (with Chroma client settings)
db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings,
    client_settings=Settings(
        anonymized_telemetry=False,  # disable telemetry
        allow_reset=True             # allow reload if DB already exists
    )
)

# Instantiate LLM
llm = LocalLLM(model_name="google/flan-t5-base")

def answer_query(query: str, k=1):
    """
    Retrieve the top recipe matching the query and
    use the LLM to format it clearly.
    """
    results = db.similarity_search(query, k=k)
    if not results:
        return "Sorry, no matching recipe found."

    recipe_text = results[0].page_content

    prompt = f"""
You are a helpful cooking assistant.

User asked: "{query}"

Here is the matching recipe from the database:

{recipe_text}

Rewrite this recipe clearly with:

Recipe: <name>
Ingredients: <list, comma separated>
Steps:
1. Step one in full detail
2. Step two in full detail
...
Continue numbering all steps.
"""

    response = llm.generate(prompt, max_new_tokens=500)
    return response


if __name__ == "__main__":
    q = "What can I cook with spinach and garlic?"
    print("User:", q)
    print("Assistant:", answer_query(q))
