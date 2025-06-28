# Space Mining Empire

A sci-fi resource management game where you build a mining empire across the galaxy!

## Overview

You start as a space prospector with a basic mining vessel and limited resources. Your goal is to:
- Mine valuable resources from celestial bodies
- Trade resources for profit at outposts
- Upgrade your ships and buy new vessels
- Explore distant locations with rarer, more valuable resources
- Build your economic empire across the galaxy

## Game Features

### ✅ Currently Implemented
- **Start Screen & Settings**: New game setup with customizable starting credits
- **Location-Based UI**: Interface adapts based on available facilities at each location
- **Strategic Travel-to-Trade**: Mining and trading separated by location for strategic gameplay
- **Resource Mining**: Extract materials from planets, asteroids, and moons
- **Trading System**: Sell resources at specific outpost locations with dynamic pricing
- **Ship Management**: Upgrade existing ships or purchase new vessels at ship shops
- **Space Travel**: Navigate between celestial bodies (fuel required)
- **Economic Progression**: Start small and build your mining empire
- **Resource Types**: Iron, Copper, Titanium, Gold, Rare Earth, Quantum Crystals

### 🚧 Future Features
- **NPC Interactions**: Form relationships and negotiate contracts
- **Dynamic Economy**: Supply and demand affects pricing
- **Random Events**: Pirates, asteroid storms, equipment failures
- **Base Building**: Establish your own mining outposts
- **Fleet Management**: Control multiple ships simultaneously

## How to Play

### Installation
```bash
# Clone or download the game files
cd space_mining_empire

# Install dependencies (if available)
pip install rich

# Run the terminal version
python3 main.py

# Run the web UI version (recommended)
python3 web_main.py
# Then open http://localhost:8080 in your browser

# Or run the demo to see all features
python3 demo.py

# See strategic travel-to-trade gameplay
python3 strategic_demo.py

# Demo new start screen and location-based UI features
python3 demo_start_screen.py
```

### Game Controls

#### Start Screen
1. **New Game**: Start fresh with customizable settings
2. **Continue Game**: Resume saved game (coming soon) 
3. **Settings**: Configure starting credits (500-10,000 range)

#### In-Game (Location-Based)
The available options change based on your current location's facilities:

**At Mining Locations** (planets, asteroids):
- **Mine Resources**: Extract materials from your current location
- **View Location**: Check available resources and mining difficulty
- **Travel**: Move between celestial bodies

**At Trading Outposts** (stations, research facilities):
- **Trading Post**: Sell your cargo for credits
- **View Location**: Check outpost information and prices
- **Travel**: Move between celestial bodies

**At Ship Shop Locations** (major stations):
- **Ship Shop**: Buy upgrades or new ships to improve your capabilities
- **View Location**: Check available services
- **Travel**: Move between celestial bodies

**Available Everywhere**:
- **End Turn**: Progress to next turn

### Tips for Success
- **Mine first, travel to trade**: Start by mining Iron and Copper on your starting planet, then travel to Frontier Station to sell
- **Plan your fuel usage**: Calculate round-trip fuel costs before traveling to distant locations
- **Strategic location selection**: 
  - Kepler-442b: Good starter mining (Iron, Copper, Titanium)
  - Frontier Station: Close trading post with fair prices
  - Asteroid Belt Alpha: Rich mining with no trading (Iron, Copper, Gold, Titanium)
  - Titan-VII Research Base: Distant but high prices for rare materials
  - Xerion Prime: Richest mining for rare resources (Gold, Rare Earth, Quantum Crystals)
- **Optimize your routes**: Mine at resource-rich locations, then travel back to outposts to sell
- **Manage cargo vs fuel**: Balance how much you can carry vs. fuel needed for return trips
- **Upgrade strategically**: Fuel tank upgrades let you reach distant valuable locations

## Game Mechanics

### Strategic Travel-to-Trade System
- **Separated Mining and Trading**: You must travel between locations to mine and sell
- **Location Types**:
  - **Planets**: Rich in basic and rare resources, no trading
  - **Asteroids**: Concentrated mining opportunities, no trading  
  - **Stations**: Trading outposts with no mining resources
  - **Research Bases**: Both limited mining and high-value trading

### Mining
- Each location has different resources and mining difficulty
- Your ship's mining efficiency affects yield
- Resources are finite and will eventually deplete
- Distant locations have rarer, more valuable resources

### Trading
- Only available at specific outpost locations (stations and research facilities)
- Must carry cargo from mining locations to trading outposts
- Different outposts offer different prices and demand multipliers
- Research facilities pay premium prices but are farther away

### Fuel Management
- Essential strategic resource for space travel
- Fuel cost = distance between locations × 10
- Must plan round trips: mine → travel to outpost → sell → return
- Fuel upgrades unlock access to distant valuable locations

### Ships & Upgrades
- **Cargo Expansion**: Increase storage capacity
- **Mining Laser**: Improve mining efficiency
- **Fuel Tank**: Travel further without refueling
- **Engine Boost**: Increase ship speed

### Available Ships
- **Rusty Prospector**: Starting ship (basic stats)
- **Mining Hauler**: Large cargo capacity
- **Deep Space Explorer**: High speed and fuel capacity
- **Industrial Miner**: Maximum mining efficiency

## User Interfaces

The game includes multiple interface options:

### 🌐 Web UI (Recommended)
- **File**: `web_main.py`
- **Features**: Full-featured web interface with modern styling
- **Benefits**: Works on any system with Python, no additional dependencies
- **Access**: Run the server and open http://localhost:8080 in your browser

### 💻 Terminal UI  
- **File**: `main.py`
- **Features**: Rich terminal interface with colors and tables
- **Benefits**: Lightweight, works in any terminal
- **Requires**: `rich` library for best experience

### 🔧 Demo Mode
- **File**: `demo.py`
- **Features**: Automated gameplay demonstration
- **Benefits**: Shows all game mechanics without user input

## File Structure
```
space_mining_empire/
├── main.py              # Terminal game entry point
├── web_main.py          # Web UI entry point
├── gui_main.py          # GUI entry point (requires tkinter)
├── demo.py              # Automated demo
├── strategic_demo.py    # Strategic gameplay demonstration  
├── demo_start_screen.py # Start screen and location-based UI demo
├── test_web_api.py      # API functionality test
├── test_travel_trade.py # Travel-to-trade mechanics test
├── test_start_screen.py # Start screen features test
├── game.html            # Web UI interface
├── requirements.txt     # Python dependencies
├── game/
│   ├── __init__.py
│   ├── models.py        # Core game classes
│   ├── engine.py        # Terminal game engine
│   ├── gui_engine.py    # GUI game engine
│   ├── web_engine.py    # Web API game engine
│   ├── world_generator.py # World/content generation
│   └── shop.py          # Ship upgrades and purchases
└── README.md           # This file
```

## Technical Details

- **Language**: Python 3
- **UI Options**: Web UI (HTML/CSS/JS), Terminal UI (Rich library), GUI (tkinter)
- **Architecture**: Object-oriented design with modular game engines
- **Data**: Uses Python dataclasses for game entities
- **API**: RESTful API for web interface communication

The game provides multiple interface options to suit different preferences and environments, from modern web browsers to classic terminal interfaces.

Enjoy building your space mining empire! 🚀⛏️