# Energy Data Platform

An end-to-end data engineering project that ingests UK carbon intensity data from an external API, transforms and stores the data using Azure services, and exposes the resulting data through a Power BI monitoring dashboard.

The project demonstrates a complete data pipeline covering data ingestion, transformation, storage, orchestration, testing, CI, and visualisation.

## Architecture

## Overview

The platform retrieves carbon intensity data from the UK Carbon Intensity API and processes it through a series of stages:

1. Ingestion – retrieves carbon intensity data from the API and stores the raw response as JSON.
2. Transformation – converts the raw JSON into a structured Pandas DataFrame and stores it as Parquet.
3. Cloud storage – uploads the processed Parquet data to Azure Blob Storage.
4. SQL loading – loads the processed data into Azure SQL Database for querying and analysis.
5. Orchestration – coordinates the individual pipeline stages into a single end-to-end process.
6. Visualisation – Power BI connects to the SQL data to provide a monitoring dashboard.
7. Testing and CI – unit tests validate the pipeline components, with GitHub Actions automatically running Ruff and pytest.

The pipeline can also retrieve historical data, allowing multiple days of carbon intensity data to be processed and analysed.

## Data Pipeline
### 1. Ingestion

The ingestion process uses Python and the Carbon Intensity API to retrieve carbon intensity data.

The API response is saved locally as a raw JSON file:

```text
data/raw/carbon_intensity_raw.json
```

The ingestion process supports retrieving historical daily data, allowing the platform to build a larger historical dataset rather than relying solely on the latest API response.

The ingestion stage uses:

Python
Requests
JSON
Environment-based configuration
Python logging

### 2. Transformation

The transformation process reads the raw JSON data and extracts the relevant fields into a structured dataset.

The following fields are extracted:

| Field | Description |
| :--- | :--- |
| `from_time` | Start of the carbon intensity period |
| `to_time` | End of the carbon intensity period |
| `forecast_intensity` | Forecast carbon intensity |
| `actual_intensity` | Actual carbon intensity |
| `intensity_index` | Carbon intensity classification |

The resulting data is converted into a Pandas DataFrame and timestamps are converted into datetime values.

The transformed data is stored as a Parquet file:
```text
data/processed/carbon_intensity.parquet
```

Parquet was selected as the processed storage format because it provides a structured, columnar representation of the transformed dataset.

### 3. Azure Blob Storage

The processed Parquet dataset is uploaded to Azure Blob Storage.

The platform uses the processed container and stores the dataset as:

```text
carbon_intensity.parquet
```

The Azure connection string is provided through environment variables rather than being stored directly in the source code.

### 4. Azure SQL Database

The processed data is also loaded into Azure SQL Database.

The pipeline creates a carbon_intensity table if one does not already exist.

The table contains:

- from_time
- to_time
- forecast_intensity
- actual_intensity
- intensity_index

The SQL loading process uses SQLAlchemy and Pandas to load the transformed dataset into Azure SQL.

Before loading the dataset, existing records can be cleared to ensure that the SQL table represents the current processed dataset.

### 5. Orchestration

The individual pipeline stages are combined using the orchestration script:

```text
src/orchestration/run_pipeline.py
```

```text
This coordinates:

Ingestion
    ↓
Transformation
    ↓
Azure Blob Storage
    ↓
Azure SQL
```

This provides a single entry point for running the complete data pipeline.

## Power BI Dashboard

A Power BI monitoring dashboard has been developed using the Azure SQL data.

The dashboard provides a way to monitor and explore the carbon intensity data processed by the pipeline.

The Power BI file is included in the repository and provides the analytical layer on top of the processed SQL data.

The dashboard demonstrates how the output of a data engineering pipeline can be made available to end users for monitoring and analysis.

## Testing

The project includes unit tests covering the main pipeline components.

Tests are included for:

- Data ingestion
- Data transformation
- Azure Blob Storage upload
- Azure SQL loading

External services such as Azure Blob Storage and Azure SQL are mocked during unit testing, allowing the tests to run without requiring live Azure connections.

The tests can be run locally using:

```text
python -m pytest
```

## Continuous Integration

GitHub Actions is used to automatically validate changes to the project.

The CI workflow runs on pushes and pull requests against the master branch.

The workflow:

- Checks out the repository
- Sets up Python 3.13
- Installs project dependencies
- Runs Ruff
- Runs pytest

This provides automated code-quality and test checks before changes are considered complete.

## Code Quality

Ruff is used for Python linting and import organisation.

Run Ruff locally with:

```text
ruff check .
```

The test suite can then be run with:

```text
python -m pytest
```

Both checks are also performed automatically by GitHub Actions.

## Project Structure

```text
Energy Data Platform/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   └── architecture.png
│
├── src/
│   ├── ingestion/
│   │   └── ingest_carbon_intensity.py
│   │
│   ├── transformation/
│   │   └── transform_carbon_intensity.py
│   │
│   ├── loading/
│   │   ├── upload_to_blob.py
│   │   └── load_to_sql.py
│   │
│   ├── orchestration/
│   │   └── run_pipeline.py
│   │
│   └── utils/
│       ├── config.py
│       └── logger.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_transform.py
│   ├── test_upload.py
│   └── test_load_to_sql.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Configuration

Configuration and credentials are managed using environment variables.

A .env file is used locally for values such as:

```text
API_URL
AZURE_STORAGE_CONNECTION_STRING
AZURE_SQL_SERVER
AZURE_SQL_DATABASE
AZURE_SQL_USERNAME
AZURE_SQL_PASSWORD
```

The .env file should not be committed to source control.

A .env.example file can be used to document the required configuration without exposing credentials.

## Running the Pipeline

### 1. Create and activate a virtual environment

Windows:

```text
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```text
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a .env file containing the required API and Azure configuration.

### 4. Run the complete pipeline

```text
python -m src.orchestration.run_pipeline
```

### 5. Run the tests

```text
python -m pytest
```

6. Run code-quality checks

```text
ruff check .
```

## Technologies

| Area | Technology |
| :--- | :--- |
| **Language** | Python |
| **Data ingestion** | Requests |
| **Data processing** | Pandas |
| **Processed storage** | Parquet |
| **Cloud storage** | Azure Blob Storage |
| **Database** | Azure SQL Database |
| **Database connectivity** | SQLAlchemy / pyodbc |
| **Visualisation** | Power BI |
| **Testing** | pytest |
| **Code quality** | Ruff |
| **CI** | GitHub Actions |
| **Version control** | Git / GitHub |

## Future Improvements

Potential future improvements include:

- Introducing a dedicated cloud orchestration service such as Azure Data Factory or Microsoft Fabric pipelines.
- Adding more comprehensive data-quality validation.
- Implementing incremental loading rather than replacing the SQL dataset.
- Adding pipeline failure alerting and operational monitoring.
- Expanding the Power BI dashboard with additional historical analysis.
- Introducing infrastructure-as-code for the Azure resources.