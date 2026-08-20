import json
from unittest.mock import MagicMock, patch

import requests

from src.ingestion.ingest_carbon_intensity import ingest
from src.utils.config import Config


def test_ingest_creates_json_file(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    mock_response = MagicMock()

    mock_response.json.return_value = {
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

    with patch(
        "src.ingestion.ingest_carbon_intensity.requests.get",
        return_value=mock_response
    ) as mock_get:

        ingest()

    # The pipeline retrieves the previous 14 days.
    assert mock_get.call_count == 14

    # Every request should use the configured timeout.
    for call in mock_get.call_args_list:
        assert call.kwargs["timeout"] == 30

    output_file = (
        tmp_path
        / "carbon_intensity_raw.json"
    )

    assert output_file.exists()

    with open(output_file) as file:
        data = json.load(file)

    assert "data" in data
    assert len(data["data"]) == 14


def test_ingest_raises_for_http_error(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    mock_response = MagicMock()

    mock_response.raise_for_status.side_effect = (
        requests.HTTPError("API request failed")
    )

    with patch(
        "src.ingestion.ingest_carbon_intensity.requests.get",
        return_value=mock_response
    ):

        try:
            ingest()

        except requests.HTTPError:
            pass

        else:
            raise AssertionError(
                "ingest() should raise HTTPError"
            )


def test_ingest_writes_expected_api_data(tmp_path, monkeypatch):

    monkeypatch.setattr(
        Config,
        "RAW_DATA_DIR",
        tmp_path
    )

    expected_record = {
        "from": "2026-06-01T00:00Z",
        "to": "2026-06-01T00:30Z",
        "intensity": {
            "forecast": 100,
            "actual": 95,
            "index": "moderate"
        }
    }

    mock_response = MagicMock()

    mock_response.json.return_value = {
        "data": [expected_record]
    }

    with patch(
        "src.ingestion.ingest_carbon_intensity.requests.get",
        return_value=mock_response
    ):

        ingest()

    output_file = (
        tmp_path
        / "carbon_intensity_raw.json"
    )

    with open(output_file) as file:
        actual_data = json.load(file)

    assert len(actual_data["data"]) == 14

    for record in actual_data["data"]:
        assert record == expected_record