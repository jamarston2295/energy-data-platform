import pandas as pd
from sqlalchemy import create_engine


def load():

    print("Starting load step...")

    # Read processed data
    df = pd.read_csv("/opt/airflow/data/processed_data.csv")

    # Postgres connection
    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres/airflow"
    )

    # Load into database
    df.to_sql(
        "taxi_trips",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded to Postgres")