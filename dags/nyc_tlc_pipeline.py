from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='nyc_tlc_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['nyc_tlc', 'pipeline', 'main'],
) as dag:

    start = EmptyOperator(task_id='start')

    trigger_ingestion = TriggerDagRunOperator(
        task_id='trigger_ingestion',
        trigger_dag_id='nyc_tlc_dsp_ingestion',
        wait_for_completion=True,
        poke_interval=30,
    )

    trigger_quality = TriggerDagRunOperator(
        task_id='trigger_quality_check',
        trigger_dag_id='nyc_tlc_quality_check',
        wait_for_completion=True,
        poke_interval=30,
    )

    trigger_silver = TriggerDagRunOperator(
        task_id='trigger_silver',
        trigger_dag_id='nyc_tlc_silver',
        wait_for_completion=True,
        poke_interval=30,
    )

    trigger_gold = TriggerDagRunOperator(
        task_id='trigger_gold',
        trigger_dag_id='nyc_tlc_gold',
        wait_for_completion=True,
        poke_interval=30,
    )

    end = EmptyOperator(task_id='end')

    start >> trigger_ingestion >> trigger_quality >> trigger_silver >> trigger_gold >> end