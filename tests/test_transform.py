import pandas as pd

from src.transformation.transform_carbon_intensity import transform_data


def test_transform_creates_expected_columns():

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

    df = transform_data(sample_data)

    expected_columns = [
        "from_time",
        "to_time",
        "forecast_intensity",
        "actual_intensity",
        "intensity_index"
    ]

    assert list(df.columns) == expected_columns
    assert len(df) == 1