🚀 Astro Airflow ETL Pipeline

Production-ready ETL pipeline built with Apache Airflow and Astro CLI that extracts data from CSV files and REST APIs, transforms and validates it, then incrementally loads clean data into PostgreSQL.

📌 Features
CSV + REST API ingestion
Incremental loading with watermarking
PostgreSQL upserts
Retry & exponential backoff for API requests
Modular Airflow DAG design
Structured logging & monitoring
Dockerized local environment
Astro CLI ready
🏗️ Architecture
CSV File ─────┐
              ├── Extract ──► Transform ──► Validate ──► Load ──► PostgreSQL
REST API ─────┘
🛠️ Tech Stack
Layer	Technology
Orchestration	Apache Airflow
Runtime	Astro CLI
Database	PostgreSQL
API Requests	requests + urllib3
Containerization	Docker
📂 Project Structure
astro-airflow-pipelines/
│
├── dags/
│   └── retail_etl_dag.py
│
├── include/
│   ├── data/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   └── load_postgre.py
│
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
⚡ Quick Start
Clone Repository
git clone https://github.com/kareemashrafsaber7/airflow_etl.git

cd astro-airflow-pipelines
Configure Environment Variables
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
Start Airflow
astro dev start

Airflow UI:

http://localhost:8080

Default credentials:

admin / admin
🗄️ Database Tables
dim_products

Stores product metadata.

Column	Type
product_id	INT
title	VARCHAR
category	VARCHAR
price	NUMERIC
fact_sales

Stores transactional sales data.

Column	Type
sale_id	INT
product_id	INT
customer_id	INT
quantity	INT
price	NUMERIC
sale_date	DATE
🔄 Incremental Loading

The pipeline uses a high-watermark strategy:

Read latest processed record
Extract only new data
Upsert into PostgreSQL
Update watermark after success

This keeps the pipeline idempotent and prevents duplicate ingestion.

📊 Monitoring

Each Airflow task logs:

Extracted rows
Loaded rows
Watermark updates
Duplicate records
Error tracebacks

Logs are accessible through Airflow UI and Docker container logs.
