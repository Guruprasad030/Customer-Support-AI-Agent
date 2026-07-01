import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Application Configuration
    """

    # ==========================
    # API Keys
    # ==========================
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change_this_secret_key"
    )

    # ==========================
    # LLM Configuration
    # ==========================
    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gemini-1.5-flash"
    )

    TEMPERATURE = float(
        os.getenv("TEMPERATURE", 0.3)
    )

    MAX_OUTPUT_TOKENS = int(
        os.getenv("MAX_OUTPUT_TOKENS", 2048)
    )

    # ==========================
    # Database
    # ==========================
    DATABASE_NAME = os.getenv(
        "DATABASE_NAME",
        "tickets.db"
    )

    # ==========================
    # RAG Configuration
    # ==========================
    DATA_FOLDER = os.getenv(
        "DATA_FOLDER",
        "data"
    )

    VECTOR_DB_PATH = os.getenv(
        "VECTOR_DB_PATH",
        "vectorstore"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    CHUNK_SIZE = int(
        os.getenv("CHUNK_SIZE", 1000)
    )

    CHUNK_OVERLAP = int(
        os.getenv("CHUNK_OVERLAP", 200)
    )

    TOP_K = int(
        os.getenv("TOP_K", 3)
    )

    # ==========================
    # Ticket Settings
    # ==========================
    DEFAULT_PRIORITY = "Medium"

    VALID_PRIORITIES = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    VALID_STATUS = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    # ==========================
    # Logging
    # ==========================
    LOG_FILE = os.getenv(
        "LOG_FILE",
        "logs.txt"
    )

    # ==========================
    # Application
    # ==========================
    APP_NAME = "Customer Support AI Agent"

    VERSION = "1.0.0"

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    HOST = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv("PORT", 8000)
  )
