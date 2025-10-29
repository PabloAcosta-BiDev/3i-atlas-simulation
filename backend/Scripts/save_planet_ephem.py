"""
Generate planet position JSONs using the same format as ephem_vectors_fetched.json
but for each planet separately. Files will be saved in data/planets/{name}.json
"""
import os
import json
from backend.Scripts.generate_planet_ephem import generate_planet_ephem

# Use the same epoch range as the comet data
START_DATE = "2025-10-23T00:00:00"
END_DATE = "2025-10-29T00:00:00"

# Generate for all planets with hourly steps
data = generate_planet_ephem(
    start=START_DATE,
    end=END_DATE,
    step_minutes=60,  # hourly steps like the comet data
    bodies=["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
)

# Save individual JSON files
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_dir = os.path.join(PROJECT_ROOT, "data", "planets")
os.makedirs(data_dir, exist_ok=True)

for name, positions in data["bodies"].items():
    fname = os.path.join(data_dir, f"{name}.json")
    planet_data = {
        "times": data["times"],
        "positions": positions
    }
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(planet_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {fname}")