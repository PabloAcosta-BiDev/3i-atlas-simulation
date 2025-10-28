from backend.Scripts.generate_planet_ephem import generate_planet_ephem
import json

try:
    result = generate_planet_ephem('2025-10-28T00:00:00')
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()