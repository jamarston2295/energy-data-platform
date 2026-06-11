from src.utils.config import Config


def test_azure_connection_string_exists():

    assert (
        Config.AZURE_STORAGE_CONNECTION_STRING
        is not None
    )

    