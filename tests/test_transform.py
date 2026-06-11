from src.utils.config import Config


def test_processed_directory_exists():

    assert (
        Config.PROCESSED_DATA_DIR.exists()
    )