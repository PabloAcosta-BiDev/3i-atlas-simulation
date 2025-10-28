"""
Uso:
(venv) $ python fetch_mpc_ephem.py
Ajusta las variables abajo (TARGET, START, STEP, NUMBER, LOCATIONS)
"""
from astroquery.mpc import MPC
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation, Angle
from astropy.units import Quantity
import json
import os

# --- CONFIGURAR ---
TARGET = "0003I"   # o "3I/ATLAS" según cómo lo acepte MPC
START = "2025-10-23"   # UTC date string
STEP = '1h'            # intervalo: '1h', '10m', '30m', '1d', etc.
NUMBER_VECT = 1440     # <= 1441 (puntos para vectores heliocéntricos)
NUMBER_DELTA = None    # si None, usa default de MPC; si quieres específico: 49, 100, etc.
OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

# Locations: (lon east, lat, alt). MPC acepta longitud este; usamos strings legibles por Angle
LOCATIONS = {
    "huejotzingo": ("-98.4073988d", "19.158971d", "2260m"),
    "tijuana": ("-117.060556d", "32.514947d", "40m"),
    "cancun": ("-86.8475d", "21.1619d", "10m")
}

def table_to_jsonlist(tab, heliocentric=False, include_jd=True):
    """Convierte astropy.table.Table a lista de dicts JSON serializables.
       heliocentric True -> espera columnas X,Y,Z and X',Y',Z' (con JD en lugar de Date)
    """
    out = []
    for row in tab:
        rec = {}
        
        # Date: buscar columna de fecha (puede ser 'Date', 'JD', 'MJD', etc.)
        date_col = None
        for possible_col in ['Date', 'JD', 'MJD', 'date', 'Epoch']:
            if possible_col in tab.colnames:
                date_col = possible_col
                break
        
        if date_col:
            try:
                t = Time(row[date_col], format='jd' if date_col in ['JD', 'MJD'] else None)
                rec['JD_TT'] = float(t.tt.jd) if hasattr(t, 'tt') else float(t.jd)
                rec['ISO'] = t.iso
            except Exception as e:
                rec['Date'] = str(row[date_col])

        # If heliocentric, convert vector columns (they come as Quantities)
        if heliocentric:
            # columnas típicas: 'X','Y','Z','X\'','Y\'','Z\''
            for k in ('X','Y','Z',"X'","Y'","Z'"):
                if k in tab.colnames:
                    v = row[k]
                    try:
                        # if Quantity
                        val = float(v.value) if hasattr(v, 'value') else float(v)
                    except Exception:
                        val = v
                    rec[k] = val
            # distancia heliocéntrica (norm)
            try:
                import numpy as _np
                X = float(rec['X']); Y = float(rec['Y']); Z = float(rec['Z'])
                dist_au = (_np.sqrt(X*X + Y*Y + Z*Z))
                rec['Distance_AU'] = float(dist_au)
                rec['Distance_km'] = float(dist_au * u.AU.to(u.km))
            except Exception:
                pass
        else:
            # equatorial/topocentric columns: RA/Dec/Delta/r/Azimuth/Altitude/Phase/Moon...
            # Iterate over columns and convert Quantity -> value
            for col in tab.colnames:
                if col == date_col:
                    continue  # ya procesamos la fecha arriba
                val = row[col]
                if hasattr(val, 'unit'):
                    # Quantity: use .value
                    try:
                        rec[col] = float(val.value) if val.shape == () else list(val.value)
                    except Exception:
                        # sometimes Angle columns -> to_string
                        try:
                            rec[col] = str(val)
                        except Exception:
                            rec[col] = None
                else:
                    # plain python type
                    rec[col] = val if (isinstance(val, (str, int, float))) else str(val)
        out.append(rec)
    return out

def fetch_vectors():
    print("Fetching heliocentric vectors...")
    
    # Convertir STEP a Quantity si es string
    step_qty = Quantity(STEP) if isinstance(STEP, str) else STEP
    
    tab = MPC.get_ephemeris(TARGET, start=START, step=step_qty, number=NUMBER_VECT, 
                           eph_type='heliocentric', cache=False)
    lst = table_to_jsonlist(tab, heliocentric=True)
    outfn = os.path.join(OUT_DIR, "ephem_vectors_fetched.json")
    with open(outfn, "w", encoding="utf-8") as f:
        json.dump(lst, f, indent=2, ensure_ascii=False)
    print(f"Saved: {outfn} (records: {len(lst)})")

def fetch_deltas():
    # Convertir STEP a Quantity si es string
    step_qty = Quantity(STEP) if isinstance(STEP, str) else STEP
    
    for name, coords in LOCATIONS.items():
        print(f"Fetching topocentric ephemeris for {name}...")
        loc = (coords[0], coords[1], coords[2])
        
        tab = MPC.get_ephemeris(TARGET, location=loc, start=START, step=step_qty, 
                               number=NUMBER_DELTA, cache=False)
        lst = table_to_jsonlist(tab, heliocentric=False)
        
        # add metadata fields for location and UTC offset
        for rec in lst:
            rec['Location'] = name
            rec['UTC_offset'] = -6 if name == 'huejotzingo' else (-7 if name=='tijuana' else -5)
        
        outfn = os.path.join(OUT_DIR, f"ephem_delta_{name}.json")
        with open(outfn, "w", encoding="utf-8") as f:
            json.dump(lst, f, indent=2, ensure_ascii=False)
        print(f"Saved: {outfn} (records: {len(lst)})")

if __name__ == "__main__":
    # Opcional: limpia cache si quieres datos frescos
    # MPC.clear_cache()
    
    print(f"Fetching ephemeris for {TARGET}")
    print(f"Start: {START}, Step: {STEP}")
    print("-" * 50)
    
    fetch_vectors()
    fetch_deltas()
    
    print("-" * 50)
    print("Done! Check the 'data' folder for output files.")