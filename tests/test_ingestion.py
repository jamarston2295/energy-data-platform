from pathlib import Path
import json

from src.ingestion.ingest_carbon_intensity import save_raw_data


def test_save_raw_data_creates_file(tmp_path):

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

    output_file = tmp_path / "test.json"

    save_raw_data(sample_data, output_file)

    assert output_file.exists()

    with open(output_file) as f:
        loaded_data = json.load(f)

    assert loaded_data == sample_data