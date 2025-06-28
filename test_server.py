#!/usr/bin/env python3
"""
Test server to check if the game backend works
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.web_engine import GameWebEngine
import json

def test_backend():
    print("Testing Space Mining Empire Backend...")
    
    # Create game engine
    engine = GameWebEngine()
    
    # Test 1: Check initial state
    print(f"1. Is initialized: {engine.is_initialized()}")
    
    # Test 2: Initialize game
    print("2. Initializing game...")
    try:
        engine.initialize_game(1000)
        print(f"   Game initialized: {engine.is_initialized()}")
    except Exception as e:
        print(f"   Error initializing: {e}")
        return False
    
    # Test 3: Get status
    print("3. Getting status...")
    try:
        status = engine.get_status()
        print(f"   Status: {status}")
    except Exception as e:
        print(f"   Error getting status: {e}")
        return False
    
    # Test 4: Get location
    print("4. Getting location...")
    try:
        location = engine.get_location_info()
        print(f"   Location: {location['name']} ({location['body_type']})")
        print(f"   Resources: {list(location['resources'].keys())}")
    except Exception as e:
        print(f"   Error getting location: {e}")
        return False
    
    # Test 5: Get destinations
    print("5. Getting destinations...")
    try:
        destinations = engine.get_destinations()
        print(f"   Found {len(destinations)} destinations")
        for dest in destinations[:2]:  # Show first 2
            print(f"   - {dest['name']} ({dest['distance']:.1f} AU)")
    except Exception as e:
        print(f"   Error getting destinations: {e}")
        return False
    
    print("\n✅ Backend tests passed! The game engine is working properly.")
    return True

if __name__ == "__main__":
    test_backend()