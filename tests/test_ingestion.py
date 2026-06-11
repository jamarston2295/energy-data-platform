from src.utils.config import Config


def test_api_url_exists():

    assert Config.API_URL is not None


def test_raw_data_directory_exists():

    assert Config.RAW_DATA_DIR.exists()