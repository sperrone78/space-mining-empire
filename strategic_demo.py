#!/usr/bin/env python3
"""
Strategic gameplay demonstration showing the travel-to-trade mechanics
"""

from game.web_engine import GameWebEngine

def strategic_gameplay_demo():
    print("=== SPACE MINING EMPIRE: Strategic Gameplay Demo ===")
    print("Demonstrating the new travel-to-trade mechanics that require strategic planning!\n")
    
    # Create game engine
    engine = GameWebEngine()
    
    def show_status():
        status = engine.get_status()
        location = engine.get_location_info()
        print(f"📍 Location: {location['name']} ({location['body_type']})")
        print(f"💰 Credits: {status['credits']:.0f}")
        print(f"📦 Cargo: {status['cargo_used']}/{status['cargo_capacity']}")
        print(f"⛽ Fuel: {status['current_fuel']}/{status['fuel_capacity']}")
        if status['cargo']:
            cargo_list = [f"{amount} {resource}" for resource, amount in status['cargo'].items()]
            print(f"🎒 Current cargo: {', '.join(cargo_list)}")
        print()
    
    # Starting situation
    print("🌟 STARTING SITUATION:")
    show_status()
    
    print("🎯 GOAL: Mine resources and sell them for profit!")
    print("⚠️  CHALLENGE: Mining and trading happen at different locations!")
    print("🚀 STRATEGY: Travel between locations, manage fuel, maximize profits\n")
    
    # Phase 1: Initial Mining
    print("📍 PHASE 1: MINING AT STARTING PLANET")
    location = engine.get_location_info()
    print(f"Available resources at {location['name']}:")
    
    for resource, amount in location['resources'].items():
        print(f"  • {resource}: {amount} units")
    
    # Mine multiple resources
    print("\n⛏️  Mining Iron and Copper...")
    iron_result = engine.mine_resource('Iron')
    print(f"Iron mining: {iron_result['message']}")
    
    copper_result = engine.mine_resource('Copper')
    print(f"Copper mining: {copper_result['message']}")
    
    print("\n📊 After mining:")
    show_status()
    
    # Phase 2: Scouting destinations
    print("🗺️  PHASE 2: SCOUTING TRAVEL DESTINATIONS")
    destinations = engine.get_destinations()
    
    print("Available destinations:")
    for dest in destinations:
        features = []
        if dest['has_outpost']:
            features.append(f"🏪 {dest['outpost_name']}")
        if dest['has_resources']:
            features.append("⛏️ Mining")
        
        fuel_status = "✅" if engine.get_status()['current_fuel'] >= dest['fuel_cost'] else "❌"
        
        print(f"  {dest['name']} ({dest['body_type']}) - {dest['distance']:.1f} AU")
        print(f"    Fuel needed: {dest['fuel_cost']} {fuel_status}")
        print(f"    Features: {', '.join(features) if features else '⚠️ No facilities'}")
    
    # Phase 3: Travel to trading post
    print("\n🚀 PHASE 3: TRAVELING TO TRADING POST")
    outpost_destinations = [d for d in destinations if d['has_outpost']]
    closest_outpost = min(outpost_destinations, key=lambda x: x['fuel_cost'])
    
    print(f"Traveling to {closest_outpost['name']} (closest trading post)...")
    travel_result = engine.travel_to(closest_outpost['index'])
    print(f"Travel: {travel_result['message']}")
    
    print("\n📊 After travel:")
    show_status()
    
    # Phase 4: Trading
    print("💱 PHASE 4: TRADING AT OUTPOST")
    outpost_info = engine.get_outposts()
    
    if outpost_info:
        print(f"Welcome to {outpost_info['name']}!")
        print(f"Outpost type: {outpost_info['outpost_type']}")
        print("\nCargo prices:")
        
        for cargo in outpost_info['cargo_prices']:
            print(f"  {cargo['resource']}: {cargo['amount']} units @ {cargo['price']:.1f} = {cargo['value']:.0f} credits")
        
        print(f"\nTotal cargo value: {outpost_info['total_value']:.0f} credits")
        
        trade_result = engine.trade_at_outpost(sell_all=True)
        print(f"\nTrading: {trade_result['message']}")
    
    print("\n📊 After trading:")
    show_status()
    
    # Phase 5: Strategic decision - where to go next?
    print("🤔 PHASE 5: STRATEGIC PLANNING")
    current_status = engine.get_status()
    print("Now you have credits but need more resources. Where should you go?")
    print("\nOptions:")
    
    destinations = engine.get_destinations()  # Refresh destinations
    
    # Find rich mining locations
    rich_mining = [d for d in destinations if d['has_resources'] and not d['has_outpost']]
    nearby_mining = [d for d in rich_mining if d['fuel_cost'] <= current_status['current_fuel']]
    
    if nearby_mining:
        best_mining = max(nearby_mining, key=lambda x: x['distance'])  # Further = rarer resources
        print(f"  🎯 RECOMMENDED: {best_mining['name']} - Rich mining location")
        print(f"     Distance: {best_mining['distance']:.1f} AU, Fuel cost: {best_mining['fuel_cost']}")
        print(f"     Strategy: Mine rare resources, then return to sell at higher prices!")
        
        # Execute the strategy
        print(f"\n🚀 Executing strategy: Traveling to {best_mining['name']}...")
        travel_result = engine.travel_to(best_mining['index'])
        print(f"Travel: {travel_result['message']}")
        
        print("\n📊 At new mining location:")
        show_status()
        
        new_location = engine.get_location_info()
        print(f"Available resources at {new_location['name']}:")
        for resource, amount in new_location['resources'].items():
            print(f"  • {resource}: {amount} units")
        
        # Mine something valuable
        if 'Gold' in new_location['resources']:
            print("\n⛏️  Mining Gold (valuable resource)...")
            gold_result = engine.mine_resource('Gold')
            print(f"Gold mining: {gold_result['message']}")
        elif new_location['resources']:
            resource = list(new_location['resources'].keys())[0]
            print(f"\n⛏️  Mining {resource}...")
            mine_result = engine.mine_resource(resource)
            print(f"{resource} mining: {mine_result['message']}")
    
    print("\n📊 Final status:")
    show_status()
    
    # Show the strategic elements
    print("🎯 STRATEGIC ELEMENTS DEMONSTRATED:")
    print("✅ Separate mining and trading locations")
    print("✅ Fuel management affects travel planning")
    print("✅ Different locations offer different opportunities")
    print("✅ Distance vs. reward tradeoffs")
    print("✅ Planning round trips between mining and trading")
    print("✅ Resource scarcity creates strategic choices")
    
    print("\n🏆 SUCCESS! The travel-to-trade mechanics create engaging strategic gameplay!")
    print("Players must now plan their routes, manage fuel, and make strategic decisions")
    print("about which locations to visit and when to trade their cargo.")

if __name__ == "__main__":
    strategic_gameplay_demo()