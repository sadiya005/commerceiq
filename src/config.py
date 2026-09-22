import os
from pathlib import Path

from dotenv import load_dotenv


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / "data"

# Environment variables
load_dotenv(PROJECT_ROOT / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Models
TEXT_MODEL = "openai/gpt-oss-20b"
VISION_MODEL = "qwen/qwen3.8-27b"

# Data files
CUSTOMER_DATA_PATH = DATA_DIR / "customer_features.csv"
PRODUCT_DATA_PATH = DATA_DIR / "product_features.csv"
ORDER_DATA_PATH = DATA_DIR / "order_analytics.csv"


def validate_config():
    """Validate required CommerceIQ configuration."""

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    required_files = [
        CUSTOMER_DATA_PATH,
        PRODUCT_DATA_PATH,
        ORDER_DATA_PATH
    ]

    missing_files = [
        str(path)
        for path in required_files
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing required data files:\n"
            + "\n".join(missing_files)
        )

    return True
    