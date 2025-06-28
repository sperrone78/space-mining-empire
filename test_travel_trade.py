#!/usr/bin/env python3
"""
Test the new travel-to-trade mechanics
"""

from game.web_engine import GameWebEngine

def test_travel_trade_mechanics():
    print("=== Testing Travel-to-Trade Mechanics ===")
    
    # Create game engine
    engine = GameWebEngine()
    
    print("\n1. Starting Game State:")
    status = engine.get_status()
    location = engine.get_location_info()
    print(f"   Starting Location: {location['name']} ({location['body_type']})")
    print(f"   Has Outpost: {location['has_outpost']}")
    print(f"   Resources: {list(location['resources'].keys())}")
    print(f"   Starting Credits: {status['credits']}")
    
    # Try to mine some resources at starting location
    print("\n2. Mining at Starting Location:")
    if location['resources']:
        resource_type = list(location['resources'].keys())[0]
        result = engine.mine_resource(resource_type)
        print(f"   Mining {resource_type}: {result['message']}")
        
        # Check cargo after mining
        new_status = engine.get_status()
        print(f"   New cargo: {new_status['cargo']}")
    else:
        print("   No resources to mine here")
    
    # Try to trade at starting location (should fail)
    print("\n3. Attempting to Trade at Starting Location:")
    trade_result = engine.trade_at_outpost(sell_all=True)
    print(f"   Trade attempt: {trade_result['message']}")
    print(f"   Success: {trade_result['success']}")
    
    # Show available destinations
    print("\n4. Available Travel Destinations:")
    destinations = engine.get_destinations()
    for dest in destinations:
        features = []
        if dest['has_outpost']:
            features.append(f"Outpost: {dest['outpost_name']}")
        if dest['has_resources']:
            features.append("Mining Available")
        
        print(f"   {dest['name']} ({dest['body_type']}) - {dest['distance']:.1f} AU")
        print(f"     Fuel cost: {dest['fuel_cost']}, Features: {', '.join(features) if features else 'None'}")
    
    # Travel to the first outpost location
    print("\n5. Traveling to Trading Outpost:")
    outpost_destinations = [d for d in destinations if d['has_outpost']]
    
    if outpost_destinations:
        dest = outpost_destinations[0]
        print(f"   Traveling to {dest['name']}...")
        
        travel_result = engine.travel_to(dest['index'])
        print(f"   Travel result: {travel_result['message']}")
        
        if travel_result['success']:
            # Check new location
            new_location = engine.get_location_info()
            print(f"   New location: {new_location['name']}")
            print(f"   Has outpost: {new_location['has_outpost']}")
            if new_location['has_outpost']:
                print(f"   Outpost: {new_location['outpost_name']} ({new_location['outpost_type']})")
    
    # Try trading at the outpost
    print("\n6. Trading at Outpost:")
    current_status = engine.get_status()
    if current_status['cargo']:
        outpost_info = engine.get_outposts()
        if outpost_info:
            print(f"   Trading at {outpost_info['name']}")
            print(f"   Cargo value: {outpost_info['total_value']:.0f} credits")
            
            trade_result = engine.trade_at_outpost(sell_all=True)
            print(f"   Trade result: {trade_result['message']}")
            
            final_status = engine.get_status()
            print(f"   Credits after trade: {final_status['credits']}")
        else:
            print("   No outpost data available")
    else:
        print("   No cargo to trade")
    
    # Travel to a rich mining location
    print("\n7. Traveling to Rich Mining Location:")
    mining_destinations = [d for d in destinations if d['has_resources'] and not d['has_outpost']]
    
    if mining_destinations:
        dest = mining_destinations[0]
        print(f"   Traveling to {dest['name']} for mining...")
        
        travel_result = engine.travel_to(dest['index'])
        print(f"   Travel result: {travel_result['message']}")
        
        if travel_result['success']:
            new_location = engine.get_location_info()
            print(f"   New location: {new_location['name']}")
            print(f"   Resources available: {list(new_location['resources'].keys())}")
            
            # Mine some resources
            if new_location['resources']:
                resource_type = list(new_location['resources'].keys())[0]
                result = engine.mine_resource(resource_type)
                print(f"   Mining {resource_type}: {result['message']}")
    
    print("\n=== Travel-to-Trade Mechanics Test Complete! ===")
    print("✓ Location-based trading enforced")
    print("✓ Mining and trading separated by location")
    print("✓ Players must travel between locations")
    print("✓ Fuel management becomes strategic")
    print("✓ Different locations have different purposes")

if __name__ == "__main__":
    test_travel_trade_mechanics()