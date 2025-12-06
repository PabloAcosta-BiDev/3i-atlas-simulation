# 3I/ATLAS Simulation

Interactive 3D visualization of **3I/ATLAS** comet trajectory using ephemeris data from the Minor Planet Center (MPC) and NASA/JPL Horizons.

![3I/ATLAS Visualization](https://img.shields.io/badge/Status-Live-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue) ![Three.js](https://img.shields.io/badge/Three.js-v0.158.0-black) ![Python](https://img.shields.io/badge/Python-3.11+-blue)

## 🌌 Features

- **Real-time 3D Visualization** - Interactive solar system with comet trajectory using Three.js
- **Multi-Observatory Support** - Data for 4 international observation sites
- **Power BI Dashboard** - Embedded analytics with observability metrics
- **Serverless Architecture** - Deployed on Vercel with zero infrastructure management
- **Scientific Accuracy** - Pre-computed ephemeris data from authoritative sources

## 🚀 Live Demo

**[View Live Simulation](https://3i-atlas-simulation.vercel.app/)


## 📡 API Endpoints

All endpoints available at `https://your-deployment.vercel.app/api/`

| Endpoint | Description |
|----------|-------------|
| `GET /api/vectors` | Heliocentric state vectors (X, Y, Z, VX, VY, VZ) |
| `GET /api/planets` | All planetary positions |
| `GET /api/planets/{name}` | Specific planet ephemeris |
| `GET /api/deltas/{location}` | Observatory-specific topocentric data |
| `GET /api/orbits` | Keplerian orbital elements |

### Example Response
```json
GET /api/vectors
[
  {
    "JD_TT": 2460605.5,
    "ISO": "2025-10-23 00:00:00.000",
    "X": 1.2345,
    "Y": -0.8765,
    "Z": 0.4321,
    "VX": 0.012,
    "VY": 0.034,
    "VZ": -0.007,
    "r": 1.543,
    "delta": 0.876
  }
]
```

## 🌍 Observatory Locations

- **Paranal Observatory** - Chile (ESO)
- **San Pedro Mártir** - México
- **La Palma** - Spain (Roque de los Muchachos)
- **Mauna Kea** - Hawaii

## 🔧 Local Development

### Prerequisites
- Python 3.11+
- Modern web browser with WebGL support

### Setup
```bash
# Clone repository
git clone https://github.com/PabloAcosta-BiDev/3i-atlas-simulation.git
cd 3i-atlas-simulation

# Run local API server
python local_server.py
```

Then open `web/index-modern.html` in your browser. The frontend will automatically connect to `http://localhost:8000`.

## 📊 Power BI Integration

The project includes an embedded Power BI dashboard with:
- Observability index calculations
- Country-based filtering
- Date range slicing
- Velocity vs. distance analysis (Kepler's laws)

## 🎓 Scientific Background

**3I/ATLAS** is an interstellar comet discovered in 2024. This simulation visualizes:
- Hyperbolic trajectory through the solar system
- Heliocentric and topocentric positions
- Observable windows from ground-based observatories
- Velocity changes as function of solar distance

## 📖 Documentation

- [Architecture Overview](3iASIM_Arch.md) - System design and components

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🔗 Links

- **Data Sources**: [Minor Planet Center](https://www.minorplanetcenter.net/), [JPL Horizons](https://ssd.jpl.nasa.gov/horizons/)
- **Three.js**: [threejs.org](https://threejs.org/)
- **Vercel**: [vercel.com](https://vercel.com)

---

**Developed by**: Pablo Acosta  
**Last Updated**: December 2025
