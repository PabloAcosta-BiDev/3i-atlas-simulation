from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import requests
import pandas as pd

# Configure via environment variables
API_URL = os.getenv('EPHEM_API_URL', 'http://127.0.0.1:8000/api/vectors')
OUTPUT_DIR = os.getenv('EPHEM_OUTPUT_DIR', os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'output'))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'ephem_vectors.csv')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_and_transform(**context):
    print('Fetching data from', API_URL)
    resp = requests.get(API_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Convert to DataFrame, normalize different possible shapes
    df = pd.DataFrame(data)

    # Example transforms: ensure numeric columns, compute distance_km if missing
    if 'Distance_AU' in df.columns and 'Distance_km' not in df.columns:
        df['Distance_km'] = pd.to_numeric(df['Distance_AU'], errors='coerce') * 149597870.7

    # Minimal clean: drop huge nested objects
    df.to_csv(OUTPUT_FILE, index=False)
    print('Wrote', OUTPUT_FILE)


def noop(**context):
    print('No-op task for testing')

with DAG(dag_id='ephem_to_csv', start_date=datetime(2025, 11, 1), schedule_interval='@daily', catchup=False) as dag:
    task_fetch = PythonOperator(task_id='fetch_and_transform', python_callable=fetch_and_transform)
    task_noop = PythonOperator(task_id='noop', python_callable=noop)

    task_fetch >> task_noop
