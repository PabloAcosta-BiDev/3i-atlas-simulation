"""
Script para generar deltas de 4 nuevos observatorios astronómicos
Usa el mismo formato que Huejotzingo pero para:
- Paranal Observatory, Chile
- San Pedro Mártir Observatory, México  
- Roque de los Muchachos Observatory, La Palma
- Mauna Kea Observatory, Hawái
"""
from astroquery.mpc import MPC
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation, Angle
from astropy.units import Quantity
import json
import os

# --- CONFIGURAR ---
TARGET = "0003I"   # 3I/ATLAS
START = "2025-10-23"   # UTC date string (mismo que Huejotzingo)
STEP = '1h'            # intervalo: '1h'
NUMBER_DELTA = None    # usa default de MPC

OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

# Nuevos observatorios astronómicos
OBSERVATORIES = {
    "paranal": {
        "coords": ("-70.4045d", "-24.6272d", "2635m"),
        "name": "Paranal Observatory",
        "country": "Chile",
        "description": "Observatorio Paranal en el Desierto de Atacama"
    },
    "sanpedromartir": {
        "coords": ("-115.5045d", "31.0456d", "2830m"), 
        "name": "San Pedro Mártir Observatory",
        "country": "México",
        "description": "Observatorio Astronómico Nacional San Pedro Mártir"
    },
    "lapalma": {
        "coords": ("-17.8850d", "28.7569d", "2396m"),
        "name": "Roque de los Muchachos Observatory", 
        "country": "España",
        "description": "Observatorio del Roque de los Muchachos, La Palma"
    },
    "maunakea": {
        "coords": ("-155.4747d", "19.8260d", "4205m"),
        "name": "Mauna Kea Observatory",
        "country": "USA", 
        "description": "Observatorio Mauna Kea, Hawái"
    }
}

def table_to_jsonlist(tab, heliocentric=False, include_jd=True):
    """Convierte astropy.table.Table a lista de dicts JSON serializables."""
    out = []
    for row in tab:
        rec = {}
        
        # Date: buscar columna de fecha
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
        
        # Resto de columnas
        for col in tab.colnames:
            if col != date_col:
                val = row[col]
                if hasattr(val, 'value'):
                    rec[col] = float(val.value) if val.value is not None else None
                elif isinstance(val, str):
                    rec[col] = val
                else:
                    try:
                        rec[col] = float(val) if val is not None else None
                    except:
                        rec[col] = str(val)
        
        out.append(rec)
    
    return out

def generate_observatory_delta(obs_name, obs_data):
    """Genera archivo delta para un observatorio específico"""
    print(f"\n=== Generando deltas para {obs_data['name']} ===")
    
    try:
        # Crear EarthLocation
        lon_str, lat_str, alt_str = obs_data['coords']
        lon = Angle(lon_str)
        lat = Angle(lat_str) 
        alt = Quantity(alt_str)
        location = EarthLocation(lon=lon, lat=lat, height=alt)
        
        print(f"Coordenadas: {lat.deg:.4f}°, {lon.deg:.4f}°, {alt}")
        
        # Query MPC para deltas
        print("Consultando MPC para deltas...")
        delta_tab = MPC.get_ephemeris(
            TARGET, 
            start=START, 
            step=STEP, 
            number=NUMBER_DELTA,
            location=location
        )
        
        print(f"Datos obtenidos: {len(delta_tab)} puntos")
        
        # Convertir a JSON
        delta_data = table_to_jsonlist(delta_tab)
        
        # Crear estructura del JSON (mismo formato que Huejotzingo)
        output = {
            "Objeto": "3I/ATLAS",
            "DesignacionMPC": "0003I",
            "ElementosOrbitales": {
                "Epoch_TT": "2025 Nov. 21.0 TT",
                "Epoch_JDT": "2461000.5",
                "TiempoPerihelio_T_TT": "2025 Oct. 29.4836 TT",
                "TiempoPerihelio_T_JDT": "2460977.98361 JDT",
                "DistanciaPerihelio_q_AU": "1.356411",
                "InversaSemiejeMayor_z": "-3.788733",
                "Excentricidad_e": "6.139080",
                "ArgumentoPerihelio_w": "80.08633",
                "LongitudNodoAscendente_Node": "318.86109",
                "Inclinacion_i": "77.37844"
            },
            "Observatorio": {
                "Nombre": obs_data['name'],
                "Pais": obs_data['country'],
                "Descripcion": obs_data['description'],
                "Coordenadas": {
                    "Latitud": f"{lat.deg:.6f}",
                    "Longitud": f"{lon.deg:.6f}", 
                    "Altitud_m": f"{alt.value:.0f}"
                }
            },
            "ParametrosEfemerides": {
                "ObjetoConsultado": TARGET,
                "FechaInicio": START,
                "Intervalo": STEP,
                "NumeroPuntos": len(delta_data),
                "TipoEfemerides": "Topocentric",
                "FuenteDatos": "Minor Planet Center (MPC)"
            },
            "DatosEfemerides": delta_data
        }
        
        # Guardar archivo
        filename = f"ephem_{obs_name}_delta.json"
        filepath = os.path.join(OUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Guardado: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Error generando {obs_name}: {e}")
        return False

def main():
    """Generar deltas para todos los observatorios"""
    print("🔭 Generando deltas para observatorios astronómicos...")
    print(f"Objetivo: {TARGET}")
    print(f"Fecha inicio: {START}")
    print(f"Intervalo: {STEP}")
    
    success_count = 0
    
    for obs_name, obs_data in OBSERVATORIES.items():
        if generate_observatory_delta(obs_name, obs_data):
            success_count += 1
    
    print(f"\n🎯 Completado: {success_count}/{len(OBSERVATORIES)} observatorios")
    print("\nArchivos generados en el directorio 'data/':")
    
    for obs_name in OBSERVATORIES.keys():
        filename = f"ephem_{obs_name}_delta.json"
        filepath = os.path.join(OUT_DIR, filename)
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  ✅ {filename} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()