import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            if path == '/api/' or path == '/api':
                response = {"message": "3I/ATLAS API is running on Vercel", "version": "1.0"}
            elif path == '/api/status':
                response = self.get_status()
            elif path == '/api/vectors':
                response = self.load_json("ephem_vectors_fetched.json")
            elif path.startswith('/api/deltas/'):
                location = path.split('/')[-1]
                response = self.load_json(f"ephem_delta_{location.lower()}.json")
            elif path == '/api/orbits':
                response = self.load_json("elemental_orbits.json")
            elif path == '/api/planets':
                response = self.get_planets()
            elif path.startswith('/api/planets/'):
                name = path.split('/')[-1]
                response = self.load_json(f"planets/{name.lower()}.json")
            else:
                self.send_response(404)
                response = {"error": "Endpoint not found", "path": path}
                
        except Exception as e:
            self.send_response(500)
            response = {"error": str(e), "path": path}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def load_json(self, filename):
        """Load JSON file from data directory with proper error handling"""
        # Get base directory (two levels up from api/)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, "data")
        path = os.path.join(data_dir, filename)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Data file not found: {filename}")
        
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get_status(self):
        """Get API status and last data update time"""
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            data_dir = os.path.join(base_dir, "data")
            
            # Check if last_update.json exists (GitHub Actions creates this)
            update_file = os.path.join(data_dir, "last_update.json")
            if os.path.exists(update_file):
                with open(update_file, "r", encoding="utf-8") as f:
                    update_info = json.load(f)
                return {
                    "status": "ok",
                    "last_update": update_info.get("last_update"),
                    "updated_files": update_info.get("updated_files", []),
                    "deployment": "vercel"
                }
            
            # Fallback: check file modification times
            json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
            if json_files:
                latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(data_dir, f)))
                latest_time = os.path.getmtime(os.path.join(data_dir, latest_file))
                from datetime import datetime
                return {
                    "status": "ok",
                    "last_update": datetime.fromtimestamp(latest_time).isoformat(),
                    "latest_file": latest_file,
                    "deployment": "vercel"
                }
            else:
                return {"status": "no data files found", "deployment": "vercel"}
                
        except Exception as e:
            return {"status": "error", "error": str(e), "deployment": "vercel"}
    
    def get_planets(self):
        """Get heliocentric positions for all planets"""
        result = {
            "bodies": {},
            "times": None
        }
        
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            planets_dir = os.path.join(base_dir, "data", "planets")
            
            if not os.path.exists(planets_dir):
                return {"error": "Planets data directory not found"}
            
            planet_names = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]
            loaded_count = 0
            
            for name in planet_names:
                try:
                    planet_path = os.path.join(planets_dir, f"{name}.json")
                    if os.path.exists(planet_path):
                        with open(planet_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        if result["times"] is None:
                            result["times"] = data.get("times", [])
                        result["bodies"][name] = data.get("positions", [])
                        loaded_count += 1
                except Exception as e:
                    print(f"Error loading {name}.json: {e}")
                    continue
            
            if loaded_count == 0:
                return {"error": "No planet data files could be loaded"}
            
            return result
            
        except Exception as e:
            return {"error": f"Planet data loading failed: {str(e)}"}
    
# For Vercel compatibility
def lambda_handler(event, context):
    """AWS Lambda compatibility layer (if needed)"""
    return handler