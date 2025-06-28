"""
Web Engine for Space Mining Empire
"""

from typing import Dict, List, Optional
import random

from .models import Player, Ship, CelestialBody, Outpost, ResourceType
from .world_generator import WorldGenerator
from .shop import ShipShop


class GameWebEngine:
    def __init__(self):
        self.world_gen = WorldGenerator()
        self.shop = ShipShop()
        self.player = None
        self.celestial_bodies = []
        self.outposts = []
        self.settings = {
            'starting_credits': 1000.0
        }
        # Don't auto-initialize - wait for user to start new game
        # self.initialize_game()
        
    def initialize_game(self, starting_credits=None):
        if starting_credits is not None:
            self.settings['starting_credits'] = starting_credits
        
        # Create starting ship
        starter_ship = Ship(
            name="Rusty Prospector",
            cargo_capacity=50,
            mining_efficiency=10.0,
            speed=5.0,
            fuel_capacity=100,
            current_fuel=100
        )
        
        # Create player with configurable starting credits
        self.player = Player(
            name="Commander",
            credits=self.settings['starting_credits'],
            current_ship=starter_ship
        )
        
        # Generate world
        self.celestial_bodies = self.world_gen.generate_starting_system()
        self.player.current_location = self.celestial_bodies[0]
    
    def is_initialized(self):
        return self.player is not None
    
    def get_status(self):
        if not self.is_initialized():
            return {'error': 'Game not initialized'}
        
        ship = self.player.current_ship
        return {
            'player_name': self.player.name,
            'credits': self.player.credits,
            'location': self.player.current_location.name,
            'ship_name': ship.name,
            'cargo_used': ship.cargo_used,
            'cargo_capacity': ship.cargo_capacity,
            'current_fuel': ship.current_fuel,
            'fuel_capacity': ship.fuel_capacity,
            'cargo': {rt.value: amount for rt, amount in ship.cargo.items()}
        }
    
    def get_location_info(self):
        if not self.is_initialized():
            return {'error': 'Game not initialized'}
            
        location = self.player.current_location
        return {
            'name': location.name,
            'distance': location.distance_from_start,
            'mining_difficulty': location.mining_difficulty,
            'body_type': location.body_type,
            'has_outpost': location.has_outpost,
            'outpost_name': location.outpost.name if location.outpost else None,
            'outpost_type': location.outpost.outpost_type if location.outpost else None,
            'has_ship_shop': location.has_ship_shop,
            'resources': {rt.value: amount for rt, amount in location.resources.items() if amount > 0}
        }
    
    def get_outposts(self):
        # Only return the outpost at current location (if any)
        current_location = self.player.current_location
        
        if not current_location.has_outpost or not current_location.outpost:
            return None
        
        outpost = current_location.outpost
        cargo_prices = []
        total_value = 0
        
        for resource_type, amount in self.player.current_ship.cargo.items():
            price = outpost.get_sell_price(resource_type)
            value = amount * price
            total_value += value
            cargo_prices.append({
                'resource': resource_type.value,
                'amount': amount,
                'price': price,
                'value': value
            })
        
        return {
            'name': outpost.name,
            'outpost_type': outpost.outpost_type,
            'location_name': current_location.name,
            'cargo_prices': cargo_prices,
            'total_value': total_value
        }
    
    def get_shop_data(self):
        upgrades = []
        for i, upgrade in enumerate(self.shop.upgrades):
            upgrades.append({
                'index': i,
                'name': upgrade.name,
                'description': upgrade.description,
                'cost': upgrade.cost,
                'affordable': self.shop.can_afford_upgrade(self.player, upgrade)
            })
        
        ships = []
        for i, ship_blueprint in enumerate(self.shop.ships):
            ships.append({
                'index': i,
                'name': ship_blueprint.name,
                'description': ship_blueprint.description,
                'cost': ship_blueprint.cost,
                'stats': ship_blueprint.stats,
                'affordable': self.shop.can_afford_ship(self.player, ship_blueprint)
            })
        
        return {
            'upgrades': upgrades,
            'ships': ships,
            'player_ships': [ship.name for ship in self.player.ships],
            'current_ship': self.player.current_ship.name
        }
    
    def get_destinations(self):
        current_location = self.player.current_location
        ship = self.player.current_ship
        
        destinations = []
        for i, body in enumerate(self.celestial_bodies):
            if body != current_location:
                fuel_cost = int(abs(body.distance_from_start - current_location.distance_from_start) * 10)
                destinations.append({
                    'index': i,
                    'name': body.name,
                    'distance': body.distance_from_start,
                    'body_type': body.body_type,
                    'has_outpost': body.has_outpost,
                    'outpost_name': body.outpost.name if body.outpost else None,
                    'has_ship_shop': body.has_ship_shop,
                    'fuel_cost': fuel_cost,
                    'can_travel': ship.current_fuel >= fuel_cost,
                    'has_resources': len(body.resources) > 0
                })
        
        return destinations
    
    def mine_resource(self, resource_type_name):
        try:
            resource_type = ResourceType(resource_type_name)
        except ValueError:
            return {'success': False, 'message': 'Invalid resource type'}
        
        location = self.player.current_location
        ship = self.player.current_ship
        
        if resource_type not in location.resources or location.resources[resource_type] <= 0:
            return {'success': False, 'message': 'Resource not available'}
        
        mined_amount = location.mine_resource(resource_type, ship.mining_efficiency)
        
        if mined_amount > 0:
            added_amount = ship.add_cargo(resource_type, mined_amount)
            if added_amount < mined_amount:
                location.resources[resource_type] += (mined_amount - added_amount)
                return {
                    'success': True, 
                    'message': f'Cargo full! Only loaded {added_amount} units of {resource_type.value}',
                    'partial': True
                }
            else:
                return {
                    'success': True, 
                    'message': f'Mined {added_amount} units of {resource_type.value}!'
                }
        else:
            return {'success': False, 'message': 'Mining failed - resource depleted or equipment malfunction!'}
    
    def travel_to(self, destination_index):
        if destination_index >= len(self.celestial_bodies):
            return {'success': False, 'message': 'Invalid destination'}
        
        current_location = self.player.current_location
        destination = self.celestial_bodies[destination_index]
        
        if destination == current_location:
            return {'success': False, 'message': 'Already at this location'}
        
        ship = self.player.current_ship
        fuel_cost = int(abs(destination.distance_from_start - current_location.distance_from_start) * 10)
        
        if ship.current_fuel < fuel_cost:
            return {
                'success': False, 
                'message': f'Not enough fuel! Need {fuel_cost}, have {ship.current_fuel}'
            }
        
        ship.current_fuel -= fuel_cost
        self.player.current_location = destination
        
        return {
            'success': True,
            'message': f'Traveled to {destination.name}! Used {fuel_cost} fuel.',
            'remaining_fuel': ship.current_fuel
        }
    
    def trade_at_outpost(self, resource_type_name=None, sell_all=False):
        current_location = self.player.current_location
        
        if not current_location.has_outpost or not current_location.outpost:
            return {'success': False, 'message': 'No trading outpost at this location! You must travel to a location with an outpost to trade.'}
        
        outpost = current_location.outpost
        
        if not self.player.current_ship.cargo:
            return {'success': False, 'message': 'No cargo to trade'}
        
        if sell_all:
            total_earnings = 0
            sold_items = []
            
            for resource_type in list(self.player.current_ship.cargo.keys()):
                amount = self.player.current_ship.remove_cargo(resource_type, 
                                                             self.player.current_ship.cargo[resource_type])
                earnings = amount * outpost.get_sell_price(resource_type)
                total_earnings += earnings
                sold_items.append(f"{amount} {resource_type.value}")
            
            self.player.credits += total_earnings
            
            return {
                'success': True,
                'message': f"Sold all cargo at {outpost.name} for {total_earnings:.0f} credits!",
                'earnings': total_earnings,
                'items': sold_items
            }
        
        elif resource_type_name:
            try:
                resource_type = ResourceType(resource_type_name)
            except ValueError:
                return {'success': False, 'message': 'Invalid resource type'}
            
            amount = self.player.current_ship.cargo.get(resource_type, 0)
            if amount == 0:
                return {'success': False, 'message': 'No cargo of this type'}
            
            removed_amount = self.player.current_ship.remove_cargo(resource_type, amount)
            earnings = removed_amount * outpost.get_sell_price(resource_type)
            self.player.credits += earnings
            
            return {
                'success': True,
                'message': f'Sold {removed_amount} {resource_type.value} at {outpost.name} for {earnings:.0f} credits!',
                'earnings': earnings
            }
        
        return {'success': False, 'message': 'No action specified'}
    
    def buy_from_shop(self, item_type, item_index):
        if item_type == 'upgrade':
            if item_index >= len(self.shop.upgrades):
                return {'success': False, 'message': 'Invalid upgrade'}
            
            upgrade = self.shop.upgrades[item_index]
            
            if not self.shop.can_afford_upgrade(self.player, upgrade):
                return {
                    'success': False, 
                    'message': f'Not enough credits! Need {upgrade.cost:.0f}, have {self.player.credits:.0f}'
                }
            
            self.player.credits -= upgrade.cost
            self.shop.apply_upgrade(self.player.current_ship, upgrade)
            
            return {
                'success': True,
                'message': f'Purchased {upgrade.name}! Credits remaining: {self.player.credits:.0f}'
            }
        
        elif item_type == 'ship':
            if item_index >= len(self.shop.ships):
                return {'success': False, 'message': 'Invalid ship'}
            
            ship_blueprint = self.shop.ships[item_index]
            
            if not self.shop.can_afford_ship(self.player, ship_blueprint):
                return {
                    'success': False, 
                    'message': f'Not enough credits! Need {ship_blueprint.cost:.0f}, have {self.player.credits:.0f}'
                }
            
            self.player.credits -= ship_blueprint.cost
            new_ship = self.shop.create_ship(ship_blueprint)
            self.player.ships.append(new_ship)
            
            return {
                'success': True,
                'message': f'Purchased {new_ship.name}! Credits remaining: {self.player.credits:.0f}',
                'new_ship': new_ship.name
            }
        
        return {'success': False, 'message': 'Invalid item type'}
    
