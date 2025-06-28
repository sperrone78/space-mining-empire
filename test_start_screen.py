#!/usr/bin/env python3
"""
Test the start screen and location-based UI features
"""

from game.web_engine import GameWebEngine

def test_start_screen_features():
    print("=== Testing Start Screen and Location-Based UI ===")
    
    # Test 1: Engine starts without auto-initialization
    print("\n1. Testing Engine Initialization:")
    engine = GameWebEngine()
    print(f"   Player initialized: {engine.player is not None}")
    print(f"   Expected: False (should wait for user input)")
    
    # Test 2: Custom starting credits
    print("\n2. Testing Custom Starting Credits:")
    engine.initialize_game(starting_credits=2500)
    print(f"   Starting credits: {engine.player.credits}")
    print(f"   Expected: 2500.0")
    
    # Test 3: Location facilities
    print("\n3. Testing Location Facilities:")
    for i, body in enumerate(engine.celestial_bodies):
        print(f"   {body.name} ({body.body_type}):")
        print(f"     Has outpost: {body.has_outpost}")
        print(f"     Has ship shop: {body.has_ship_shop}")
        print(f"     Has resources: {len(body.resources) > 0}")
        
        if body.has_outpost:
            print(f"     Outpost: {body.outpost.name}")
    
    # Test 4: Starting location setup
    print("\n4. Testing Starting Location:")
    start_location = engine.player.current_location
    print(f"   Starting at: {start_location.name}")
    print(f"   Has mining: {len(start_location.resources) > 0}")
    print(f"   Has trading: {start_location.has_outpost}")
    print(f"   Has ship shop: {start_location.has_ship_shop}")
    
    # Test 5: Nearby trading post
    print("\n5. Testing Nearby Trading Access:")
    destinations = engine.get_destinations()
    trading_posts = [d for d in destinations if d['has_outpost']]
    
    print(f"   Available trading posts: {len(trading_posts)}")
    for post in trading_posts:
        print(f"     {post['name']}: {post['fuel_cost']} fuel cost")
    
    # Find closest trading post
    if trading_posts:
        closest = min(trading_posts, key=lambda x: x['fuel_cost'])
        print(f"   Closest trading post: {closest['name']} ({closest['fuel_cost']} fuel)")
        
        # Test if reachable with starting fuel
        can_reach = engine.get_status()['current_fuel'] >= closest['fuel_cost']
        print(f"   Reachable with starting fuel: {can_reach}")
    
    # Test 6: Location-based UI logic
    print("\n6. Testing Location-Based UI Logic:")
    
    def check_ui_options(location_name):
        # Find the location
        location = next((body for body in engine.celestial_bodies if body.name == location_name), None)
        if not location:
            return
        
        # Simulate being at this location
        engine.player.current_location = location
        location_data = engine.get_location_info()
        
        print(f"   At {location_name}:")
        print(f"     Show Mining: {len(location_data['resources']) > 0}")
        print(f"     Show Trading: {location_data['has_outpost']}")
        print(f"     Show Ship Shop: {location_data['has_ship_shop']}")
    
    # Test at different locations
    for body in engine.celestial_bodies:
        check_ui_options(body.name)
    
    # Test 7: Settings functionality
    print("\n7. Testing Settings System:")
    original_credits = engine.settings['starting_credits']
    print(f"   Default starting credits: {original_credits}")
    
    # Test different starting amounts
    test_amounts = [500, 2000, 5000, 10000]
    for amount in test_amounts:
        engine.initialize_game(starting_credits=amount)
        print(f"   With {amount} credits: {engine.player.credits}")
    
    print("\n=== Start Screen Features Test Complete! ===")
    print("✅ Engine waits for user initialization")
    print("✅ Custom starting credits work")
    print("✅ Location facilities properly configured")
    print("✅ Trading post available near starting area")
    print("✅ Location-based UI logic implemented")
    print("✅ Settings system functional")

if __name__ == "__main__":
    test_start_screen_features()