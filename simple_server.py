#!/usr/bin/env python3
"""
Simple web server to test the game
"""
import http.server
import socketserver
import os

# Change to the directory containing game.html
os.chdir('/home/sperrone/space_mining_empire')

PORT = 8080

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/game.html'
        return super().do_GET()

with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    print("Game available at http://localhost:8080")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")