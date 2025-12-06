# 3I/ATLAS Simulation - Architecture

## System Architecture

```mermaid
graph TB
    %% User Interface Layer
    USER["👤 Usuario"]
    
    %% Frontend Layer
    FRONTEND["Frontend Web<br/>(Three.js + Vanilla JS)"]
    DASHBOARD["Power BI Dashboard<br/>(Embedded iframe)"]
    
    %% Backend Layer
    API["Vercel Serverless API<br/>(api/index.py)"]
    
    %% Data Layer
    VECTORS["📁 ephem_vectors_fetched.json<br/>(Comet trajectory)"]
    PLANETS["📁 data/planets/*.json<br/>(Planetary positions)"]
    DELTAS["📁 ephem_delta_*.json<br/>(Observatory data)"]
    ORBITS["📁 elemental_orbits.json<br/>(Orbital elements)"]
    
    %% Development/Documentation
    SCRIPTS["backend/Scripts/<br/>(Data generation docs)"]
    
    %% Hosting
    VERCEL["Vercel Hosting<br/>(Production)"]
    
    %% User interactions
    USER --> FRONTEND
    USER --> DASHBOARD
    
    %% Frontend to Backend
    FRONTEND --> API
    
    %% API to Data
    API --> VECTORS
    API --> PLANETS
    API --> DELTAS
    API --> ORBITS
    
    %% Deployment
    VERCEL --> FRONTEND
    VERCEL --> API
    
    %% Documentation reference (one-way, not executed)
    SCRIPTS -.->|"documents how to generate"| VECTORS
    SCRIPTS -.->|"documents how to generate"| PLANETS
    
    %% Data flow to visualization
    VECTORS --> FRONTEND
    PLANETS --> FRONTEND
    DELTAS --> FRONTEND
    
    style USER fill:#e1f5ff
    style FRONTEND fill:#b3e5fc
    style DASHBOARD fill:#b3e5fc
    style API fill:#81c784
    style VECTORS fill:#fff9c4
    style PLANETS fill:#fff9c4
    style DELTAS fill:#fff9c4
    style ORBITS fill:#fff9c4
    style SCRIPTS fill:#ffccbc
    style VERCEL fill:#ce93d8
```

## Technology Stack

### Frontend
- **Three.js** (v0.158.0) - 3D visualization engine
- **Vanilla JavaScript** - No framework dependencies
- **HTML5/CSS3** - Modern responsive design
- **Embedded Power BI** - Analytics dashboard (iframe)

### Backend
- **Vercel Serverless Functions** - Python HTTP handlers
- **Python 3.11+** - Runtime environment
- **Standard Library Only** - No external dependencies in production

### Data Storage
- **Static JSON Files** - Pre-computed ephemeris data
- **GitHub Repository** - Version control and storage
- **Vercel CDN** - Fast global data delivery

### Hosting & Deployment
- **Vercel** - Serverless hosting platform
- **Custom Domain Support** - Production-ready URLs
- **Automatic HTTPS** - SSL certificates included

## API Endpoints

| Endpoint | Method | Description | Data Source |
|----------|--------|-------------|-------------|
| `/api/vectors` | GET | Heliocentric state vectors of 3I/ATLAS | `ephem_vectors_fetched.json` |
| `/api/planets` | GET | All planetary positions (aggregated) | `data/planets/*.json` |
| `/api/planets/{name}` | GET | Specific planet position data | `data/planets/{name}.json` |
| `/api/deltas/{location}` | GET | Topocentric data for observatory | `ephem_delta_{location}.json` |
| `/api/orbits` | GET | Orbital elements | `elemental_orbits.json` |

## Data Files

### Core Ephemeris Data
- `ephem_vectors_fetched.json` - 3I/ATLAS heliocentric positions (X, Y, Z, VX, VY, VZ)
- `elemental_orbits.json` - Keplerian orbital elements

### Planetary Data (8 files)
- `data/planets/mercury.json` through `neptune.json`
- Format: `{"times": [...], "positions": [...]}`

### Observatory Data (4 locations)
- `ephem_delta_lapalma.json` - La Palma Observatory
- `ephem_delta_maunakea.json` - Mauna Kea Observatory
- `ephem_delta_paranal.json` - Paranal Observatory
- `ephem_delta_sanpedromartir.json` - San Pedro Mártir Observatory

## Development Documentation

### Data Generation Scripts (`backend/Scripts/`)
**Purpose**: Documentation of how original JSON data files were generated

- `generate_planet_ephem.py` - Logic for planetary position calculations
- `save_planet_ephem.py` - Script to generate planet JSON files
- `fetch_mpc_ephem.py` - MPC (Minor Planet Center) data fetching utilities

**Note**: These scripts are **not executed in production**. They serve as reference documentation showing the methodology used to create the static JSON files.
---
