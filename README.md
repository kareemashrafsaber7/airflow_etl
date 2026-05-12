🚀 Astro Airflow ETL Platform

A scalable ETL workflow built with Apache Airflow and Astro CLI that ingests data from both flat files and REST APIs, processes and validates it, then incrementally loads clean datasets into PostgreSQL.

📖 Project Summary

This project demonstrates a production-style data engineering pipeline orchestrated with Apache Airflow.
The workflow combines data from:

A local CSV dataset (retail_sales.csv)
The DummyJSON Products API

The pipeline performs extraction, transformation, validation, and incremental loading into PostgreSQL while maintaining observability through structured logging and Airflow monitoring.

The architecture is designed to be modular, fault-tolerant, and idempotent, making it suitable for scalable ETL workflows and real-world orchestration practices.

🏗️ System Flow
           ┌────────────────────┐
           │   CSV Data Source  │
           │  retail_sales.csv  │
           └─────────┬──────────┘
                     │
                     │
           ┌─────────▼──────────┐
           │    REST API Source │
           │ DummyJSON Products │
           └─────────┬──────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │    Extraction Layer  │
          │  CSV + API ingestion │
          └─────────┬────────────┘
                    ▼
          ┌──────────────────────┐
          │ Transformation Layer │
          │ Cleaning & shaping   │
          └─────────┬────────────┘
                    ▼
          ┌──────────────────────┐
          │  Validation Layer    │
          │ Data quality checks  │
          └─────────┬────────────┘
                    ▼
          ┌──────────────────────┐
          │ Incremental Loading  │
          │ PostgreSQL Upserts   │
          └─────────┬────────────┘
                    ▼
          ┌──────────────────────┐
          │ Monitoring & Logging │
          └──────────────────────┘
✨ Core Features
Multi-Source Data Ingestion

Extracts data from:

Local CSV files
External REST APIs
Fault-Tolerant API Requests

The API extractor includes:

Automatic retries
Exponential backoff
Custom HTTP headers
Resilient request handling
Incremental Processing

Implements watermark-based loading to:

Prevent duplicate ingestion
Avoid full-table reloads
Support safe reruns
Data Validation

Dedicated validation tasks ensure:

Schema consistency
Clean records
Reliable downstream loading
PostgreSQL Integration

Uses:

Structured warehouse tables
Upsert operations
Conflict resolution with ON CONFLICT
Workflow Orchestration

Apache Airflow manages:

Scheduling
Dependencies
Task retries
Execution tracking
Observability

Structured logging provides:

Extracted row counts
Loaded row counts
Watermark tracking
Error diagnostics
🛠️ Technology Stack
Layer	Technology
Orchestration	Apache Airflow 2.x
Runtime Environment	Astro CLI
Database	PostgreSQL
API Handling	Python Requests + urllib3 Retry
Containerization	Docker
Monitoring	Python Logging
📂 Repository Structure
astro-airflow-pipelines/
│
├── dags/
│   └── retail_etl_dag.py
│
├── include/
│   ├── data/
│   │   └── retail_sales.csv
│   │
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   └── load_postgre.py
│
├── tests/
├── .astro/
├── Dockerfile
├── requirements.txt
└── README.md
⚙️ Local Setup
Requirements

Before running the project, install:

Docker Desktop
Astro CLI
PostgreSQL
1. Clone Repository
git clone https://github.com/ali-essam2002/astro-airflow-pipelines.git

cd astro-airflow-pipelines
2. Configure Environment Variables

Create a .env file:

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
3. Start Airflow Environment
astro dev start

Airflow UI:

http://localhost:8080

Default credentials:

Username: admin
Password: admin
4. Configure PostgreSQL Container

Enter the PostgreSQL container:

docker exec -it airflow_6d7b1c-postgres-1 bash

Connect to PostgreSQL:

psql -U postgres

Create the Airflow database and user:

CREATE USER airflow WITH PASSWORD 'airflow';

ALTER USER airflow CREATEDB;

CREATE DATABASE airflow OWNER airflow;

GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;

Verify roles:

\du

Reconnect using the new user:

psql -U airflow -d airflow
5. Configure Airflow Connection

Inside the Airflow UI:

Admin → Connections

Create a new PostgreSQL connection:

Field	Value
Conn ID	postgres_default
Conn Type	Postgres
Host / Port / Schema	Values from .env
6. Run the DAG

Trigger the pipeline manually:

astro dev run dags trigger retail_etl_dag
🗄️ Warehouse Schema
dim_products

Product dimension table storing product metadata.

Column	Type
product_id	INT
title	VARCHAR
category	VARCHAR
price	NUMERIC
quantity	INT

Example:

1   | Essence Mascara Lash Princess | beauty     | 9.99
6   | Calvin Klein CK One           | fragrances | 49.99
11  | Annibale Colombo Bed          | furniture  | 1899.99
fact_sales

Transactional sales table.

Column	Type
sale_id	INT
product_id	INT
customer_id	INT
quantity	INT
price	NUMERIC
sale_date	DATE

Example:

1 | 101 | 1001 | 2 | 300.0 | 2025-01-01
2 | 102 | 1002 | 1 | 150.0 | 2025-01-02
3 | 103 | 1003 | 5 | 200.0 | 2025-01-03
🔄 Incremental Loading Strategy

The pipeline uses a high-watermark approach:

Read the latest successfully processed ID or timestamp
Extract only new records
Upsert records into PostgreSQL
Update the watermark after successful completion

This design ensures:

No duplicate records
Faster pipeline execution
Safe reruns after failure
Idempotent behavior
📊 Logging & Monitoring

Each Airflow task generates structured logs containing:

Number of extracted records
Number of inserted records
Watermark updates
Duplicate/skipped rows
Error stack traces

Logs can be monitored through:

Airflow task logs
Docker container output
🎯 Project Highlights
End-to-end ETL orchestration with Apache Airflow
Production-style incremental loading strategy
Retry-enabled REST API ingestion
PostgreSQL warehouse integration
Modular pipeline architecture
Dockerized local development environment
Astro CLI deployment ready
