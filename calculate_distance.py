import json
from astropy import units as u
import numpy as np

# Ruta al archivo de vectores
input_file = "data/ephem_vectors.json"
output_file = "data/ephem_distance.json"

# Cargar vectores del JSON
with open(input_file, "r") as f:
    vectors = json.load(f)

# Supongamos que el origen para calcular distancias es el Sol en (0,0,0)
origin = np.array([0.0, 0.0, 0.0]) * u.AU

# Inicializamos variables para distancia mínima
min_distance = None
closest_jd = None

# Recorremos los vectores y calculamos distancia
for rec in vectors:
    x = float(rec["X"])
    y = float(rec["Y"])
    z = float(rec["Z"])
    pos = np.array([x, y, z]) * u.AU
    
    delta = pos - origin
    dist_au = np.linalg.norm(delta.value)  # Distancia en AU
    dist_km = (dist_au * u.AU).to(u.km).value  # Convertir a km

    rec["Distance_AU"] = dist_au
    rec["Distance_km"] = dist_km

    # Actualizamos mínima
    if (min_distance is None) or (dist_au < min_distance):
        min_distance = dist_au
        closest_jd = rec["JD_TT"]

# Guardar resultados
with open(output_file, "w") as f:
    json.dump(vectors, f, indent=2)

print(f"✅ Archivo generado: {output_file}")
print(f"Distancia mínima: {min_distance:.6f} AU / {dist_km:.0f} km")
print(f"JD_TT aproximación más cercana: {closest_jd}")
