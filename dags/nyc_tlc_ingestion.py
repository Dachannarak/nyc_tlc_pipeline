from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

def ingest_nyc_tlc_dsp():
    url = "https://data.cityofnewyork.us/resource/2n4x-d97d.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ดึงข้อมูลสำเร็จ ได้ {len(data)} records")
        
        # สร้าง folder bronze ถ้ายังไม่มี
        os.makedirs("/opt/airflow/data/bronze", exist_ok=True)
        
        # บันทึกเป็น JSON
        import json
        output_path = "/opt/airflow/data/bronze/nyc_tlc_dsp_raw.json"
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ บันทึกไฟล์ที่ {output_path}")
    else:
        raise Exception(f"❌ ดึงข้อมูลไม่สำเร็จ status: {response.status_code}")

with DAG(
    dag_id='nyc_tlc_dsp_ingestion',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['nyc_tlc', 'bronze', 'ingestion'],
) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_nyc_tlc_dsp',
        python_callable=ingest_nyc_tlc_dsp,
    )