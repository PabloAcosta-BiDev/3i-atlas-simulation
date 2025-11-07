Airflow quickstart (Docker Compose)

This repo includes a minimal `docker-compose.override.yml` that mounts the
local `airflow/dags`, `scripts` and `data/output` into the official Apache
Airflow Docker Quickstart stack. Follow these steps on Windows PowerShell.

1) Download the official Airflow docker-compose.yaml into this repo root

```powershell
Invoke-WebRequest -Uri "https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml" -OutFile "docker-compose.yaml"
```

2) Confirm the override file is present (it was added to the repo):

```powershell
Get-ChildItem -Path . -Filter "docker-compose.override.yml"
```

3) (Optional) Edit `docker-compose.override.yml` to set environment variables
for your environment (for example EPHEM_API_URL or EPHEM_DELTA_LOCATIONS).

4) Initialize the Airflow environment (this creates DB, users and installs
requirements present in the image):

```powershell
# initialize DB and images
docker compose up airflow-init
```

5) Start the stack (detached):

```powershell
docker compose up -d
```

6) Open the Airflow UI:

- http://localhost:8080
- default user: create one during `airflow init` step or use the web UI to sign in.

7) Find DAGs:

- `ephem_to_json` (fetches JSON from the API and writes into `data/output`)
- `run_ephem_script` (calls `scripts/run_ephem_to_csv_fast.py`) — demonstrate running the script via Airflow

8) Trigger a DAG manually to test. After the run, check `data/output` locally for
new files such as `ephem_vectors.csv` and `ephem_delta_*.csv` or the corresponding JSONs.

Notes & troubleshooting
- The official Airflow quickstart uses images that include many dependencies; using Docker avoids installing Airflow locally and the need to compile native extensions (Rust/MSVC) on Windows.
- If you need extra Python packages inside the worker/webserver image, add a `requirements.txt` and extend the image in a custom Dockerfile, or modify the provided quickstart according to Airflow docs.
- If the DAGs don't show up, check the logs of `airflow-webserver` and ensure the `./airflow/dags` path is mounted correctly.

If you want, I can also create a small `docker-compose.override.requirements.yml` and a Dockerfile that installs `requests`/`pandas` into the image so the script runs cleanly inside the container.