import json
from unittest.mock import patch, MagicMock

from src.ingestion.ingest_carbon_intensity import ingest
from src.utils.config import Config


@patch("src.ingestion.ingest_carbon_intensity.requests.get")
def test_ingest_creates_json_file(mock_get):

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

    mock_get.return_value = mock_response

    ingest()

    output_file = (
        Config.RAW_DATA_DIR
        / "carbon_intensity_raw.json"
    )

    assert output_file.exists()

    with open(output_file) as f:
        data = json.load(f)

    assert "data" in data