from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import requests
import json

# Simple DAG to fetch JSON from the public API endpoints and write JSON files to disk.
# This keeps the example minimal for demonstrating Airflow → Power BI workflow.

# Configure via environment variables
# EPHEM_API_URL: default to the Render service
EPHEM_API_URL = os.getenv('EPHEM_API_URL', 'https://threei-atlas-simulation-1.onrender.com/api/vectors')
# Comma-separated list of delta locations to fetch (defaults to the three requested)
EPHEM_DELTA_LOCATIONS = [s.strip() for s in os.getenv('EPHEM_DELTA_LOCATIONS', 'cancun,huejotzingo,tijuana').split(',') if s.strip()]
OUTPUT_DIR = os.getenv('EPHEM_OUTPUT_DIR', os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'output'))

os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_vectors(**context):
    print('Fetching vectors from', EPHEM_API_URL)
    resp = requests.get(EPHEM_API_URL, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    out_file = os.path.join(OUTPUT_DIR, 'ephem_vectors.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Wrote', out_file)


def fetch_deltas(**context):
    # Derive base URL (strip trailing /api/... if present)
    api = EPHEM_API_URL
    base = api.split('/api/')[0] if '/api/' in api else api.rsplit('/', 1)[0]

    for loc in EPHEM_DELTA_LOCATIONS:
        loc = loc.lower()
        url = f"{base}/api/deltas/{loc}"
        try:
            print('Fetching delta for', loc, 'from', url)
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            j = r.json()
            out_file = os.path.join(OUTPUT_DIR, f'ephem_delta_{loc}.json')
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(j, f, ensure_ascii=False, indent=2)
            print('Wrote', out_file)
        except Exception as e:
            print('Failed to fetch delta for', loc, e)


with DAG(dag_id='ephem_to_json', start_date=datetime(2025, 11, 1), schedule_interval='@daily', catchup=False) as dag:
    task_fetch_vectors = PythonOperator(task_id='fetch_vectors', python_callable=fetch_vectors)
    task_fetch_deltas = PythonOperator(task_id='fetch_deltas', python_callable=fetch_deltas)

    task_fetch_vectors >> task_fetch_deltas
