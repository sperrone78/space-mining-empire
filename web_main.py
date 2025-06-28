#!/usr/bin/env python3
"""
Space Mining Empire - Web UI Version
"""

import http.server
import socketserver
import json
import urllib.parse
import threading
import webbrowser
import time
from game.web_engine import GameWebEngine

class GameHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, game_engine=None, **kwargs):
        self.game_engine = game_engine
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/game.html'
        elif self.path == '/api/status':
            if self.game_engine.is_initialized():
                self.send_api_response(self.game_engine.get_status())
            else:
                self.send_api_response({'error': 'Game not initialized'})
            return
        elif self.path == '/api/location':
            if self.game_engine.is_initialized():
                self.send_api_response(self.game_engine.get_location_info())
            else:
                self.send_api_response({'error': 'Game not initialized'})
            return
        elif self.path == '/api/outposts':
            if self.game_engine.is_initialized():
                self.send_api_response(self.game_engine.get_outposts())
            else:
                self.send_api_response({'error': 'Game not initialized'})
            return
        elif self.path == '/api/shop':
            if self.game_engine.is_initialized():
                self.send_api_response(self.game_engine.get_shop_data())
            else:
                self.send_api_response({'error': 'Game not initialized'})
            return
        elif self.path == '/api/destinations':
            if self.game_engine.is_initialized():
                self.send_api_response(self.game_engine.get_destinations())
            else:
                self.send_api_response({'error': 'Game not initialized'})
            return
        elif self.path == '/api/init_game':
            if hasattr(self.game_engine, 'player') and self.game_engine.player:
                self.send_api_response({'success': True, 'message': 'Game already initialized'})
            else:
                self.send_api_response({'success': False, 'message': 'Game not initialized'})
            return
        
        super().do_GET()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/mine':
            self.handle_mine_request()
        elif self.path == '/api/travel':
            self.handle_travel_request()
        elif self.path == '/api/trade':
            self.handle_trade_request()
        elif self.path == '/api/shop/buy':
            self.handle_shop_buy_request()
        elif self.path == '/api/init_game':
            self.handle_init_game_request()
        else:
            self.send_error(404)
    
    def handle_mine_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        result = self.game_engine.mine_resource(data['resource_type'])
        self.send_api_response(result)
    
    def handle_travel_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        result = self.game_engine.travel_to(data['destination_index'])
        self.send_api_response(result)
    
    def handle_trade_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        result = self.game_engine.trade_at_outpost(data.get('resource_type'), data.get('sell_all', False))
        self.send_api_response(result)
    
    def handle_shop_buy_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        result = self.game_engine.buy_from_shop(data['item_type'], data['item_index'])
        self.send_api_response(result)
    
    def handle_init_game_request(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            starting_credits = data.get('starting_credits', 1000)
            self.game_engine.initialize_game(starting_credits)
            
            self.send_api_response({
                'success': True,
                'message': f'Game initialized with {starting_credits} starting credits'
            })
        except Exception as e:
            print(f"Error in init_game: {e}")
            self.send_api_response({
                'success': False,
                'message': f'Failed to initialize game: {str(e)}'
            })
    
    def send_api_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def create_handler(game_engine):
    def handler(*args, **kwargs):
        return GameHTTPHandler(*args, game_engine=game_engine, **kwargs)
    return handler

def find_available_port(start_port=8080):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise OSError("No available ports found")

def main():
    game_engine = GameWebEngine()
    # Don't auto-initialize - wait for user to start new game
    handler = create_handler(game_engine)
    
    try:
        PORT = find_available_port(8080)
    except OSError:
        print("Error: No available ports found in range 8080-8090")
        return
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Space Mining Empire Web UI running at http://localhost:{PORT}")
        print("Opening game in your default browser...")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}')
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nGame server stopped.")

if __name__ == "__main__":
    main()