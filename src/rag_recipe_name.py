from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from local_llm import LocalLLM
import os

DB_DIR = "artifacts/chroma"

# Load embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Ensure DB folder exists
os.makedirs(DB_DIR, exist_ok=True)

# Load vectorstore with embeddings
db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings,
    client_settings=Settings(
        anonymized_telemetry=False,  # prevent chroma startup crash
        allow_reset=True             # allow reload/reset
    )
)

# Instantiate LLM
llm = LocalLLM(model_name="google/flan-t5-base")
