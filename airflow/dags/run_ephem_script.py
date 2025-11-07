from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

# This DAG wraps the local script `scripts/run_ephem_to_csv_fast.py` by importing
# its `fetch_and_write` function and invoking it via a PythonOperator. It is a
# minimal, demonstrative DAG to show Airflow executing the existing script.

with DAG(dag_id='run_ephem_script', start_date=datetime(2025, 11, 1), schedule_interval='@daily', catchup=False) as dag:
    def call_runner(**context):
        # Import here to ensure Airflow's environment has the repo on PYTHONPATH
        from scripts.run_ephem_to_csv_fast import fetch_and_write
        fetch_and_write()

    task_run = PythonOperator(task_id='run_ephem_runner', python_callable=call_runner)

    task_run
