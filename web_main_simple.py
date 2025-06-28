#!/usr/bin/env python3
"""
Space Mining Empire - Simple Web Server (no browser auto-open)
"""

import http.server
import socketserver
import json
import urllib.parse
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

def main():
    game_engine = GameWebEngine()
    handler = create_handler(game_engine)
    PORT = 8080
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Space Mining Empire Web Server running at http://localhost:{PORT}")
        print("Game available at http://localhost:8080")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nGame server stopped.")

if __name__ == "__main__":
    main()