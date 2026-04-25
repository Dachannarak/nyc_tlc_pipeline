# 🚕 NYC TLC Data Pipeline (Airflow)

## 📌 ภาพรวมโปรเจค

โปรเจคนี้เป็นการสร้าง **Data Pipeline แบบ Batch** สำหรับประมวลผลข้อมูลจาก NYC Taxi & Limousine Commission (TLC) โดยใช้ Apache Airflow เป็นตัวควบคุมการทำงาน (Orchestration)

Pipeline นี้ออกแบบตามแนวคิด **Medallion Architecture (Bronze → Silver → Gold)** เพื่อให้ข้อมูลมีคุณภาพ และสามารถนำไปใช้งานได้จริง

---

## 🧠 โครงสร้างการไหลของข้อมูล (Workflow)

```text
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
<img width="1019" height="228" alt="image" src="https://github.com/user-attachments/assets/7efb2598-eb22-4e9f-9ba1-8770a5700c06" />

---

## 🧱 Layer ของข้อมูล

### 1️⃣ Data Source
- ข้อมูลจาก NYC Open Data API (TLC DSP)
- รูปแบบ: JSON (REST API)
- อัปเดต: รายวัน (Batch)

### 2️⃣ Ingestion Layer
- ดึงข้อมูลจาก API
- บันทึกลง Bronze Layer

### 3️⃣ Bronze Layer (Raw Data)
- เก็บข้อมูลดิบ (ยังไม่ผ่านการประมวลผล)
- เก็บในรูปแบบ JSON
- มีการเก็บ metadata

> **⚠️ หมายเหตุ:** folder `bronze/` ไม่ได้อยู่ใน repo เพราะเป็น runtime data  
> เมื่อรัน pipeline ครั้งแรก ingestion DAG จะสร้าง folder และบันทึกไฟล์ลง container อัตโนมัติ  
> ```
> /opt/airflow/data/bronze/nyc_tlc_dsp_raw.json
> ```
> ข้อมูลดิบจาก API จะอยู่ใน container ไม่ใช่ใน repo

### 4️⃣ Data Quality Layer

ตรวจสอบคุณภาพข้อมูลก่อนใช้งาน:
- ✅ ตรวจสอบค่า Null
- ✅ ตรวจสอบข้อมูลซ้ำ (Duplicate)
- ✅ ตรวจสอบจำนวนข้อมูล (Row count)

📌 ถ้าไม่ผ่าน → หยุด Pipeline  
📌 ถ้าผ่าน → ส่งต่อไป Silver

### 5️⃣ Silver Layer (Cleaned Data)

ทำความสะอาดและแปลงข้อมูล:
- ลบค่า Null
- ลบข้อมูลซ้ำ
- ปรับรูปแบบข้อความ
- แปลงชนิดข้อมูล (Data Type)

### 6️⃣ Gold Layer (Business Data)

สร้างข้อมูลสำหรับใช้งานจริง:
- จำนวน provider ทั้งหมด
- จำนวน provider ที่ active
- การแจกแจงสถานะ (status breakdown)

ใช้สำหรับ Dashboard, Analytics และ Machine Learning

### 7️⃣ Serving Layer
- Dashboard (Metabase / Superset)
- Machine Learning Model

---
<img width="917" height="284" alt="image" src="https://github.com/user-attachments/assets/06fa2119-9d96-48af-a48f-00c6e323f4f1" />

---

## ⚙️ Airflow DAG

### 🔹 DAG หลัก

```
nyc_tlc_pipeline
```

### 🔁 ลำดับการทำงาน

```
start → trigger_ingestion → trigger_quality_check → trigger_silver → trigger_gold → end
```

### 📂 DAG ย่อย

| DAG | หน้าที่ |
|-----|---------|
| `nyc_tlc_dsp_ingestion` | ดึงข้อมูลจาก API → บันทึกลง Bronze |
| `nyc_tlc_quality_check` | ตรวจสอบคุณภาพข้อมูล แยก flow ผ่าน/ไม่ผ่าน |
| `nyc_tlc_silver` | ทำความสะอาดและแปลงข้อมูล |
| `nyc_tlc_gold` | สร้างข้อมูลสรุป (metrics) |

---

## 🗂️ Data Storage

ข้อมูลทุก layer ถูกเก็บใน container ขณะรัน ไม่ได้ commit ขึ้น repo เพราะเป็น runtime data

| Layer | Path ใน Container | สร้างโดย |
|-------|-------------------|---------|
| Bronze | `/opt/airflow/data/bronze/nyc_tlc_dsp_raw.json` | ingestion DAG |
| Silver | `/opt/airflow/data/silver/nyc_tlc_dsp_cleaned.json` | silver DAG |
| Gold | `/opt/airflow/data/gold/nyc_tlc_dsp_metrics.json` | gold DAG |

---

## 🛠️ เทคโนโลยีที่ใช้

| ส่วนประกอบ | เทคโนโลยี |
|------------|-----------|
| Orchestration | Apache Airflow 2.9.1 |
| ภาษา | Python 3.11 |
| Container | Docker Desktop |
| Database | PostgreSQL 13 |
| Queue | Redis 7.2 |
| Storage | Local File System (ใน container) |
| Data Source | NYC Open Data API |

---

## 📁 โครงสร้างโปรเจค

```
nyc_tlc_pipeline/
├── dags/
│   ├── nyc_tlc_pipeline.py         # Main DAG
│   ├── nyc_tlc_ingestion.py        # Bronze
│   ├── nyc_tlc_quality_check.py    # QC
│   ├── nyc_tlc_silver.py           # Silver
│   └── nyc_tlc_gold.py             # Gold
├── docker-compose.yaml
├── .env
└── README.md
```

> **หมายเหตุ:** ไม่มี folder `data/` ใน repo เพราะ Bronze / Silver / Gold  
> ถูกสร้างอัตโนมัติใน container ตอนรัน pipeline

---

## ▶️ วิธีการรันโปรเจค

### 1. เริ่ม Airflow

```bash
docker compose up -d
```

### 2. เข้าใช้งาน Airflow

```
http://localhost:8080
```

| | |
|---|---|
| Username | airflow |
| Password | airflow |

### 3. รัน Pipeline

1. เปิด DAG `nyc_tlc_pipeline`
2. กด **Trigger DAG** มุมขวาบน
3. ดูการทำงานใน **Graph view**
4. เมื่อทุก task เป็นสีเขียว = Pipeline สำเร็จ ✅

### 4. หยุด Airflow

```bash
docker compose down
```

---

## 🚀 จุดเด่นของโปรเจค

- Batch Data Pipeline ครบ End-to-End
- Medallion Architecture (Bronze / Silver / Gold)
- มี Data Quality Layer แยกชัดเจน
- ใช้ Apache Airflow ควบคุม workflow
- รันด้วย Docker ได้เลย ไม่ต้องติดตั้งอะไรเพิ่ม

---

## 📌 แนวทางพัฒนาต่อ

- [ ] เชื่อมต่อ Dashboard (Metabase / Superset)
- [ ] เพิ่มระบบแจ้งเตือน (Email / Slack) เมื่อ QC fail
- [ ] ย้าย Storage ไป Cloud (S3 / GCS)
- [ ] เพิ่ม Machine Learning Model สำหรับ Provider Compliance
- [ ] เพิ่ม Data Lineage tracking (OpenLineage)

---
