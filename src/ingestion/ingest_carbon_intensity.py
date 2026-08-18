import json
import requests

from src.utils.config import Config
from src.utils.logger import get_logger
from datetime import datetime, timedelta, UTC

logger = get_logger(__name__)


def ingest():

    end_date = datetime.now(UTC)
    start_date = end_date - timedelta(days=14)

    start = start_date.strftime("%Y-%m-%dT%H:%MZ")
    end = end_date.strftime("%Y-%m-%dT%H:%MZ")

    url = (
        f"{Config.API_URL}/"
        f"{start}/{end}"
    )

    logger.info(f"Requesting data from {start} to {end}")

    all_data = []

    today = datetime.now(UTC).date()

    for i in range(14):

        day = today - timedelta(days=i)

        url = (
            f"{Config.API_URL}/date/"
            f"{day.strftime('%Y-%m-%d')}"
        )

        logger.info(f"Requesting {url}")

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        day_data = response.json()["data"]

        all_data.extend(day_data)

    data = {
        "data": all_data
    }

    output_file = (
        Config.RAW_DATA_DIR
        / "carbon_intensity_raw.json"
    )

    Config.RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    logger.info(
        f"Data written to {output_file}"
    )


if __name__ == "__main__":
    ingest()