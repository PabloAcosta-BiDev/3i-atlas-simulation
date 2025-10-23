# 3I Atlas Simulation

Simulación 3D del cometa **3I/ATLAS** utilizando datos de ephemerides del Minor Planet Center (MPC) y NASA/JPL.

## Objetivos

- Simular la trayectoria hiperbólica del cometa en 3D (Three.js / React).
- Generar datos de distancia a la Tierra, días y horas con mejor visibilidad.
- Crear un dashboard sencillo en Power BI para visualizar resultados y métricas.
- Permitir ejecución programada de DAGs para actualización automática de datos (opcional: Apache Airflow).

## Estructura de Carpetas

- `backend/` → Código Python y FastAPI
- `web/` → Frontend 3D
- `airflow/` → DAGs programados
- `data/` → Ephemerides, CSV/JSON
- `notebooks/` → Pruebas y análisis
- `docs/` → Documentación y diagramas
- `.github/workflows/` → CI/CD con GitHub Actions

## Licencia

MIT
