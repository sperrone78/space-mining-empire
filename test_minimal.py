#!/usr/bin/env python3
"""
Minimal test to verify the game initialization flow
"""

from game.web_engine import GameWebEngine

def test_minimal_flow():
    print("=== Minimal New Game Flow Test ===")
    
    # Step 1: Create engine (should not be initialized)
    print("\n1. Creating engine...")
    engine = GameWebEngine()
    print(f"   Initialized: {engine.is_initialized()}")
    
    # Step 2: Try to get status (should return error)
    print("\n2. Getting status before initialization...")
    status = engine.get_status()
    print(f"   Status: {status}")
    
    # Step 3: Initialize game
    print("\n3. Initializing game with 1500 credits...")
    engine.initialize_game(starting_credits=1500)
    print(f"   Initialized: {engine.is_initialized()}")
    
    # Step 4: Get status after initialization
    print("\n4. Getting status after initialization...")
    status = engine.get_status()
    if 'error' not in status:
        print(f"   Player: {status['player_name']}")
        print(f"   Credits: {status['credits']}")
        print(f"   Location: {status['location']}")
        print(f"   Ship: {status['ship_name']}")
    else:
        print(f"   Error: {status['error']}")
    
    # Step 5: Get location info
    print("\n5. Getting location info...")
    location = engine.get_location_info()
    if 'error' not in location:
        print(f"   Location: {location['name']}")
        print(f"   Type: {location['body_type']}")
        print(f"   Has outpost: {location['has_outpost']}")
        print(f"   Has shop: {location['has_ship_shop']}")
        print(f"   Resources: {list(location['resources'].keys())}")
    else:
        print(f"   Error: {location['error']}")
    
    print("\n✅ Minimal flow test complete!")
    print("If all steps show expected results, the New Game button should work.")

if __name__ == "__main__":
    test_minimal_flow()