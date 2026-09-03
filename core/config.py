import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

ARES_NAME = os.getenv("ARES_NAME", "ARES")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4")

MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", "20"))

MEMORY_DB = PROJECT_ROOT / "data" / "ares_memory.db"
LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(exist_ok=True)
MEMORY_DB.parent.mkdir(exist_ok=True)