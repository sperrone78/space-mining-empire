#!/usr/bin/env python3
"""
Quick test to verify the New Game button fix
"""

import time
import threading
import webbrowser
from web_main import main

def test_server():
    print("Starting test server...")
    print("This will start the web server and you can test the New Game button")
    print("Check your browser console for debug messages")
    print("Press Ctrl+C to stop the server")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    test_server()