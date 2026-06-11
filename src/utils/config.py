from pathlib import Path
from dotenv import load_dotenv
import os

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