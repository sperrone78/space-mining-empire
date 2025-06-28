"""
Core game models for Space Mining Empire
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random


class ResourceType(Enum):
    IRON = "Iron"
    COPPER = "Copper"
    TITANIUM = "Titanium"
    GOLD = "Gold"
    RARE_EARTH = "Rare Earth"
    QUANTUM_CRYSTALS = "Quantum Crystals"


@dataclass
class Resource:
    type: ResourceType
    amount: int
    base_value: float
    
    @property
    def total_value(self) -> float:
        return self.amount * self.base_value


@dataclass
class Ship:
    name: str
    cargo_capacity: int
    mining_efficiency: float
    speed: float
    fuel_capacity: int
    current_fuel: int
    cargo: Dict[ResourceType, int] = field(default_factory=dict)
    
    @property
    def cargo_used(self) -> int:
        return sum(self.cargo.values())
    
    @property
    def cargo_free(self) -> int:
        return self.cargo_capacity - self.cargo_used
    
    def add_cargo(self, resource_type: ResourceType, amount: int) -> int:
        space_available = min(amount, self.cargo_free)
        if space_available > 0:
            self.cargo[resource_type] = self.cargo.get(resource_type, 0) + space_available
        return space_available
    
    def remove_cargo(self, resource_type: ResourceType, amount: int) -> int:
        current_amount = self.cargo.get(resource_type, 0)
        removed = min(amount, current_amount)
        if removed > 0:
            self.cargo[resource_type] = current_amount - removed
            if self.cargo[resource_type] == 0:
                del self.cargo[resource_type]
        return removed


@dataclass
class CelestialBody:
    name: str
    distance_from_start: float
    resources: Dict[ResourceType, int]
    mining_difficulty: float = 1.0
    body_type: str = "planet"  # planet, asteroid, moon, station
    has_outpost: bool = False
    outpost: Optional['Outpost'] = None
    has_ship_shop: bool = False  # Ship shops available at major stations
    
    def mine_resource(self, resource_type: ResourceType, mining_power: float) -> int:
        if resource_type not in self.resources or self.resources[resource_type] <= 0:
            return 0
        
        base_yield = mining_power / self.mining_difficulty
        actual_yield = int(random.uniform(base_yield * 0.5, base_yield * 1.5))
        actual_yield = min(actual_yield, self.resources[resource_type])
        
        self.resources[resource_type] -= actual_yield
        return actual_yield


@dataclass
class Outpost:
    name: str
    outpost_type: str  # mining_station, research_facility, trade_hub, etc.
    resource_prices: Dict[ResourceType, float]
    demand_multipliers: Dict[ResourceType, float] = field(default_factory=dict)
    
    def get_sell_price(self, resource_type: ResourceType) -> float:
        base_price = self.resource_prices.get(resource_type, 0)
        multiplier = self.demand_multipliers.get(resource_type, 1.0)
        return base_price * multiplier


@dataclass
class Player:
    name: str
    credits: float
    current_ship: Ship
    ships: List[Ship] = field(default_factory=list)
    current_location: Optional[CelestialBody] = None
    
    def __post_init__(self):
        if self.current_ship not in self.ships:
            self.ships.append(self.current_ship)