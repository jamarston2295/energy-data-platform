import json
import pandas as pd

from src.transformation.transform_carbon_intensity import transform
from src.utils.config import Config


def test_transform_creates_parquet():

    raw_file = (
        Config.RAW_DATA_DIR
        / "carbon_intensity_test.json"
    )

    sample_data = {
        "data": [
            {
                "from": "2026-06-01T00:00Z",
                "to": "2026-06-01T00:30Z",
                "intensity": {
                    "forecast": 100,
                    "actual": 95,
                    "index": "moderate"
                }
            }
        ]
    }

    with open(raw_file, "w") as f:
        json.dump(sample_data, f)

    transform()

    output_file = (
        Config.PROCESSED_DATA_DIR
        / "carbon_intensity.parquet"
    )

    assert output_file.exists()

    df = pd.read_parquet(output_file)

    assert len(df) == 1

    assert "forecast_intensity" in df.columns

def test_transform_has_expected_columns():

    output_file = (
        Config.PROCESSED_DATA_DIR
        / "carbon_intensity.parquet"
    )

    df = pd.read_parquet(output_file)

    expected_columns = {
        "from_time",
        "to_time",
        "forecast_intensity",
        "actual_intensity",
        "intensity_index"
    }

    assert set(df.columns) == expected_columns