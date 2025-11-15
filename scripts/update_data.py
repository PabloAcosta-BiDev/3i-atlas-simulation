#!/usr/bin/env python3
"""
Data Generation Script for 3I-ATLAS GitHub Actions
Uses MPC (Minor Planet Center) to fetch new ephemeris data and appends to existing JSONs
Generates 60 days of future data from current date
"""
import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add backend to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    from astroquery.mpc import MPC
    from astropy import units as u
    from astropy.time import Time
    from astropy.units import Quantity
    from Scripts.fetch_mpc_ephem import table_to_jsonlist
except ImportError as e:
    print(f"❌ Missing required packages: {e}")
    print("Install: pip install astroquery astropy")
    sys.exit(1)

# Configuration
TARGET = "0003I"  # 3I/ATLAS comet
STEP = '1h'       # 1 hour intervals
NUMBER_DAYS = 60  # Generate 60 days of future data
NUMBER_VECT = NUMBER_DAYS * 24  # 24 hours per day

# Observatory locations
LOCATIONS = {
    "huejotzingo": ("-98.4073988d", "19.158971d", "2260m"),
    "tijuana": ("-117.060556d", "32.514947d", "40m"),
    "cancun": ("-86.8475d", "21.1619d", "10m")
}

# Repository paths
REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

def get_next_start_date():
    """Get start date for next 60 days based on existing data"""
    vectors_file = DATA_DIR / 'ephem_vectors_fetched.json'
    
    if vectors_file.exists():
        try:
            with open(vectors_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            if existing_data and len(existing_data) > 0:
                # Get the last date from existing data
                last_record = existing_data[-1]
                if 'ISO' in last_record:
                    last_date = datetime.fromisoformat(last_record['ISO'].replace('Z', '+00:00'))
                    # Start 1 hour after last record to avoid overlap
                    start_date = last_date + timedelta(hours=1)
                    return start_date.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"⚠️ Could not parse existing data, using current date: {e}")
    
    # Default: start from now
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def fetch_and_append_vectors():
    """Fetch heliocentric vectors from MPC and append to existing data"""
    start_date = get_next_start_date()
    print(f'📡 Fetching heliocentric vectors from {start_date} for {NUMBER_DAYS} days...')
    
    try:
        # Fetch new data from MPC
        step_qty = Quantity(STEP)
        tab = MPC.get_ephemeris(TARGET, start=start_date, step=step_qty, 
                               number=NUMBER_VECT, eph_type='heliocentric', cache=False)
        new_data = table_to_jsonlist(tab, heliocentric=True)
        
        # Load existing data
        vectors_file = DATA_DIR / 'ephem_vectors_fetched.json'
        existing_data = []
        if vectors_file.exists():
            with open(vectors_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        # Append new data to existing
        combined_data = existing_data + new_data
        
        # Write combined data back
        with open(vectors_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
        
        print(f'✅ Updated {vectors_file} (added {len(new_data)} records, total: {len(combined_data)})')
        return True
        
    except Exception as e:
        print(f'❌ Error fetching vectors: {e}')
        return False

def fetch_and_append_deltas():
    """Fetch topocentric ephemeris for each location and append to existing data"""
    start_date = get_next_start_date()
    success_count = 0
    
    # Calculate number of records for deltas (can be different from vectors)
    number_delta = NUMBER_DAYS * 24  # Same as vectors for consistency
    
    for location_name, coords in LOCATIONS.items():
        try:
            print(f'📡 Fetching delta data for {location_name} from {start_date}...')
            
            # Fetch new data from MPC
            step_qty = Quantity(STEP)
            tab = MPC.get_ephemeris(TARGET, location=coords, start=start_date, 
                                   step=step_qty, number=number_delta, cache=False)
            new_data = table_to_jsonlist(tab, heliocentric=False)
            
            # Add location metadata
            for rec in new_data:
                rec['Location'] = location_name
                rec['UTC_offset'] = -6 if location_name == 'huejotzingo' else (-7 if location_name == 'tijuana' else -5)
            
            # Load existing data
            delta_file = DATA_DIR / f'ephem_delta_{location_name}.json'
            existing_data = []
            if delta_file.exists():
                with open(delta_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Append new data to existing
            combined_data = existing_data + new_data
            
            # Write combined data back
            with open(delta_file, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, indent=2, ensure_ascii=False)
            
            print(f'✅ Updated {delta_file} (added {len(new_data)} records, total: {len(combined_data)})')
            success_count += 1
            
        except Exception as e:
            print(f'❌ Error fetching delta for {location_name}: {e}')
    
    return success_count == len(LOCATIONS)

def update_status():
    """Update status file with last update timestamp"""
    status_file = DATA_DIR / 'last_update.json'
    status = {
        'last_update': datetime.utcnow().isoformat() + 'Z',
        'update_type': 'append_60_days',
        'target': TARGET,
        'step': STEP,
        'days_added': NUMBER_DAYS,
        'updated_files': [
            'ephem_vectors_fetched.json',
            'ephem_delta_cancun.json',
            'ephem_delta_huejotzingo.json',
            'ephem_delta_tijuana.json'
        ]
    }
    
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    
    print(f'✅ Updated {status_file}')

def main():
    """Main execution function"""
    print("🌌 Starting 3I-ATLAS ephemeris data update...")
    print(f"Target: {TARGET}")
    print(f"Step: {STEP}")
    print(f"Days to add: {NUMBER_DAYS}")
    print(f"Data Directory: {DATA_DIR}")
    print("-" * 60)
    
    # Fetch data from Minor Planet Center
    vectors_success = fetch_and_append_vectors()
    deltas_success = fetch_and_append_deltas()
    
    if vectors_success and deltas_success:
        update_status()
        print("-" * 60)
        print("✅ All ephemeris data updated successfully!")
        print(f"📊 Added {NUMBER_DAYS} days of future data to existing datasets")
        return 0
    else:
        print("-" * 60)
        print("❌ Some updates failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())