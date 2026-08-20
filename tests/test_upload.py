from unittest.mock import MagicMock, patch

from src.loading.upload_to_blob import upload_processed_data
from src.utils.config import Config


def test_upload_processed_data_uploads_file(
    tmp_path,
    monkeypatch
):

    test_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    test_file.write_bytes(
        b"test parquet data"
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        tmp_path
    )

    monkeypatch.setattr(
        Config,
        "AZURE_STORAGE_CONNECTION_STRING",
        "test-connection-string"
    )

    mock_blob_service = MagicMock()

    uploaded_content = {}

    def capture_upload(data, overwrite=False):
        uploaded_content["data"] = data.read()
        uploaded_content["overwrite"] = overwrite

    mock_blob_service.get_blob_client.return_value.upload_blob.side_effect = (
        capture_upload
    )

    with patch(
        "src.loading.upload_to_blob.BlobServiceClient"
    ) as mock_client:

        mock_client.from_connection_string.return_value = (
            mock_blob_service
        )

        upload_processed_data()

    mock_client.from_connection_string.assert_called_once_with(
        "test-connection-string"
    )

    mock_blob_service.get_blob_client.assert_called_once_with(
        container="processed",
        blob="carbon_intensity.parquet"
    )

    assert uploaded_content["data"] == b"test parquet data"

    assert uploaded_content["overwrite"] is True