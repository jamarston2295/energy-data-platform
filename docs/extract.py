import pandas as pd

def extract():
    df = pd.DataFrame({
        "distance": [1, 2, 3, 4],
        "duration": [10, 20, 30, 40]
    })

    df.to_csv("/opt/airflow/data/raw_data.csv", index=False)

    print("Running extract step...")

# import pandas as pd

# def extract():
#     print("EXTRACT FUNCTION RUNNING")

#     df = pd.DataFrame({
#         "distance": [1, 2, 3],
#         "duration": [10, 20, 30]
#     })

#     df.to_csv("/opt/airflow/data/raw_data.csv", index=False)

#     print("CSV SAVED")