import pandas as pd

def transform():
    df = pd.read_csv("/opt/airflow/data/raw_data.csv")

    # Example transformation
    df["trip_speed"] = df["distance"] / df["duration"]

    # Save transformed data
    df.to_csv(
    "/opt/airflow/data/processed_data.csv",
    index=False)

    print("Transformation complete")