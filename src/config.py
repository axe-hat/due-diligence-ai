import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SAMPLE_DIR = DATA_DIR / "sample"
CHROMA_PATH = os.getenv("CHROMA_PATH", str(DATA_DIR / "vectorstore"))

# LLM
LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma2:9b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")

# Embedding
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# SEC EDGAR
SEC_AGENT_NAME = os.getenv("SEC_AGENT_NAME", "DueDiligenceAI Bot")
SEC_AGENT_EMAIL = os.getenv("SEC_AGENT_EMAIL", "duediligenceai@proton.me")

# Retrieval
TOP_K = 8
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
