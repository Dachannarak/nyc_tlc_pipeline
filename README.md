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
<img width="1019" height="228" alt="image" src="https://github.com/user-attachments/assets/24bf88fa-647c-4fde-a13a-d81c6fc56f16" />

---

## 🧱 Layer ของข้อมูล

### 1️⃣ Data Source

* ข้อมูลจาก NYC Open Data API (TLC DSP)
* รูปแบบ: JSON (REST API)
* อัปเดต: รายวัน (Batch)

---

### 2️⃣ Ingestion Layer

* ดึงข้อมูลจาก API
* บันทึกลง Bronze Layer

---

### 3️⃣ Bronze Layer (Raw Data)

* เก็บข้อมูลดิบ (ยังไม่ผ่านการประมวลผล)
* เก็บในรูปแบบ JSON
* มีการเก็บ metadata

---

### 4️⃣ Data Quality Layer

ตรวจสอบคุณภาพข้อมูลก่อนใช้งาน เช่น:

* ตรวจสอบค่า Null
* ตรวจสอบข้อมูลซ้ำ (Duplicate)
* ตรวจสอบจำนวนข้อมูล (Row count)

📌 ถ้าไม่ผ่าน → หยุด Pipeline
📌 ถ้าผ่าน → ส่งต่อไป Silver

---

### 5️⃣ Silver Layer (Cleaned Data)

ทำความสะอาดและแปลงข้อมูล:

* ลบค่า Null
* ลบข้อมูลซ้ำ
* ปรับรูปแบบข้อความ
* แปลงชนิดข้อมูล (Data Type)

---

### 6️⃣ Gold Layer (Business Data)

สร้างข้อมูลสำหรับใช้งานจริง เช่น:

* จำนวน provider ทั้งหมด
* จำนวน provider ที่ active
* การแจกแจงสถานะ (status breakdown)

ใช้สำหรับ:

* Dashboard
* Analytics
* Machine Learning

---

### 7️⃣ Serving Layer

นำข้อมูลไปใช้งาน:

* Dashboard (Metabase / Superset)
* Machine Learning Model

---

## ⚙️ Airflow DAG

### 🔹 DAG หลัก

```
nyc_tlc_pipeline
```

### 🔁 ลำดับการทำงาน

```
start
 → ingestion
 → quality_check
 → silver
 → gold
end
```

---

### 📂 DAG ย่อย

#### 1. ingestion

* ดึงข้อมูลจาก API
* บันทึกลง Bronze

#### 2. quality_check

* ตรวจสอบคุณภาพข้อมูล
* แยก flow (ผ่าน / ไม่ผ่าน)

#### 3. silver

* ทำความสะอาดและแปลงข้อมูล

#### 4. gold

* สร้างข้อมูลสรุป (metrics)

---

## 🛠️ เทคโนโลยีที่ใช้

| ส่วนประกอบ    | เทคโนโลยี         |
| ------------- | ----------------- |
| Orchestration | Apache Airflow    |
| ภาษา          | Python 3          |
| Container     | Docker            |
| Database      | PostgreSQL        |
| Queue         | Redis             |
| Storage       | Local File System |

---

## 📁 โครงสร้างโปรเจค

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

## ▶️ วิธีการรันโปรเจค

### 1. เริ่ม Airflow

```bash
docker compose up -d
```

---

### 2. เข้าใช้งาน Airflow

```
http://localhost:8080
```

Login:

* Username: airflow
* Password: airflow

---

### 3. รัน Pipeline

* เปิด DAG `nyc_tlc_pipeline`
* กด **Trigger DAG**
* ดูการทำงานใน Graph view

---

## 🚀 จุดเด่นของโปรเจค

* เป็น Batch Data Pipeline
* ใช้ Medallion Architecture (Bronze / Silver / Gold)
* มี Data Quality Layer แยกชัดเจน
* ใช้ Apache Airflow ควบคุม workflow
* เป็น End-to-End Pipeline

---

## 🎯 สรุป

โปรเจคนี้แสดงให้เห็นการออกแบบ Data Pipeline ที่สามารถใช้งานได้จริง โดยมีการจัดการข้อมูลเป็น layer และมีการตรวจสอบคุณภาพก่อนนำไปใช้งาน

---

## 📌 แนวทางพัฒนาต่อ

* เชื่อมต่อ Dashboard (Metabase / Superset)
* เพิ่มระบบแจ้งเตือน (Email / Slack)
* ย้าย Storage ไป Cloud (S3 / GCS)
* เพิ่ม Machine Learning Model
* เพิ่ม Data Lineage

---
