#!/usr/bin/env python3
"""
Simple HTTP server for the Handy web app
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8000
WEB_DIR = Path(__file__).parent / "web"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

def main():
    # Ensure the web directory exists
    if not WEB_DIR.exists():
        print(f"Error: Web directory not found at {WEB_DIR}")
        return
    
    # Print server information
    print(f"Starting Handy Web App server at http://localhost:{PORT}")
    print(f"Serving files from: {WEB_DIR}")
    print("Press Ctrl+C to stop the server")
    
    # Open the browser
    webbrowser.open(f"http://localhost:{PORT}")
    
    # Start the server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()