# 🚀 Astro Airflow ETL Pipeline

A production-ready ETL pipeline built with Apache Airflow and Astro CLI that extracts data from CSV files and REST APIs, transforms and validates the data, then incrementally loads it into PostgreSQL.

---

# 📌 Overview

This project demonstrates an end-to-end ETL workflow orchestrated with Apache Airflow.

The pipeline extracts data from:
- A local CSV dataset (`retail_sales.csv`)
- The DummyJSON REST API (`dummyjson.com/products`)

After extraction, the data is transformed, validated, and incrementally loaded into PostgreSQL using an idempotent loading strategy.

---

# ✨ Features

- CSV and REST API ingestion
- Incremental loading using watermark logic
- PostgreSQL upserts with `ON CONFLICT`
- Retry and exponential backoff for API requests
- Modular Airflow DAG architecture
- Structured logging and monitoring
- Dockerized local development environment
- Astro CLI compatible

---

# 🏗️ Pipeline Architecture

```text
CSV File -----------\
                     \
                      --> Extract --> Transform --> Validate --> Load --> PostgreSQL
                     /
REST API -----------/
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | Apache Airflow 2.x |
| Runtime | Astro CLI |
| Database | PostgreSQL |
| API Requests | Python requests + urllib3 Retry |
| Containerization | Docker |
| Monitoring | Python logging |

---

# 📂 Project Structure

```text
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
```

---

# ⚡ Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/kareemashrafsaber7/airflow_etl.git

cd astro-airflow-pipelines
```

---

## 2. Configure Environment Variables

Create a `.env` file:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=retail_dw
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

---

## 3. Start Airflow

```bash
astro dev start
```

Airflow UI:
```text
http://localhost:8080
```

Default credentials:
```text
admin / admin
```

---

## 4. Configure PostgreSQL

Enter the PostgreSQL container:

```bash
docker exec -it airflow_6d7b1c-postgres-1 bash
```

Connect to PostgreSQL:

```bash
psql -U postgres
```

Run:

```sql
CREATE USER airflow WITH PASSWORD 'airflow';

ALTER USER airflow CREATEDB;

CREATE DATABASE airflow OWNER airflow;

GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
```

Reconnect using:

```bash
psql -U airflow -d airflow
```

---

## 5. Add Airflow Connection

In the Airflow UI:

```text
Admin → Connections
```

Create a PostgreSQL connection:

| Field | Value |
|---|---|
| Conn ID | postgres_default |
| Conn Type | Postgres |
| Host / Port / Schema | Values from `.env` |

---

## 6. Trigger the DAG

```bash
astro dev run dags trigger retail_etl_dag
```

---

# 🗄️ Database Schema

## dim_products

Stores product metadata.

| Column | Type |
|---|---|
| product_id | INT |
| title | VARCHAR |
| category | VARCHAR |
| price | NUMERIC |
| quantity | INT |

Example:

```text
1  | Essence Mascara Lash Princess | beauty     | 9.99
6  | Calvin Klein CK One           | fragrances | 49.99
11 | Annibale Colombo Bed          | furniture  | 1899.99
```

---

## fact_sales

Stores transactional sales data.

| Column | Type |
|---|---|
| sale_id | INT |
| product_id | INT |
| customer_id | INT |
| quantity | INT |
| price | NUMERIC |
| sale_date | DATE |

Example:

```text
1 | 101 | 1001 | 2 | 300.0 | 2025-01-01
2 | 102 | 1002 | 1 | 150.0 | 2025-01-02
3 | 103 | 1003 | 5 | 200.0 | 2025-01-03
```

---

# 🔄 Incremental Loading

The pipeline uses a high-watermark strategy:

1. Read the latest processed record
2. Extract only new records
3. Upsert records into PostgreSQL
4. Update the watermark after successful execution

This ensures:
- No duplicate ingestion
- Faster execution
- Safe reruns after failures
- Idempotent pipeline behavior

---

# 📊 Monitoring & Logging

Each Airflow task logs:

- Extracted row counts
- Loaded row counts
- Watermark updates
- Duplicate/skipped records
- Error tracebacks

Logs can be viewed through:
- Airflow task logs
- Docker container logs
- CI/CD integration
- Kafka streaming ingestion
- Airflow alerts and notifications
