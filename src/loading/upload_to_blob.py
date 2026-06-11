from azure.storage.blob import BlobServiceClient

from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

def upload_processed_data():

    logger.info(
        "Connecting to Azure Blob Storage"
    )

    blob_service_client = (
        BlobServiceClient.from_connection_string(
            Config.AZURE_STORAGE_CONNECTION_STRING
        )
    )

    local_file = (
        Config.PROCESSED_DATA_DIR
        / "carbon_intensity.parquet"
    )

    blob_client = (
        blob_service_client
        .get_blob_client(
            container="processed",
            blob="carbon_intensity.parquet"
        )
    )

    with open(local_file, "rb") as data:

        blob_client.upload_blob(
            data,
            overwrite=True
        )

        logger.info(
            "Upload completed successfully"
        )

if __name__ == "__main__":
    upload_processed_data()