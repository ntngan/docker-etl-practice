from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime 
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.etl_script import extract, transform, load

default_args = {
    'owner': 'ntngan',
    'start_date': datetime(2024,11,18),
    'retries': 1
}

with DAG(
    dag_id='etl_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract,
        dag=dag,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform,
        dag=dag,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load,
        dag=dag,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
