"""
World and content generation for Space Mining Empire
"""

import random
from typing import List, Dict
from .models import CelestialBody, Outpost, ResourceType


class WorldGenerator:
    def __init__(self):
        self.resource_base_values = {
            ResourceType.IRON: 2.0,
            ResourceType.COPPER: 3.5,
            ResourceType.TITANIUM: 8.0,
            ResourceType.GOLD: 15.0,
            ResourceType.RARE_EARTH: 25.0,
            ResourceType.QUANTUM_CRYSTALS: 100.0
        }
    
    def generate_starting_system(self) -> List[CelestialBody]:
        bodies = []
        
        # Starting planet - good for initial mining, no outpost
        starter_planet = CelestialBody(
            name="Kepler-442b",
            distance_from_start=0.0,
            resources={
                ResourceType.IRON: random.randint(50, 100),
                ResourceType.COPPER: random.randint(30, 60),
                ResourceType.TITANIUM: random.randint(10, 25)
            },
            mining_difficulty=0.8,
            body_type="planet",
            has_outpost=False
        )
        bodies.append(starter_planet)
        
        # Space station with trading post - close but no mining
        space_station = CelestialBody(
            name="Frontier Station",
            distance_from_start=1.5,
            resources={},  # No mining resources at stations
            mining_difficulty=0.0,
            body_type="station",
            has_outpost=True,
            has_ship_shop=True  # Main station has ship shop
        )
        
        # Create mining station outpost
        mining_station = Outpost(
            name="Frontier Trading Post",
            outpost_type="mining_station",
            resource_prices={
                ResourceType.IRON: 2.5,
                ResourceType.COPPER: 4.0,
                ResourceType.TITANIUM: 9.0,
                ResourceType.GOLD: 16.0,
                ResourceType.RARE_EARTH: 28.0,
                ResourceType.QUANTUM_CRYSTALS: 110.0
            },
            demand_multipliers={
                ResourceType.IRON: 1.2,
                ResourceType.COPPER: 1.1,
                ResourceType.TITANIUM: 0.9
            }
        )
        space_station.outpost = mining_station
        bodies.append(space_station)
        
        # Rich asteroid field - good mining, no trading
        asteroid_field = CelestialBody(
            name="Asteroid Belt Alpha",
            distance_from_start=3.2,
            resources={
                ResourceType.IRON: random.randint(100, 200),
                ResourceType.COPPER: random.randint(60, 120),
                ResourceType.GOLD: random.randint(15, 30),
                ResourceType.TITANIUM: random.randint(20, 40)
            },
            mining_difficulty=1.1,
            body_type="asteroid",
            has_outpost=False
        )
        bodies.append(asteroid_field)
        
        # Distant research facility - high prices but far
        research_moon = CelestialBody(
            name="Titan-VII Research Base",
            distance_from_start=6.8,
            resources={
                ResourceType.RARE_EARTH: random.randint(5, 15),  # Small mining opportunity
                ResourceType.QUANTUM_CRYSTALS: random.randint(1, 3)
            },
            mining_difficulty=2.0,
            body_type="moon",
            has_outpost=True,
            has_ship_shop=True  # Research facility also has ship shop
        )
        
        # Create research facility outpost
        research_facility = Outpost(
            name="Deep Space Research Facility",
            outpost_type="research_facility",
            resource_prices={
                ResourceType.IRON: 3.0,    # Higher prices due to distance
                ResourceType.COPPER: 5.0,
                ResourceType.TITANIUM: 12.0,
                ResourceType.GOLD: 22.0,
                ResourceType.RARE_EARTH: 40.0,
                ResourceType.QUANTUM_CRYSTALS: 180.0
            },
            demand_multipliers={
                ResourceType.RARE_EARTH: 1.8,
                ResourceType.QUANTUM_CRYSTALS: 2.0,
                ResourceType.TITANIUM: 1.5
            }
        )
        research_moon.outpost = research_facility
        bodies.append(research_moon)
        
        # Remote high-value mining location - rare resources, no trading
        outer_planet = CelestialBody(
            name="Xerion Prime",
            distance_from_start=8.5,
            resources={
                ResourceType.RARE_EARTH: random.randint(30, 60),
                ResourceType.QUANTUM_CRYSTALS: random.randint(8, 15),
                ResourceType.GOLD: random.randint(25, 50)
            },
            mining_difficulty=2.5,
            body_type="planet",
            has_outpost=False
        )
        bodies.append(outer_planet)
        
        return bodies
    
    def get_outposts_from_bodies(self, bodies: List[CelestialBody]) -> List[CelestialBody]:
        """Returns list of celestial bodies that have outposts"""
        return [body for body in bodies if body.has_outpost]