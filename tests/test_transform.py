import json

import pandas as pd

from src.transformation.transform_carbon_intensity import transform
from src.utils.config import Config

SAMPLE_DATA = {
    "data": [
        {
            "from": "2026-06-01T00:00Z",
            "to": "2026-06-01T00:30Z",
            "intensity": {
                "forecast": 100,
                "actual": 95,
                "index": "moderate"
            }
        },
        {
            "from": "2026-06-01T00:30Z",
            "to": "2026-06-01T01:00Z",
            "intensity": {
                "forecast": 110,
                "actual": 105,
                "index": "moderate"
            }
        }
    ]
}


def create_raw_test_file(tmp_path):
    raw_file = (
        tmp_path
        / "carbon_intensity_test.json"
    )

    with open(raw_file, "w") as file:
        json.dump(SAMPLE_DATA, file)

    return raw_file


def test_transform_creates_parquet(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    create_raw_test_file(tmp_path)

    transform()

    output_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    assert output_file.exists()

    df = pd.read_parquet(output_file)

    assert len(df) == 2


def test_transform_has_expected_columns(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    create_raw_test_file(tmp_path)

    transform()

    output_file = (
        tmp_path
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


def test_transform_has_datetime_columns(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    create_raw_test_file(tmp_path)

    transform()

    output_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    df = pd.read_parquet(output_file)

    assert pd.api.types.is_datetime64_any_dtype(
        df["from_time"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        df["to_time"]
    )


def test_transform_has_no_null_values(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    create_raw_test_file(tmp_path)

    transform()

    output_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    df = pd.read_parquet(output_file)

    required_columns = [
        "from_time",
        "to_time",
        "forecast_intensity",
        "actual_intensity",
        "intensity_index"
    ]

    assert not df[required_columns].isnull().any().any()


def test_transform_has_valid_time_ranges(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    create_raw_test_file(tmp_path)

    transform()

    output_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    df = pd.read_parquet(output_file)

    assert (df["from_time"] < df["to_time"]).all()


def test_transform_has_valid_intensity_values(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    create_raw_test_file(tmp_path)

    transform()

    output_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    df = pd.read_parquet(output_file)

    assert (
        df["forecast_intensity"]
        .apply(lambda value: isinstance(value, (int, float)))
        .all()
    )

    assert (
        df["actual_intensity"]
        .apply(lambda value: isinstance(value, (int, float)))
        .all()
    )

    assert (df["forecast_intensity"] >= 0).all()
    assert (df["actual_intensity"] >= 0).all()


def test_transform_has_valid_intensity_index(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    create_raw_test_file(tmp_path)

    transform()

    output_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    df = pd.read_parquet(output_file)

    valid_indexes = {
        "very low",
        "low",
        "moderate",
        "high",
        "very high"
    }

    assert set(
        df["intensity_index"].dropna()
    ).issubset(valid_indexes)


def test_transform_has_no_duplicate_time_periods(
    tmp_path,
    monkeypatch
):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    create_raw_test_file(tmp_path)

    transform()

    output_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    df = pd.read_parquet(output_file)

    assert not df.duplicated(
        subset=["from_time", "to_time"]
    ).any()