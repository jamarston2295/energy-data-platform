import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

class Config:

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

    PROCESSED_DATA_DIR = (
        PROJECT_ROOT
        / "data"
        / "processed"
    )

    API_URL = (
        "https://api.carbonintensity.org.uk/intensity"
    )

    AZURE_STORAGE_CONNECTION_STRING = (
        os.getenv(
            "AZURE_STORAGE_CONNECTION_STRING"
        )
    )

    AZURE_SQL_SERVER = os.getenv(
    "AZURE_SQL_SERVER"
    )

    AZURE_SQL_DATABASE = os.getenv(
        "AZURE_SQL_DATABASE"
    )

    AZURE_SQL_USERNAME = os.getenv(
        "AZURE_SQL_USERNAME"
    )

    AZURE_SQL_PASSWORD = os.getenv(
        "AZURE_SQL_PASSWORD"
    )