# check_ephem_data.py
import json
import os
import math

# ------------------------------
# 1️⃣ Verificar existencia del archivo
# ------------------------------
ruta = "data/ephem_distance.json"
if not os.path.exists(ruta):
    raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
print(f"✅ Archivo encontrado: {ruta}")

# ------------------------------
# 2️⃣ Cargar datos JSON
# ------------------------------
with open(ruta, "r") as f:
    data = json.load(f)

print(f"✅ Archivo cargado correctamente, registros encontrados: {len(data)}")

# ------------------------------
# 3️⃣ Verificar campos esperados
# ------------------------------
campos_esperados = [
    "Obj", "JD_TT", "X", "Y", "Z", "X'", "Y'", "Z'", "Distance_AU", "Distance_km"
]

faltantes = []
for i, rec in enumerate(data):
    for campo in campos_esperados:
        if campo not in rec:
            faltantes.append((i, campo))

if faltantes:
    print(f"❌ Campos faltantes encontrados: {faltantes}")
else:
    print("✅ Todos los registros contienen los campos requeridos")

# ------------------------------
# 4️⃣ Verificar que las distancias sean numéricas
# ------------------------------
errores = []
for i, rec in enumerate(data):
    try:
        au = float(rec["Distance_AU"])
        km = float(rec["Distance_km"])
        if math.isnan(au) or math.isnan(km):
            errores.append(i)
    except:
        errores.append(i)

if errores:
    print(f"❌ Registros con valores no numéricos o NaN en distancias: {errores}")
else:
    print("✅ Todas las distancias son valores numéricos válidos")

# ------------------------------
# 5️⃣ Verificar consistencia AU ↔ km
# ------------------------------
AU_TO_KM = 149597870.7
inconsistentes = []

for i, rec in enumerate(data):
    km_calc = float(rec["Distance_AU"]) * AU_TO_KM
    km_real = float(rec["Distance_km"])
    if abs(km_calc - km_real) > 1000:  # tolerancia de ±1 km
        inconsistentes.append(i)

if inconsistentes:
    print(f"❌ Registros con inconsistencias AU↔km: {inconsistentes}")
else:
    print("✅ Todas las distancias AU↔km son consistentes")

# ------------------------------
# 6️⃣ Resumen final
# ------------------------------
print("\n📊 Resumen final:")
print(f"Total registros: {len(data)}")
print(f"Registros con campos faltantes: {len(faltantes)}")
print(f"Registros con distancias no numéricas: {len(errores)}")
print(f"Registros con inconsistencias AU↔km: {len(inconsistentes)}")
print("✅ Comprobación completada")
