from unittest.mock import MagicMock


def test_blob_upload_called():

    mock_blob_client = MagicMock()

    mock_blob_client.upload_blob(
        b"test",
        overwrite=True
    )

    mock_blob_client.upload_blob.assert_called_once()