"""
GUI Engine for Space Mining Empire
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
from typing import Dict, List, Optional
import random

from .models import Player, Ship, CelestialBody, Outpost, ResourceType
from .world_generator import WorldGenerator
from .shop import ShipShop


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Mining Empire")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a1a')
        
        # Game state
        self.world_gen = WorldGenerator()
        self.shop = ShipShop()
        self.player = None
        self.celestial_bodies = []
        self.outposts = []
        self.current_turn = 1
        
        # UI variables
        self.status_frame = None
        self.main_frame = None
        self.current_interface = None
        
        # Initialize game
        self.setup_styles()
        self.initialize_game()
        self.create_main_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       foreground='#00ff88',
                       background='#0a0a1a')
        
        style.configure('Header.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground='#88aaff',
                       background='#0a0a1a')
        
        style.configure('Status.TLabel',
                       font=('Arial', 10),
                       foreground='#ffffff',
                       background='#1a1a2e')
        
        style.configure('Game.TButton',
                       font=('Arial', 10, 'bold'),
                       foreground='#ffffff')
        
    def initialize_game(self):
        # Get player name
        player_name = simpledialog.askstring("Welcome", "Enter your commander name:")
        if not player_name:
            player_name = "Commander"
        
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
        self.player = Player(
            name=player_name,
            credits=1000.0,
            current_ship=starter_ship
        )
        
        # Generate world
        self.celestial_bodies = self.world_gen.generate_starting_system()
        self.outposts = self.world_gen.generate_outposts()
        self.player.current_location = self.celestial_bodies[0]
        
    def create_main_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#0a0a1a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_container, 
                               text="SPACE MINING EMPIRE", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Status panel (top)
        self.create_status_panel(main_container)
        
        # Main content area
        self.main_frame = tk.Frame(main_container, bg='#0a0a1a')
        self.main_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Show main menu by default
        self.show_main_menu()
        
    def create_status_panel(self, parent):
        self.status_frame = tk.Frame(parent, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Player info
        info_frame = tk.Frame(self.status_frame, bg='#1a1a2e')
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Left side - player info
        left_info = tk.Frame(info_frame, bg='#1a1a2e')
        left_info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.player_name_label = ttk.Label(left_info, style='Header.TLabel')
        self.player_name_label.pack(anchor=tk.W)
        
        self.credits_label = ttk.Label(left_info, style='Status.TLabel')
        self.credits_label.pack(anchor=tk.W)
        
        self.location_label = ttk.Label(left_info, style='Status.TLabel')
        self.location_label.pack(anchor=tk.W)
        
        # Right side - ship info
        right_info = tk.Frame(info_frame, bg='#1a1a2e')
        right_info.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        self.ship_label = ttk.Label(right_info, style='Header.TLabel')
        self.ship_label.pack(anchor=tk.E)
        
        self.cargo_label = ttk.Label(right_info, style='Status.TLabel')
        self.cargo_label.pack(anchor=tk.E)
        
        self.fuel_label = ttk.Label(right_info, style='Status.TLabel')
        self.fuel_label.pack(anchor=tk.E)
        
        self.update_status_panel()
        
    def update_status_panel(self):
        if not self.player:
            return
            
        self.player_name_label.config(text=f"Commander {self.player.name} - Turn {self.current_turn}")
        self.credits_label.config(text=f"Credits: {self.player.credits:.0f}")
        self.location_label.config(text=f"Location: {self.player.current_location.name}")
        
        ship = self.player.current_ship
        self.ship_label.config(text=f"Ship: {ship.name}")
        self.cargo_label.config(text=f"Cargo: {ship.cargo_used}/{ship.cargo_capacity}")
        self.fuel_label.config(text=f"Fuel: {ship.current_fuel}/{ship.fuel_capacity}")
        
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def show_main_menu(self):
        self.clear_main_frame()
        self.current_interface = "main_menu"
        
        menu_frame = tk.Frame(self.main_frame, bg='#0a0a1a')
        menu_frame.pack(expand=True)
        
        title = ttk.Label(menu_frame, text="Main Menu", style='Header.TLabel')
        title.pack(pady=20)
        
        buttons = [
            ("Mine Resources", self.show_mining_interface),
            ("View Location", self.show_location_info),
            ("Travel", self.show_travel_interface),
            ("Trade at Outpost", self.show_trading_interface),
            ("Ship Shop", self.show_ship_shop),
            ("End Turn", self.end_turn)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(menu_frame, text=text, command=command, style='Game.TButton')
            btn.pack(pady=5, padx=20, fill=tk.X)
            
    def show_mining_interface(self):
        self.clear_main_frame()
        self.current_interface = "mining"
        
        mining_frame = tk.Frame(self.main_frame, bg='#0a0a1a')
        mining_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(mining_frame, text="Mining Operations", style='Header.TLabel')
        title.pack(pady=10)
        
        location = self.player.current_location
        
        # Location info
        info_text = f"Location: {location.name}\nMining Difficulty: {location.mining_difficulty:.1f}x"
        info_label = ttk.Label(mining_frame, text=info_text, style='Status.TLabel')
        info_label.pack(pady=10)
        
        # Available resources
        resources_frame = tk.Frame(mining_frame, bg='#0a0a1a')
        resources_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        ttk.Label(resources_frame, text="Available Resources:", style='Header.TLabel').pack(pady=10)
        
        available_resources = [(rt, amount) for rt, amount in location.resources.items() if amount > 0]
        
        if not available_resources:
            ttk.Label(resources_frame, text="No resources available at this location!", 
                     foreground='red').pack(pady=20)
        else:
            for resource_type, amount in available_resources:
                frame = tk.Frame(resources_frame, bg='#1a1a2e', relief=tk.RAISED, bd=1)
                frame.pack(fill=tk.X, pady=2, padx=10)
                
                info = f"{resource_type.value}: {amount} units available"
                ttk.Label(frame, text=info, style='Status.TLabel').pack(side=tk.LEFT, padx=10, pady=5)
                
                mine_btn = ttk.Button(frame, text="Mine", 
                                    command=lambda rt=resource_type: self.mine_resource(rt),
                                    style='Game.TButton')
                mine_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Back button
        ttk.Button(mining_frame, text="Back to Menu", command=self.show_main_menu,
                  style='Game.TButton').pack(pady=20)
        
    def mine_resource(self, resource_type):
        location = self.player.current_location
        ship = self.player.current_ship
        
        mined_amount = location.mine_resource(resource_type, ship.mining_efficiency)
        
        if mined_amount > 0:
            added_amount = ship.add_cargo(resource_type, mined_amount)
            if added_amount < mined_amount:
                location.resources[resource_type] += (mined_amount - added_amount)
                messagebox.showwarning("Cargo Full", 
                                     f"Cargo full! Only loaded {added_amount} units of {resource_type.value}")
            else:
                messagebox.showinfo("Mining Success", 
                                  f"Mined {added_amount} units of {resource_type.value}!")
        else:
            messagebox.showerror("Mining Failed", 
                               "Mining failed - resource depleted or equipment malfunction!")
        
        self.update_status_panel()
        self.show_mining_interface()  # Refresh the interface
        
    def show_location_info(self):
        location = self.player.current_location
        
        info_text = f"Location: {location.name}\n"
        info_text += f"Distance from start: {location.distance_from_start:.1f} AU\n"
        info_text += f"Mining difficulty: {location.mining_difficulty:.1f}x\n\n"
        info_text += "Available Resources:\n"
        
        for resource_type, amount in location.resources.items():
            if amount > 0:
                info_text += f"• {resource_type.value}: {amount} units\n"
        
        messagebox.showinfo("Location Information", info_text)
        
    def show_travel_interface(self):
        self.clear_main_frame()
        self.current_interface = "travel"
        
        travel_frame = tk.Frame(self.main_frame, bg='#0a0a1a')
        travel_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(travel_frame, text="Space Travel", style='Header.TLabel')
        title.pack(pady=10)
        
        current_location = self.player.current_location
        ship = self.player.current_ship
        
        available_locations = [body for body in self.celestial_bodies if body != current_location]
        
        if not available_locations:
            ttk.Label(travel_frame, text="No other locations available!", 
                     foreground='red').pack(pady=20)
        else:
            ttk.Label(travel_frame, text="Available Destinations:", style='Header.TLabel').pack(pady=10)
            
            destinations_frame = tk.Frame(travel_frame, bg='#0a0a1a')
            destinations_frame.pack(fill=tk.BOTH, expand=True, padx=20)
            
            for body in available_locations:
                fuel_cost = int(abs(body.distance_from_start - current_location.distance_from_start) * 10)
                can_travel = ship.current_fuel >= fuel_cost
                
                frame = tk.Frame(destinations_frame, bg='#1a1a2e', relief=tk.RAISED, bd=1)
                frame.pack(fill=tk.X, pady=2, padx=10)
                
                info = f"{body.name} - Distance: {body.distance_from_start:.1f} AU - Fuel cost: {fuel_cost}"
                color = '#ffffff' if can_travel else '#ff4444'
                
                label = tk.Label(frame, text=info, fg=color, bg='#1a1a2e', font=('Arial', 10))
                label.pack(side=tk.LEFT, padx=10, pady=5)
                
                travel_btn = ttk.Button(frame, text="Travel", 
                                      command=lambda dest=body: self.travel_to(dest),
                                      style='Game.TButton')
                travel_btn.pack(side=tk.RIGHT, padx=10, pady=5)
                
                if not can_travel:
                    travel_btn.config(state='disabled')
        
        ttk.Button(travel_frame, text="Back to Menu", command=self.show_main_menu,
                  style='Game.TButton').pack(pady=20)
                  
    def travel_to(self, destination):
        current_location = self.player.current_location
        ship = self.player.current_ship
        
        fuel_cost = int(abs(destination.distance_from_start - current_location.distance_from_start) * 10)
        
        if ship.current_fuel < fuel_cost:
            messagebox.showerror("Insufficient Fuel", 
                               f"Not enough fuel! Need {fuel_cost}, have {ship.current_fuel}")
            return
        
        ship.current_fuel -= fuel_cost
        self.player.current_location = destination
        
        messagebox.showinfo("Travel Complete", 
                          f"Traveled to {destination.name}! Used {fuel_cost} fuel.\nRemaining fuel: {ship.current_fuel}")
        
        self.update_status_panel()
        self.show_main_menu()
        
    def show_trading_interface(self):
        if not self.player.current_ship.cargo:
            messagebox.showwarning("No Cargo", "You have no cargo to trade!")
            return
            
        self.clear_main_frame()
        self.current_interface = "trading"
        
        trading_frame = tk.Frame(self.main_frame, bg='#0a0a1a')
        trading_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(trading_frame, text="Trading Post", style='Header.TLabel')
        title.pack(pady=10)
        
        ttk.Label(trading_frame, text="Select an outpost:", style='Header.TLabel').pack(pady=10)
        
        outposts_frame = tk.Frame(trading_frame, bg='#0a0a1a')
        outposts_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        for outpost in self.outposts:
            frame = tk.Frame(outposts_frame, bg='#1a1a2e', relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=2, padx=10)
            
            info = f"{outpost.name} ({outpost.location})"
            ttk.Label(frame, text=info, style='Status.TLabel').pack(side=tk.LEFT, padx=10, pady=5)
            
            visit_btn = ttk.Button(frame, text="Visit", 
                                 command=lambda o=outpost: self.visit_outpost(o),
                                 style='Game.TButton')
            visit_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        ttk.Button(trading_frame, text="Back to Menu", command=self.show_main_menu,
                  style='Game.TButton').pack(pady=20)
                  
    def visit_outpost(self, outpost):
        self.clear_main_frame()
        
        outpost_frame = tk.Frame(self.main_frame, bg='#0a0a1a')
        outpost_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(outpost_frame, text=f"Welcome to {outpost.name}!", style='Header.TLabel')
        title.pack(pady=10)
        
        # Show cargo and prices
        cargo_frame = tk.Frame(outpost_frame, bg='#0a0a1a')
        cargo_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        ttk.Label(cargo_frame, text="Your Cargo - Trading Prices:", style='Header.TLabel').pack(pady=10)
        
        total_value = 0
        for resource_type, amount in self.player.current_ship.cargo.items():
            price = outpost.get_sell_price(resource_type)
            value = amount * price
            total_value += value
            
            frame = tk.Frame(cargo_frame, bg='#1a1a2e', relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=2, padx=10)
            
            info = f"{resource_type.value}: {amount} units @ {price:.1f} = {value:.0f} credits"
            ttk.Label(frame, text=info, style='Status.TLabel').pack(side=tk.LEFT, padx=10, pady=5)
            
            sell_btn = ttk.Button(frame, text="Sell All", 
                                command=lambda rt=resource_type: self.sell_resource(outpost, rt),
                                style='Game.TButton')
            sell_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Total value and sell all button
        total_frame = tk.Frame(outpost_frame, bg='#1a1a2e', relief=tk.RAISED, bd=2)
        total_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(total_frame, text=f"Total Value: {total_value:.0f} credits", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=10, pady=10)
        
        sell_all_btn = ttk.Button(total_frame, text="Sell Everything", 
                                command=lambda: self.sell_all_cargo(outpost),
                                style='Game.TButton')
        sell_all_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        ttk.Button(outpost_frame, text="Back", command=self.show_trading_interface,
                  style='Game.TButton').pack(pady=20)
                  
    def sell_resource(self, outpost, resource_type):
        amount = self.player.current_ship.cargo.get(resource_type, 0)
        if amount == 0:
            return
            
        price = outpost.get_sell_price(resource_type)
        earnings = amount * price
        
        self.player.current_ship.remove_cargo(resource_type, amount)
        self.player.credits += earnings
        
        messagebox.showinfo("Sale Complete", 
                          f"Sold {amount} {resource_type.value} for {earnings:.0f} credits!")
        
        self.update_status_panel()
        
        if self.player.current_ship.cargo:
            self.visit_outpost(outpost)  # Refresh if still have cargo
        else:
            self.show_main_menu()  # Go back if no cargo left
            
    def sell_all_cargo(self, outpost):
        total_earnings = 0
        sold_items = []
        
        for resource_type in list(self.player.current_ship.cargo.keys()):
            amount = self.player.current_ship.remove_cargo(resource_type, 
                                                         self.player.current_ship.cargo[resource_type])
            earnings = amount * outpost.get_sell_price(resource_type)
            total_earnings += earnings
            sold_items.append(f"{amount} {resource_type.value}")
        
        self.player.credits += total_earnings
        
        items_text = ", ".join(sold_items)
        messagebox.showinfo("Sale Complete", 
                          f"Sold all cargo: {items_text}\nTotal earnings: {total_earnings:.0f} credits!")
        
        self.update_status_panel()
        self.show_main_menu()
        
    def show_ship_shop(self):
        self.clear_main_frame()
        self.current_interface = "ship_shop"
        
        shop_frame = tk.Frame(self.main_frame, bg='#0a0a1a')
        shop_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(shop_frame, text="Ship Shop", style='Header.TLabel')
        title.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(shop_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Upgrades tab
        upgrades_frame = tk.Frame(notebook, bg='#0a0a1a')
        notebook.add(upgrades_frame, text="Upgrades")
        
        self.create_upgrades_tab(upgrades_frame)
        
        # Ships tab
        ships_frame = tk.Frame(notebook, bg='#0a0a1a')
        notebook.add(ships_frame, text="New Ships")
        
        self.create_ships_tab(ships_frame)
        
        ttk.Button(shop_frame, text="Back to Menu", command=self.show_main_menu,
                  style='Game.TButton').pack(pady=20)
                  
    def create_upgrades_tab(self, parent):
        ttk.Label(parent, text="Ship Upgrades", style='Header.TLabel').pack(pady=10)
        
        for upgrade in self.shop.upgrades:
            frame = tk.Frame(parent, bg='#1a1a2e', relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=2, padx=10)
            
            can_afford = self.shop.can_afford_upgrade(self.player, upgrade)
            color = '#ffffff' if can_afford else '#ff4444'
            
            info = f"{upgrade.name}: {upgrade.description}\nCost: {upgrade.cost:.0f} credits"
            label = tk.Label(frame, text=info, fg=color, bg='#1a1a2e', 
                           font=('Arial', 10), justify=tk.LEFT)
            label.pack(side=tk.LEFT, padx=10, pady=5)
            
            buy_btn = ttk.Button(frame, text="Buy", 
                               command=lambda u=upgrade: self.buy_upgrade(u),
                               style='Game.TButton')
            buy_btn.pack(side=tk.RIGHT, padx=10, pady=5)
            
            if not can_afford:
                buy_btn.config(state='disabled')
                
    def create_ships_tab(self, parent):
        ttk.Label(parent, text="New Ships", style='Header.TLabel').pack(pady=10)
        
        for ship_blueprint in self.shop.ships:
            frame = tk.Frame(parent, bg='#1a1a2e', relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=2, padx=10)
            
            can_afford = self.shop.can_afford_ship(self.player, ship_blueprint)
            color = '#ffffff' if can_afford else '#ff4444'
            
            stats = ship_blueprint.stats
            info = f"{ship_blueprint.name}: {ship_blueprint.description}\n"
            info += f"Cargo: {stats['cargo_capacity']}, Mining: {stats['mining_efficiency']}, "
            info += f"Speed: {stats['speed']}, Fuel: {stats['fuel_capacity']}\n"
            info += f"Cost: {ship_blueprint.cost:.0f} credits"
            
            label = tk.Label(frame, text=info, fg=color, bg='#1a1a2e', 
                           font=('Arial', 10), justify=tk.LEFT)
            label.pack(side=tk.LEFT, padx=10, pady=5)
            
            buy_btn = ttk.Button(frame, text="Buy", 
                               command=lambda s=ship_blueprint: self.buy_ship(s),
                               style='Game.TButton')
            buy_btn.pack(side=tk.RIGHT, padx=10, pady=5)
            
            if not can_afford:
                buy_btn.config(state='disabled')
                
    def buy_upgrade(self, upgrade):
        if not self.shop.can_afford_upgrade(self.player, upgrade):
            messagebox.showerror("Insufficient Credits", 
                               f"Not enough credits! Need {upgrade.cost:.0f}, have {self.player.credits:.0f}")
            return
        
        self.player.credits -= upgrade.cost
        self.shop.apply_upgrade(self.player.current_ship, upgrade)
        
        messagebox.showinfo("Upgrade Complete", 
                          f"Purchased {upgrade.name}!\nCredits remaining: {self.player.credits:.0f}")
        
        self.update_status_panel()
        self.show_ship_shop()  # Refresh
        
    def buy_ship(self, ship_blueprint):
        if not self.shop.can_afford_ship(self.player, ship_blueprint):
            messagebox.showerror("Insufficient Credits", 
                               f"Not enough credits! Need {ship_blueprint.cost:.0f}, have {self.player.credits:.0f}")
            return
        
        self.player.credits -= ship_blueprint.cost
        new_ship = self.shop.create_ship(ship_blueprint)
        self.player.ships.append(new_ship)
        
        # Ask if they want to switch to the new ship
        if messagebox.askyesno("Ship Purchased", 
                             f"Purchased {new_ship.name}!\nWould you like to switch to this ship now?"):
            self.player.current_ship = new_ship
        
        messagebox.showinfo("Purchase Complete", 
                          f"Credits remaining: {self.player.credits:.0f}")
        
        self.update_status_panel()
        self.show_ship_shop()  # Refresh
        
    def end_turn(self):
        self.current_turn += 1
        messagebox.showinfo("Turn Complete", f"Turn {self.current_turn} begins!")
        self.update_status_panel()