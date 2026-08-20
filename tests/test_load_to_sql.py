from unittest.mock import MagicMock, patch

import pandas as pd

from src.loading.load_to_sql import (
    get_engine,
    create_table,
    load_parquet_to_sql,
    clear_table
)
from src.utils.config import Config


def test_get_engine():

    with patch(
        "src.loading.load_to_sql.create_engine"
    ) as mock_create_engine:

        get_engine()

    connection_string = (
        f"mssql+pyodbc://"
        f"{Config.AZURE_SQL_USERNAME}:"
        f"{Config.AZURE_SQL_PASSWORD}@"
        f"{Config.AZURE_SQL_SERVER}/"
        f"{Config.AZURE_SQL_DATABASE}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
    )

    mock_create_engine.assert_called_once_with(
        connection_string
    )


def test_create_table():

    mock_engine = MagicMock()
    mock_connection = MagicMock()

    mock_engine.begin.return_value.__enter__.return_value = (
        mock_connection
    )

    create_table(mock_engine)

    mock_connection.execute.assert_called_once()

    executed_sql = (
        mock_connection.execute.call_args.args[0]
    )

    assert "CREATE TABLE carbon_intensity" in str(
        executed_sql
    )

    assert "from_time" in str(executed_sql)
    assert "to_time" in str(executed_sql)
    assert "forecast_intensity" in str(executed_sql)
    assert "actual_intensity" in str(executed_sql)
    assert "intensity_index" in str(executed_sql)


@patch(
    "src.loading.load_to_sql.pd.read_parquet"
)
def test_load_parquet_to_sql(
    mock_read_parquet,
    tmp_path,
    monkeypatch
):

    parquet_file = (
        tmp_path
        / "carbon_intensity.parquet"
    )

    monkeypatch.setattr(
        Config,
        "PROCESSED_DATA_DIR",
        parquet_file
    )

    df = pd.DataFrame(
        {
            "from_time": ["2026-06-01"],
            "to_time": ["2026-06-01"],
            "forecast_intensity": [100],
            "actual_intensity": [95],
            "intensity_index": ["moderate"]
        }
    )

    mock_read_parquet.return_value = df

    mock_engine = MagicMock()

    with patch.object(
        pd.DataFrame,
        "to_sql"
    ) as mock_to_sql:

        load_parquet_to_sql(mock_engine)

    mock_read_parquet.assert_called_once_with(
        parquet_file
    )

    mock_to_sql.assert_called_once_with(
        "carbon_intensity",
        con=mock_engine,
        if_exists="append",
        index=False
    )


def test_clear_table():

    mock_engine = MagicMock()
    mock_connection = MagicMock()

    mock_engine.begin.return_value.__enter__.return_value = (
        mock_connection
    )

    clear_table(mock_engine)

    mock_connection.execute.assert_called_once()

    executed_sql = (
        mock_connection.execute.call_args.args[0]
    )

    assert "DELETE FROM carbon_intensity" in str(
        executed_sql
    )