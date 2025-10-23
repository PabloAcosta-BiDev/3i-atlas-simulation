```mermaid
graph LR
    %% Nodo central
    BACKEND["Backend Científico (FastAPI / Procesamiento)"]

    %% Componentes alrededor del centro
    AIRFLOW["AIRFLOW: DAGs (Fetch / Propagate / Publish)"]
    MPEC["MPEC / MPC Service"]
    PROCESS["Procesamiento: Poliastro / Skyfield / Transformaciones"]
    STORAGE["Almacenamiento: JSON / SQLite / Ephemerides"]
    FRONTEND["Front-end 3D (Three.js / React)"]
    POWERBI["Power BI Dashboard"]
    CI["CI/CD (GitHub Actions)"]
    DOCKER["Docker / Docker Compose"]
    GH_PAGES["GitHub Pages (Hosting Web)"]

    %% Conexiones hacia/desde el núcleo (bidireccionales donde aplica)
    AIRFLOW --> BACKEND
    MPEC --> AIRFLOW
    BACKEND --> PROCESS
    PROCESS --> STORAGE
    STORAGE --> BACKEND
    BACKEND --> FRONTEND
    BACKEND --> POWERBI
    CI --> DOCKER
    DOCKER --> BACKEND
    CI --> GH_PAGES
    GH_PAGES --> FRONTEND

    %% Opcionales / auxiliares
    STORAGE -->|export| FRONTEND
    STORAGE -->|csv/json| POWERBI
    AIRFLOW -->|writes| STORAGE
    MPEC -->|provides ephemeris| BACKEND
