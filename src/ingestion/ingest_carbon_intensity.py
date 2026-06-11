import json
import requests

from src.utils.config import Config
from src.utils.logger import get_logger


logger = get_logger(__name__)


def ingest():

    logger.info(
        "Requesting carbon intensity data"
    )

    response = requests.get(
        Config.API_URL,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    output_file = (
        Config.RAW_DATA_DIR
        / "carbon_intensity_raw.json"
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