import json
import pandas as pd

from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def transform():

    logger.info(
        "Starting transformation"
    )

    latest_file = max(
        Config.RAW_DATA_DIR.glob(
            "carbon_intensity_*.json"
        ),
        key=lambda x: x.stat().st_mtime
    )

    logger.info(
        f"Reading {latest_file.name}"
    )

    with open(latest_file) as file:
        data = json.load(file)

    records = []

    for row in data["data"]:

        records.append(
            {
                "from_time": row["from"],
                "to_time": row["to"],
                "forecast_intensity":
                    row["intensity"]["forecast"],
                "actual_intensity":
                    row["intensity"]["actual"],
                "intensity_index":
                    row["intensity"]["index"]
            }
        )

    df = pd.DataFrame(records)

    df["from_time"] = pd.to_datetime(
        df["from_time"]
    )

    df["to_time"] = pd.to_datetime(
        df["to_time"]
    )

    assert len(df) > 0

    required_columns = [
    "from_time",
    "to_time",
    "forecast_intensity",
    "actual_intensity",
    "intensity_index"
    ]

    for column in required_columns:

        assert (
            column in df.columns
        ), f"Missing column: {column}"

    output_file = (
        Config.PROCESSED_DATA_DIR
        / "carbon_intensity.parquet"
    )

    df.to_parquet(
        output_file,
        index=False
    )

    logger.info(
        f"Saved to {output_file}"
    )


if __name__ == "__main__":
    transform()