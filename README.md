# Energy Data Platform

## Overview

This project is an end-to-end cloud data engineering pipeline that ingests real-time UK carbon intensity data from the National Grid API, transforms and validates the data, stores processed datasets in Azure Blob Storage, and loads analytics-ready data into Azure SQL Database.

The project demonstrates industry-standard data engineering practices including modular ETL design, automated testing, configuration management, logging, cloud storage integration, and CI/CD.

## Architecture

National Grid API → Raw JSON → Transformation → Parquet → Azure Blob Storage → Azure SQL Database

## Tech Stack

* Python
* Pandas
* Pytest
* Azure Blob Storage
* Azure SQL Database
* SQLAlchemy
* PyODBC
* Git & GitHub
* GitHub Actions
* Parquet
* REST APIs

## Features

### Data Ingestion

* Retrieves carbon intensity data from the National Grid API
* Stores raw API responses locally as JSON
* Preserves source data for auditing and reprocessing

### Data Transformation

* Cleans and validates incoming data
* Performs schema standardisation
* Converts processed data to Parquet format

### Cloud Storage

* Uploads processed datasets to Azure Blob Storage
* Demonstrates cloud-based data lake architecture

### Database Loading

* Loads transformed data into Azure SQL Database
* Uses idempotent loading to prevent duplicate records

### Testing

* Automated unit tests using Pytest
* Validation of ingestion, transformation and loading components

### Logging & Configuration

* Centralised logging
* Environment variable management via .env
* Reusable configuration module

## Project Structure

src/

* ingestion/
* transformation/
* loading/
* orchestration/
* utils/

tests/

* unit tests

docs/

* architecture documentation

## Running the Pipeline

python -m src.orchestration.run_pipeline

## Future Improvements

* Power BI dashboard integration
* Automated scheduling
* Data quality monitoring
* Infrastructure as Code
* Containerisation with Docker

## Author

John Marston
