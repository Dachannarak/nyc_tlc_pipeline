from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import json
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

def check_data_quality():
    input_path = "/opt/airflow/data/bronze/nyc_tlc_dsp_raw.json"
    
    # เช็คว่าไฟล์มีอยู่ไหม
    if not os.path.exists(input_path):
        raise Exception("❌ ไม่พบไฟล์ bronze data")
    
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    errors = []
    
    # เช็ค 1 — มีข้อมูลไหม
    if len(data) == 0:
        errors.append("❌ ไม่มีข้อมูลเลย")
    else:
        print(f"✅ มีข้อมูล {len(data)} records")
    
    # เช็ค 2 — Null check
    null_count = sum(1 for row in data if not row.get('dsp_name'))
    if null_count > 0:
        errors.append(f"❌ พบ null ใน dsp_name จำนวน {null_count} rows")
    else:
        print("✅ ไม่พบ null ใน dsp_name")
    
    # เช็ค 3 — Duplicate check
    names = [row.get('dsp_name') for row in data]
    duplicates = len(names) - len(set(names))
    if duplicates > 0:
        print(f"⚠️ พบ duplicate {duplicates} rows")
    else:
        print("✅ ไม่พบ duplicate")
    
    if errors:
        raise Exception("\n".join(errors))
    
    print("✅ Data Quality Check ผ่านทั้งหมด")
    return "passed"

def branch_quality(**context):
    try:
        check_data_quality()
        return "quality_passed"
    except Exception as e:
        print(f"Quality check failed: {e}")
        return "quality_failed"

with DAG(
    dag_id='nyc_tlc_quality_check',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['nyc_tlc', 'quality', 'bronze'],
) as dag:

    start = EmptyOperator(task_id='start')

    quality_check = BranchPythonOperator(
        task_id='branch_quality_check',
        python_callable=branch_quality,
    )

    passed = EmptyOperator(task_id='quality_passed')
    failed = EmptyOperator(task_id='quality_failed')

    start >> quality_check >> [passed, failed]