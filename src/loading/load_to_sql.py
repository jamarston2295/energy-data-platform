import pandas as pd
from sqlalchemy import create_engine, text

from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

def get_engine():

    connection_string = (
        f"mssql+pyodbc://"
        f"{Config.AZURE_SQL_USERNAME}:"
        f"{Config.AZURE_SQL_PASSWORD}@"
        f"{Config.AZURE_SQL_SERVER}/"
        f"{Config.AZURE_SQL_DATABASE}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
    )

    return create_engine(connection_string)

def create_table(engine):

    create_table_sql = """
    IF NOT EXISTS (
        SELECT *
        FROM sys.tables
        WHERE name = 'carbon_intensity'
    )
    CREATE TABLE carbon_intensity (
        from_time VARCHAR(50),
        to_time VARCHAR(50),
        forecast_intensity INT,
        actual_intensity INT,
        intensity_index VARCHAR(20)
    )
    """

    with engine.begin() as conn:
        conn.execute(text(create_table_sql))

def load_parquet_to_sql(engine):

    logger.info("Reading transformed parquet file")

    df = pd.read_parquet(
        Config.PROCESSED_DATA_DIR
    )

    logger.info(
        f"Rows to load: {len(df)}"
    )

    df.to_sql(
        "carbon_intensity",
        con=engine,
        if_exists="append",
        index=False
    )

    logger.info(
        f"Loaded {len(df)} rows into Azure SQL"
    )

def clear_table(engine):

    logger.info(
        "Removing existing records from carbon_intensity"
    )

    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM carbon_intensity"
            )
        )

    logger.info(
        "Existing records removed"
    )

if __name__ == "__main__":

    engine = get_engine()

    create_table(engine)

    clear_table(engine)

    load_parquet_to_sql(engine)

