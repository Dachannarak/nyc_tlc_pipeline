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

def transform_to_gold():
    input_path = "/opt/airflow/data/silver/nyc_tlc_dsp_cleaned.json"
    output_path = "/opt/airflow/data/gold/nyc_tlc_dsp_metrics.json"

    # เช็คว่าไฟล์ silver มีอยู่ไหม
    if not os.path.exists(input_path):
        raise Exception("❌ ไม่พบไฟล์ silver data")

    with open(input_path, 'r') as f:
        data = json.load(f)

    # สร้าง folder gold
    os.makedirs("/opt/airflow/data/gold", exist_ok=True)

    # Aggregate metrics
    total_providers = len(data)
    
    # นับตาม status
    status_count = {}
    for row in data:
        status = row.get('status', 'UNKNOWN')
        status_count[status] = status_count.get(status, 0) + 1

    # Active providers
    active_providers = [
        row for row in data 
        if row.get('status') == 'ACTIVE'
    ]

    gold_data = {
        'summary': {
            'total_providers': total_providers,
            'active_providers': len(active_providers),
            'status_breakdown': status_count,
            'generated_at': datetime.utcnow().isoformat(),
        },
        'active_provider_list': active_providers,
    }

    with open(output_path, 'w') as f:
        json.dump(gold_data, f, indent=2)

    print(f"✅ Silver: {total_providers} records")
    print(f"✅ Active providers: {len(active_providers)}")
    print(f"✅ Status breakdown: {status_count}")
    print(f"✅ บันทึกไฟล์ที่ {output_path}")

with DAG(
    dag_id='nyc_tlc_gold',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['nyc_tlc', 'gold', 'aggregate'],
) as dag:

    gold_task = PythonOperator(
        task_id='transform_to_gold',
        python_callable=transform_to_gold,
    )