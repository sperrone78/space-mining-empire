"""
Ship upgrades and purchasing system
"""

from dataclasses import dataclass
from typing import Dict, List
from .models import Ship, Player


@dataclass
class ShipUpgrade:
    name: str
    description: str
    cost: float
    stat_bonus: Dict[str, float]


@dataclass
class ShipBlueprint:
    name: str
    description: str
    cost: float
    stats: Dict[str, float]


class ShipShop:
    def __init__(self):
        self.upgrades = [
            ShipUpgrade(
                name="Cargo Expansion",
                description="Increases cargo capacity by 25 units",
                cost=2000.0,
                stat_bonus={"cargo_capacity": 25}
            ),
            ShipUpgrade(
                name="Mining Laser Mk2",
                description="Improves mining efficiency by 50%",
                cost=3500.0,
                stat_bonus={"mining_efficiency": 0.5}
            ),
            ShipUpgrade(
                name="Fuel Tank Extension",
                description="Increases fuel capacity by 50 units",
                cost=1500.0,
                stat_bonus={"fuel_capacity": 50}
            ),
            ShipUpgrade(
                name="Engine Boost",
                description="Increases ship speed by 2.0",
                cost=2800.0,
                stat_bonus={"speed": 2.0}
            )
        ]
        
        self.ships = [
            ShipBlueprint(
                name="Mining Hauler",
                description="Heavy cargo vessel with large storage",
                cost=15000.0,
                stats={
                    "cargo_capacity": 150,
                    "mining_efficiency": 12.0,
                    "speed": 3.0,
                    "fuel_capacity": 120,
                    "current_fuel": 120
                }
            ),
            ShipBlueprint(
                name="Deep Space Explorer",
                description="Fast ship for reaching distant locations",
                cost=25000.0,
                stats={
                    "cargo_capacity": 80,
                    "mining_efficiency": 15.0,
                    "speed": 8.0,
                    "fuel_capacity": 200,
                    "current_fuel": 200
                }
            ),
            ShipBlueprint(
                name="Industrial Miner",
                description="Specialized mining vessel with high efficiency",
                cost=35000.0,
                stats={
                    "cargo_capacity": 100,
                    "mining_efficiency": 25.0,
                    "speed": 4.0,
                    "fuel_capacity": 150,
                    "current_fuel": 150
                }
            )
        ]
    
    def can_afford_upgrade(self, player: Player, upgrade: ShipUpgrade) -> bool:
        return player.credits >= upgrade.cost
    
    def can_afford_ship(self, player: Player, ship: ShipBlueprint) -> bool:
        return player.credits >= ship.cost
    
    def apply_upgrade(self, ship: Ship, upgrade: ShipUpgrade) -> Ship:
        for stat, bonus in upgrade.stat_bonus.items():
            if stat == "mining_efficiency":
                ship.mining_efficiency += bonus
            elif stat == "cargo_capacity":
                ship.cargo_capacity += int(bonus)
            elif stat == "fuel_capacity":
                ship.fuel_capacity += int(bonus)
                ship.current_fuel += int(bonus)
            elif stat == "speed":
                ship.speed += bonus
        return ship
    
    def create_ship(self, blueprint: ShipBlueprint) -> Ship:
        return Ship(
            name=blueprint.name,
            cargo_capacity=int(blueprint.stats["cargo_capacity"]),
            mining_efficiency=blueprint.stats["mining_efficiency"],
            speed=blueprint.stats["speed"],
            fuel_capacity=int(blueprint.stats["fuel_capacity"]),
            current_fuel=int(blueprint.stats["current_fuel"])
        )