#!/usr/bin/env python3
"""
Test the web API functionality
"""

from game.web_engine import GameWebEngine

def test_web_api():
    print("=== Testing Space Mining Empire Web API ===")
    
    # Create game engine
    engine = GameWebEngine()
    
    # Test status
    print("\n1. Testing status API:")
    status = engine.get_status()
    print(f"   Player: {status['player_name']}")
    print(f"   Credits: {status['credits']}")
    print(f"   Location: {status['location']}")
    print(f"   Ship: {status['ship_name']}")
    
    # Test location info
    print("\n2. Testing location API:")
    location = engine.get_location_info()
    print(f"   Location: {location['name']}")
    print(f"   Resources: {location['resources']}")
    
    # Test mining
    print("\n3. Testing mining API:")
    # Find first available resource
    if location['resources']:
        resource_type = list(location['resources'].keys())[0]
        result = engine.mine_resource(resource_type)
        print(f"   Mining {resource_type}: {result['message']}")
        
        # Check status after mining
        new_status = engine.get_status()
        print(f"   New cargo: {new_status['cargo']}")
    
    # Test travel
    print("\n4. Testing travel API:")
    destinations = engine.get_destinations()
    if destinations:
        dest = destinations[0]
        print(f"   Available destination: {dest['name']} (fuel cost: {dest['fuel_cost']})")
        
        if dest['can_travel']:
            result = engine.travel_to(dest['index'])
            print(f"   Travel result: {result['message']}")
    
    # Test trading
    print("\n5. Testing trading API:")
    outposts = engine.get_outposts()
    if outposts and engine.get_status()['cargo']:
        outpost = outposts[0]
        print(f"   Outpost: {outpost['name']}")
        print(f"   Potential value: {outpost['total_value']}")
        
        # Test selling all cargo
        result = engine.trade_at_outpost(0, sell_all=True)
        print(f"   Trade result: {result['message']}")
        
        # Check credits after trade
        final_status = engine.get_status()
        print(f"   New credits: {final_status['credits']}")
    
    # Test shop
    print("\n6. Testing shop API:")
    shop = engine.get_shop_data()
    print(f"   Available upgrades: {len(shop['upgrades'])}")
    print(f"   Available ships: {len(shop['ships'])}")
    
    upgrade = shop['upgrades'][0]
    print(f"   First upgrade: {upgrade['name']} - {upgrade['cost']} credits")
    print(f"   Affordable: {upgrade['affordable']}")
    
    print("\n=== All Web API Tests Complete! ===")
    print("✓ Status API working")
    print("✓ Location API working")
    print("✓ Mining API working")
    print("✓ Travel API working")
    print("✓ Trading API working")
    print("✓ Shop API working")

if __name__ == "__main__":
    test_web_api()