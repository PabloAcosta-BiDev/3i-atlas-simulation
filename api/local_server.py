#!/usr/bin/env python3
"""
Local development server for 3I/ATLAS Simulation
Runs the Vercel API handler on localhost:8000 for local testing

Usage:
    python local_server.py
    
Then open web/index-modern.html in your browser
"""
from http.server import HTTPServer
import sys
import os

# Add api directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from index import handler

if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('0.0.0.0', PORT), handler)
    print(f'3I/ATLAS API Server running on http://localhost:{PORT}')
    print(f'Serving data from: {os.path.join(os.getcwd(), "data")}')
    print(f'Open web/index-modern.html in your browser')
    print('Press Ctrl+C to stop\n')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n✅ Server stopped')
        server.shutdown()
