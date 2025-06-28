#!/usr/bin/env python3
"""
Test the New Game button functionality
"""

import requests
import json
import time
import threading
import http.server
import socketserver
from game.web_engine import GameWebEngine
from web_main import GameHTTPHandler, create_handler

def test_new_game_api():
    print("=== Testing New Game Button API ===")
    
    # Test 1: Engine initialization state
    print("\n1. Testing Engine Initialization:")
    engine = GameWebEngine()
    print(f"   Engine initialized: {engine.is_initialized()}")
    print(f"   Expected: False")
    
    # Test 2: Manual initialization
    print("\n2. Testing Manual Initialization:")
    engine.initialize_game(starting_credits=2000)
    print(f"   Engine initialized: {engine.is_initialized()}")
    print(f"   Player credits: {engine.player.credits}")
    print(f"   Expected: True, 2000.0")
    
    # Test 3: Reset and test API
    print("\n3. Testing API with Uninitialized Engine:")
    engine = GameWebEngine()  # Fresh engine
    
    status = engine.get_status() if engine.is_initialized() else {'error': 'Game not initialized'}
    print(f"   Status response: {status}")
    
    # Test 4: Initialize via API call
    print("\n4. Testing Initialize via API:")
    engine.initialize_game(starting_credits=1500)
    status = engine.get_status()
    print(f"   After initialization: {status['credits']} credits")
    
    print("\n=== API Test Complete ===")

def start_test_server():
    """Start a test server for manual testing"""
    print("\n=== Starting Test Server ===")
    print("You can now test the New Game button manually at:")
    print("http://localhost:8081")
    print("Check browser console for any JavaScript errors")
    
    game_engine = GameWebEngine()
    handler = create_handler(game_engine)
    
    PORT = 8081
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Test server running on port {PORT}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nTest server stopped.")

if __name__ == "__main__":
    test_new_game_api()
    
    user_input = input("\nWould you like to start a test server for manual testing? (y/n): ")
    if user_input.lower() == 'y':
        start_test_server()