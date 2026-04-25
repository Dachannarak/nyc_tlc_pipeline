from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

def transform_to_silver():
    input_path = "/opt/airflow/data/bronze/nyc_tlc_dsp_raw.json"
    output_path = "/opt/airflow/data/silver/nyc_tlc_dsp_cleaned.json"

    # เช็คว่าไฟล์ bronze มีอยู่ไหม
    if not os.path.exists(input_path):
        raise Exception("❌ ไม่พบไฟล์ bronze data")

    with open(input_path, 'r') as f:
        data = json.load(f)

    cleaned = []
    seen = set()

    for row in data:
        # Standardize — strip whitespace
        dsp_name = row.get('dsp_name', '').strip().title()
        license_number = row.get('license_number', '').strip().upper()
        status = row.get('status', '').strip().upper()
        last_updated = row.get('last_updated_date', '').strip()

        # Skip null dsp_name
        if not dsp_name:
            continue

        # Skip duplicate
        if dsp_name in seen:
            continue
        seen.add(dsp_name)

        cleaned.append({
            'dsp_name': dsp_name,
            'license_number': license_number,
            'status': status,
            'last_updated': last_updated,
            'processed_at': datetime.utcnow().isoformat(),
        })

    # สร้าง folder silver
    os.makedirs("/opt/airflow/data/silver", exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Bronze: {len(data)} records")
    print(f"✅ Silver: {len(cleaned)} records หลัง clean")
    print(f"✅ บันทึกไฟล์ที่ {output_path}")

with DAG(
    dag_id='nyc_tlc_silver',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['nyc_tlc', 'silver', 'transform'],
) as dag:

    transform_task = PythonOperator(
        task_id='transform_to_silver',
        python_callable=transform_to_silver,
    )