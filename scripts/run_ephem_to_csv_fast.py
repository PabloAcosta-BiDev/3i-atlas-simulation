#!/usr/bin/env python3
"""Quick runner to fetch ephemeris vectors and write CSV without Airflow.
Useful for testing and to produce CSVs immediately for Power BI ingestion.
"""
import os
import sys
import requests
import pandas as pd
from pathlib import Path

API_URL = os.getenv('EPHEM_API_URL', 'https://threei-atlas-simulation-1.onrender.com/api/vectors')
# Comma-separated list of delta locations to fetch (defaults to the three requested)
DELTA_LOCATIONS = [s.strip() for s in os.getenv('EPHEM_DELTA_LOCATIONS', 'cancun,huejotzingo,tijuana').split(',') if s.strip()]

OUTPUT_DIR = os.getenv('EPHEM_OUTPUT_DIR', os.path.join(os.path.dirname(__file__), '..', 'data', 'output'))
OUTPUT_DIR = str(Path(OUTPUT_DIR).resolve())
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'ephem_vectors.csv')

os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_and_write():
    print('Fetching data from', API_URL)
    resp = requests.get(API_URL, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # Convert to DataFrame
    try:
        df = pd.DataFrame(data)
    except Exception as e:
        print('Error converting JSON to DataFrame:', e)
        sys.exit(2)

    # Normalize numeric columns and add Distance_km if needed
    if 'Distance_AU' in df.columns and 'Distance_km' not in df.columns:
        df['Distance_km'] = pd.to_numeric(df['Distance_AU'], errors='coerce') * 149597870.7

    df.to_csv(OUTPUT_FILE, index=False)
    print('Wrote', OUTPUT_FILE)

    # Also fetch delta endpoints for specific locations and write CSVs
    # Determine base API URL (strip path after /api)
    try:
        if '/api/' in API_URL:
            base = API_URL.split('/api/')[0]
        else:
            base = API_URL.rsplit('/', 1)[0]
    except Exception:
        base = API_URL

    for loc in DELTA_LOCATIONS:
        loc = loc.lower()
        delta_url = f"{base}/api/deltas/{loc}"
        out_file = os.path.join(OUTPUT_DIR, f'ephem_delta_{loc}.csv')
        try:
            print('Fetching delta for', loc, 'from', delta_url)
            r = requests.get(delta_url, timeout=30)
            r.raise_for_status()
            j = r.json()
            # If the JSON is an object with nested structure, try to find array data
            if isinstance(j, dict) and 'data' in j and isinstance(j['data'], list):
                df_delta = pd.DataFrame(j['data'])
            elif isinstance(j, list):
                df_delta = pd.DataFrame(j)
            else:
                # fallback: try to coerce dict values to rows
                try:
                    df_delta = pd.DataFrame(j)
                except Exception as e:
                    print('Could not convert delta JSON to DataFrame for', loc, e)
                    continue

            df_delta.to_csv(out_file, index=False)
            print('Wrote', out_file)
        except Exception as e:
            print('Failed to fetch or write delta for', loc, e)


if __name__ == '__main__':
    try:
        fetch_and_write()
    except Exception as exc:
        print('Error:', exc)
        sys.exit(1)
