from src.ingestion.ingest_carbon_intensity import ingest
from src.loading.load_to_sql import (
    clear_table,
    create_table,
    get_engine,
    load_parquet_to_sql,
)
from src.loading.upload_to_blob import upload_processed_data
from src.transformation.transform_carbon_intensity import transform
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_pipeline():

    logger.info("Pipeline started")

    ingest()

    transform()

    upload_processed_data()

    engine = get_engine()

    create_table(engine)

    clear_table(engine)

    load_parquet_to_sql(engine)

    logger.info("Pipeline completed")

if __name__ == "__main__":
    run_pipeline()