#!/usr/bin/env python3
"""
Space Mining Empire Demo - Automated gameplay demonstration
"""

from game.models import Player, Ship, ResourceType
from game.world_generator import WorldGenerator
from game.shop import ShipShop

def main():
    print("=== Space Mining Empire Demo ===")
    
    # Create starting ship
    starter_ship = Ship(
        name="Rusty Prospector",
        cargo_capacity=50,
        mining_efficiency=10.0,
        speed=5.0,
        fuel_capacity=100,
        current_fuel=100
    )
    
    # Create player
    player = Player(
        name="Demo Commander",
        credits=1000.0,
        current_ship=starter_ship
    )
    
    # Generate world
    world_gen = WorldGenerator()
    celestial_bodies = world_gen.generate_starting_system()
    outposts = world_gen.generate_outposts()
    
    player.current_location = celestial_bodies[0]
    
    print(f"\nWelcome, {player.name}!")
    print(f"Starting credits: {player.credits}")
    print(f"Starting location: {player.current_location.name}")
    print(f"Ship: {player.current_ship.name}")
    
    # Demo mining
    print("\n=== Mining Demo ===")
    location = player.current_location
    print(f"Available resources at {location.name}:")
    for resource_type, amount in location.resources.items():
        print(f"  {resource_type.value}: {amount} units")
    
    # Mine some iron
    if ResourceType.IRON in location.resources:
        mined = location.mine_resource(ResourceType.IRON, player.current_ship.mining_efficiency)
        player.current_ship.add_cargo(ResourceType.IRON, mined)
        print(f"Mined {mined} units of Iron")
    
    # Mine some copper
    if ResourceType.COPPER in location.resources:
        mined = location.mine_resource(ResourceType.COPPER, player.current_ship.mining_efficiency)
        player.current_ship.add_cargo(ResourceType.COPPER, mined)
        print(f"Mined {mined} units of Copper")
    
    print(f"Current cargo: {player.current_ship.cargo}")
    
    # Demo trading
    print("\n=== Trading Demo ===")
    outpost = outposts[0]
    print(f"Visiting {outpost.name}")
    
    total_earnings = 0
    for resource_type, amount in list(player.current_ship.cargo.items()):
        price = outpost.get_sell_price(resource_type)
        earnings = amount * price
        total_earnings += earnings
        print(f"Selling {amount} {resource_type.value} at {price:.1f} each = {earnings:.0f} credits")
        player.current_ship.remove_cargo(resource_type, amount)
    
    player.credits += total_earnings
    print(f"Total earnings: {total_earnings:.0f}")
    print(f"New credit balance: {player.credits:.0f}")
    
    # Demo shop
    print("\n=== Ship Shop Demo ===")
    shop = ShipShop()
    
    print("Available upgrades:")
    for upgrade in shop.upgrades:
        affordable = "✓" if shop.can_afford_upgrade(player, upgrade) else "✗"
        print(f"  {upgrade.name}: {upgrade.cost:.0f} credits {affordable}")
    
    print("\nAvailable ships:")
    for ship_blueprint in shop.ships:
        affordable = "✓" if shop.can_afford_ship(player, ship_blueprint) else "✗"
        print(f"  {ship_blueprint.name}: {ship_blueprint.cost:.0f} credits {affordable}")
    
    # Demo travel
    print("\n=== Travel Demo ===")
    if len(celestial_bodies) > 1:
        current_location = player.current_location
        destination = celestial_bodies[1]
        fuel_cost = int(abs(destination.distance_from_start - current_location.distance_from_start) * 10)
        
        print(f"Traveling from {current_location.name} to {destination.name}")
        print(f"Fuel cost: {fuel_cost}")
        
        if player.current_ship.current_fuel >= fuel_cost:
            player.current_ship.current_fuel -= fuel_cost
            player.current_location = destination
            print(f"Successfully traveled to {destination.name}")
            print(f"Remaining fuel: {player.current_ship.current_fuel}")
        else:
            print("Not enough fuel for travel!")
    
    print("\n=== Game Systems Working! ===")
    print("Core features implemented:")
    print("✓ Resource mining with randomized yields")
    print("✓ Cargo management and capacity limits")
    print("✓ Trading system with dynamic pricing")
    print("✓ Ship upgrades and new ship purchases")
    print("✓ Travel between celestial bodies")
    print("✓ Fuel consumption mechanics")
    print("✓ Credit-based economy")

if __name__ == "__main__":
    main()