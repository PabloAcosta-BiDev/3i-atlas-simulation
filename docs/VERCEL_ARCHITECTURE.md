# 3I-ATLAS Simulation - Vercel Architecture

## 🚀 **NEW ARCHITECTURE OVERVIEW**

This project has been migrated from Render + Docker + Airflow to a **serverless Vercel + GitHub Actions** architecture for better performance, reliability, and zero cost.

### **Architecture Components:**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Pages  │ or │  Vercel Frontend │ -> │ Vercel API      │
│   (Frontend)    │    │   (Frontend)     │    │ (Serverless)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   JSON Data     │
                                                │  (Repository)   │
                                                └─────────────────┘
                                                         ▲
                                                         │
┌─────────────────────────────────────────────────────────────────┐
│              GitHub Actions (Every 60 days)                    │
│  • Fetches new data from Minor Planet Center (MPC)            │
│  • Appends 60 days of future ephemeris data                   │
│  • Commits updated JSONs back to repository                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 **PROJECT STRUCTURE**

```
3i-atlas-simulation/
├── 📂 api/                    # Vercel Serverless Functions
│   └── index.py              # Main API handler (all endpoints)
├── 📂 web/                    # Frontend
│   └── index-modern.html     # 3D visualization (auto-detects Vercel/localhost)
├── 📂 data/                   # Astronomical Data (JSON)
│   ├── ephem_vectors_fetched.json     # Heliocentric vectors
│   ├── ephem_delta_cancun.json       # Cancun observatory data
│   ├── ephem_delta_huejotzingo.json  # Huejotzingo observatory data
│   ├── ephem_delta_tijuana.json      # Tijuana observatory data
│   └── last_update.json              # Update metadata
├── 📂 scripts/                # Data Generation
│   └── update_data.py         # GitHub Actions script (MPC data fetching)
├── 📂 backend/                # Business Logic (referenced by Vercel)
│   ├── main.py               # Original FastAPI app (reference)
│   ├── services/             # Astronomical calculations
│   └── Scripts/              # MPC data fetchers
├── 📂 .github/workflows/      # CI/CD
│   └── update-ephemeris.yml  # 60-day automated data refresh
├── vercel.json               # Vercel configuration
├── requirements.txt          # Python dependencies (minimal)
└── .env.example             # Environment variables template
```

---

## 🔧 **DEPLOYMENT**

### **1. Vercel Backend Deployment:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod

# Your API will be available at:
# https://your-deployment.vercel.app/api/vectors
# https://your-deployment.vercel.app/api/deltas/cancun
```

### **2. Frontend Deployment:**
**Option A: Vercel Frontend**
```bash
vercel --prod
# Frontend: https://your-deployment.vercel.app/web/index-modern.html
```

**Option B: GitHub Pages**
1. Go to Repository Settings → Pages
2. Select Branch: `main`, Folder: `/web`
3. Frontend: https://username.github.io/3i-atlas-simulation/

### **3. GitHub Actions Setup:**
1. **No secrets required** (MPC data is public)
2. Workflow runs automatically every 60 days
3. Manual trigger available in Actions tab

---

## 🔌 **API ENDPOINTS**

All endpoints are available at `https://your-vercel-deployment.vercel.app/api/`

| Endpoint | Description |
|----------|-------------|
| `GET /api/status` | API status and last data update |
| `GET /api/vectors` | Heliocentric ephemeris vectors |
| `GET /api/deltas/cancun` | Cancun observatory data |
| `GET /api/deltas/huejotzingo` | Huejotzingo observatory data |
| `GET /api/deltas/tijuana` | Tijuana observatory data |
| `GET /api/orbits` | Orbital elements |
| `GET /api/planets` | Planet positions |
| `GET /api/planets/{name}` | Specific planet data |

---

## 📊 **POWER BI INTEGRATION**

1. **Data Source:** Point Power BI to Vercel API endpoints
   ```
   https://your-deployment.vercel.app/api/vectors
   https://your-deployment.vercel.app/api/deltas/cancun
   ```

2. **Benefits:**
   - ✅ No sleep/timeout (always-on Vercel)
   - ✅ Fast response times (serverless)
   - ✅ Auto-refreshed data (60-day cycle)
   - ✅ Free hosting (Vercel free tier)

---

## 🔄 **DATA PIPELINE**

### **Automated 60-Day Refresh:**
1. **GitHub Actions** triggers every 60 days
2. **Script** (`scripts/update_data.py`) fetches new data from Minor Planet Center
3. **Appends** 60 days of future data to existing JSONs
4. **Commits** updated data back to repository
5. **Vercel** automatically deploys updated data

### **Manual Data Update:**
```bash
# Local development
python scripts/update_data.py

# Or trigger GitHub Actions manually
# Go to Actions tab → "Update Ephemeris Data" → Run workflow
```

---

## 🏃‍♂️ **LOCAL DEVELOPMENT**

### **1. Setup:**
```bash
git clone https://github.com/PabloAcosta-BiDev/3i-atlas-simulation.git
cd 3i-atlas-simulation

# Install dependencies
pip install astroquery astropy numpy

# Run data update (optional)
python scripts/update_data.py
```

### **2. Test API locally:**
```bash
# Start development server
python -m http.server 8000

# Frontend will auto-detect localhost
# Open: http://localhost:8000/web/index-modern.html
```

### **3. Test Vercel functions locally:**
```bash
vercel dev
# API available at: http://localhost:3000/api/
```

---

## 🚧 **MIGRATION STATUS**

- ✅ **Vercel API** - Fully migrated and tested
- ✅ **GitHub Actions** - 60-day cron data pipeline
- ✅ **Frontend** - Auto-detection of environment
- ✅ **Data Pipeline** - MPC integration with append logic
- ✅ **Security** - No credentials in repository
- ✅ **Documentation** - Updated architecture docs
- ❌ **Legacy Cleanup** - Docker/Airflow files preserved for reference

---

## 📝 **NEXT STEPS**

1. **Deploy to Vercel** and test endpoints
2. **Configure GitHub Actions** secrets if needed
3. **Update Power BI** connections to Vercel URLs
4. **Test end-to-end flow** with real data
5. **Clean up legacy infrastructure** once validated

---

**Questions?** Contact the development team or check the repository issues.