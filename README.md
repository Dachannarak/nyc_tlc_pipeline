# 🚕 NYC TLC Data Pipeline (Airflow)

## 📌 Overview

This project implements a **batch data pipeline** for processing NYC Taxi & Limousine Commission (TLC) data using Apache Airflow.

The pipeline follows a **Medallion Architecture (Bronze → Silver → Gold)** to ensure data quality, scalability, and reliability.

---

## 🧠 Architecture & Workflow

```
Data Source
   ↓
Ingestion
   ↓
Bronze (Raw Data)
   ↓
Data Quality Check
   ↓
Silver (Cleaned Data)
   ↓
Gold (Aggregated Data)
   ↓
Serving (Dashboard / ML)
```
<img width="692" height="480" alt="image" src="https://github.com/user-attachments/assets/c6c0982e-85d3-4421-9335-2018b3e8f3aa" />

---

## 🧱 Data Layers

### 1️⃣ Data Source

* NYC Open Data API (TLC DSP)
* Format: JSON (REST API)
* Update: Daily (Batch)

---

### 2️⃣ Ingestion Layer

* Fetch data from API
* Store raw data into Bronze layer

---

### 3️⃣ Bronze Layer (Raw)

* Stores raw JSON data
* No transformation applied
* Includes metadata logging

---

### 4️⃣ Data Quality Layer

Data validation before processing:

* Null check
* Duplicate check
* Row count validation

If validation fails → pipeline stops
If validation passes → continue to Silver

---

### 5️⃣ Silver Layer (Cleaned)

Data transformation:

* Remove null values
* Remove duplicates
* Standardize text format
* Convert data types

---

### 6️⃣ Gold Layer (Business Ready)

Aggregated metrics:

* Total providers
* Active providers
* Status breakdown

Used for:

* Dashboard
* Analytics
* Machine Learning

---

### 7️⃣ Serving Layer

* Dashboard (Metabase / Superset)
* ML Models

---

## ⚙️ Airflow DAGs

### 🔹 Main DAG

```
nyc_tlc_pipeline
```

### 🔁 Workflow

```
start
 → ingestion
 → quality_check
 → silver
 → gold
end
```

---

### 📂 Sub DAGs

#### 1. ingestion

* Fetch data from API
* Save to Bronze

#### 2. quality_check

* Validate data
* Branch (pass / fail)

#### 3. silver

* Clean & transform data

#### 4. gold

* Create aggregated metrics

---

## 🛠️ Tech Stack

| Component     | Technology        |
| ------------- | ----------------- |
| Orchestration | Apache Airflow    |
| Language      | Python 3          |
| Container     | Docker            |
| Database      | PostgreSQL        |
| Queue         | Redis             |
| Storage       | Local File System |

---

## 📁 Project Structure

```
nyc_tlc_pipeline/
├── dags/
│   ├── nyc_tlc_pipeline.py
│   ├── nyc_tlc_ingestion.py
│   ├── nyc_tlc_quality_check.py
│   ├── nyc_tlc_silver.py
│   └── nyc_tlc_gold.py
├── docker-compose.yaml
├── README.md
```

---

## ▶️ How to Run

### 1. Start Airflow

```
docker compose up -d
```

### 2. Open Airflow UI

```
http://localhost:8080
```

Login:

* Username: airflow
* Password: airflow

---

### 3. Run Pipeline

* Enable DAG `nyc_tlc_pipeline`
* Click **Trigger DAG**
* Monitor execution in Graph view

---

## 🚀 Key Features

* Batch Data Pipeline
* Medallion Architecture (Bronze / Silver / Gold)
* Data Quality Validation Layer
* Apache Airflow Orchestration
* End-to-End Data Workflow

---

## 🎯 Summary

This project demonstrates how to design and implement a scalable data pipeline using Apache Airflow with proper data layering, validation, and transformation.

---

## 📌 Future Improvements

* Add dashboard integration (Metabase / Superset)
* Add alert system (Email / Slack)
* Move storage to cloud (S3 / GCS)
* Add ML model integration
* Implement data lineage tracking

---
