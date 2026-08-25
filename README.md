# DSS150P Lab 01

**Full Name:** Antonio Paulo Cuyo
**Student Number:** 2024109584

## Purpose of the Laboratory

This lab explores the early stages of a data engineering pipeline. We were asked to identify and
profile raw data sources (CSV, JSON, Parquet, a REST API, and a PostgreSQL table). We
documented their structure and identified their risks. Finally, we formalized one source into a basic
database schema and data contract. 

## Software Requirements

- Python 3.14 (or the version specified in `.python-version`, if present)
- pandas
- pyarrow
- requests
- sqlalchemy
- psycopg2-binary
- Git

## Exact Steps to Reproduce the Environment

```bash
# Clone the repository
git clone https://github.com/antoniopaulocuyo/DSS150P_Lab01_Cuyo_AntonioPaulo
cd DSS150P_Lab01_Cuyo_AntonioPaulo

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

## Exact Commands to Start and Stop PostgreSQL

```bash
# Start PostgreSQL (and any other services defined in docker-compose.yml)
docker-compose up -d

# Confirm the container is running
docker ps

# Stop PostgreSQL
docker-compose down
```

## How to Run Each Python Script

All scripts are run from the repository root, with the virtual environment activated:

```bash
# Verify the environment and PostgreSQL connection
python3 src/verify_environment.py

# Profile the CSV, JSON, and Parquet sources
python3 src/profile_sources.py

# Retrieve and inspect the REST API source
python3 src/inspect_api.py
```

## Description of Each Source

| Source | Description |
|---|---|
| `customers.csv` | Flat-file export of customer records (name, email, city, signup date, segment) |
| `orders.json` | Semi-structured order records, including a nested `shipping` object per order |
| `products.parquet` | Columnar snapshot of product catalog data (price, stock, weight) |
| `REST API` | External JSON endpoint queried live and snapshotted to `data/raw/api_snapshot.json` |
| PostgreSQL (`support_tickets`) | Instructor-provided relational table of customer support tickets |

## Known Limitations or Unresolved Questions

- `customer_id` in `customers.csv` contains 3 duplicate values across 250 rows. The
  root cause has not been confirmed.
- The expected refresh for each source
  is not documented anywhere available to this lab and is marked unknown.
- `orders.json`'s nested `shipping` field was not fully flattened/validated in this
  lab.