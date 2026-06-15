import pandas as pd


def test_dataframe_has_expected_schema():

    df = pd.DataFrame(
        {
            "from_time": ["2026-06-01"],
            "to_time": ["2026-06-01"],
            "forecast_intensity": [100],
            "actual_intensity": [95],
            "intensity_index": ["moderate"]
        }
    )

    expected_columns = {
        "from_time",
        "to_time",
        "forecast_intensity",
        "actual_intensity",
        "intensity_index"
    }

    assert set(df.columns) == expected_columns