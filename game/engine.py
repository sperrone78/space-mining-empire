"""
Main game engine for Space Mining Empire
"""

from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

from .models import Player, Ship, CelestialBody, Outpost, ResourceType
from .world_generator import WorldGenerator
from .shop import ShipShop


class GameEngine:
    def __init__(self):
        self.console = Console()
        self.world_gen = WorldGenerator()
        self.shop = ShipShop()
        self.player = None
        self.celestial_bodies = []
        self.outposts = []
        self.current_turn = 1
        
    def initialize_game(self):
        self.console.print("[bold blue]Welcome to Space Mining Empire![/bold blue]")
        self.console.print("You are a space prospector starting with a basic mining vessel.")
        self.console.print("Mine resources, trade them for profit, and build your empire!")
        
        player_name = Prompt.ask("What is your name, commander?")
        
        starter_ship = Ship(
            name="Rusty Prospector",
            cargo_capacity=50,
            mining_efficiency=10.0,
            speed=5.0,
            fuel_capacity=100,
            current_fuel=100
        )
        
        self.player = Player(
            name=player_name,
            credits=1000.0,
            current_ship=starter_ship
        )
        
        self.celestial_bodies = self.world_gen.generate_starting_system()
        self.player.current_location = self.celestial_bodies[0]
        
        self.console.print(f"\n[green]Welcome aboard, Commander {player_name}![/green]")
        self.console.print(f"You start at {self.player.current_location.name} with {self.player.credits} credits.")
    
    def display_status(self):
        table = Table(title=f"Commander {self.player.name} - Turn {self.current_turn}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Credits", f"{self.player.credits:.0f}")
        table.add_row("Current Ship", self.player.current_ship.name)
        table.add_row("Location", self.player.current_location.name)
        table.add_row("Cargo", f"{self.player.current_ship.cargo_used}/{self.player.current_ship.cargo_capacity}")
        table.add_row("Fuel", f"{self.player.current_ship.current_fuel}/{self.player.current_ship.fuel_capacity}")
        
        self.console.print(table)
        
        if self.player.current_ship.cargo:
            cargo_table = Table(title="Current Cargo")
            cargo_table.add_column("Resource", style="green")
            cargo_table.add_column("Amount", style="yellow")
            
            for resource_type, amount in self.player.current_ship.cargo.items():
                cargo_table.add_row(resource_type.value, str(amount))
            
            self.console.print(cargo_table)
    
    def display_location_info(self):
        location = self.player.current_location
        
        panel_content = f"[bold]{location.name}[/bold]\n"
        panel_content += f"Distance from start: {location.distance_from_start:.1f} AU\n"
        panel_content += f"Mining difficulty: {location.mining_difficulty:.1f}x\n\n"
        panel_content += "[bold]Available Resources:[/bold]\n"
        
        for resource_type, amount in location.resources.items():
            if amount > 0:
                panel_content += f"• {resource_type.value}: {amount} units\n"
        
        self.console.print(Panel(panel_content, title="Current Location"))
    
    def mine_resources(self):
        location = self.player.current_location
        ship = self.player.current_ship
        
        available_resources = [rt for rt, amount in location.resources.items() if amount > 0]
        
        if not available_resources:
            self.console.print("[red]No resources available at this location![/red]")
            return
        
        self.console.print("Available resources to mine:")
        for i, resource_type in enumerate(available_resources, 1):
            amount = location.resources[resource_type]
            self.console.print(f"{i}. {resource_type.value} ({amount} available)")
        
        choice = IntPrompt.ask(
            "Which resource would you like to mine? (0 to cancel)",
            choices=[str(i) for i in range(len(available_resources) + 1)]
        )
        
        if choice == 0:
            return
        
        resource_type = available_resources[choice - 1]
        mined_amount = location.mine_resource(resource_type, ship.mining_efficiency)
        
        if mined_amount > 0:
            added_amount = ship.add_cargo(resource_type, mined_amount)
            if added_amount < mined_amount:
                location.resources[resource_type] += (mined_amount - added_amount)
                self.console.print(f"[yellow]Cargo full! Only loaded {added_amount} units of {resource_type.value}[/yellow]")
            else:
                self.console.print(f"[green]Mined {added_amount} units of {resource_type.value}![/green]")
        else:
            self.console.print("[red]Mining failed - resource depleted or equipment malfunction![/red]")
    
    def trade_resources(self):
        if not self.player.current_ship.cargo:
            self.console.print("[red]You have no cargo to trade![/red]")
            return
        
        current_location = self.player.current_location
        
        if not current_location.has_outpost or not current_location.outpost:
            self.console.print("[red]No trading outpost at this location![/red]")
            self.console.print("[yellow]You must travel to a location with an outpost to trade.[/yellow]")
            self.console.print("[blue]Look for stations and research facilities that have trading posts![/blue]")
            return
        
        outpost = current_location.outpost
        self.console.print(f"\n[bold]Welcome to {outpost.name}![/bold]")
        
        trade_table = Table(title="Your Cargo - Trading Prices")
        trade_table.add_column("Resource", style="green")
        trade_table.add_column("Amount", style="yellow")
        trade_table.add_column("Price per Unit", style="cyan")
        trade_table.add_column("Total Value", style="magenta")
        
        cargo_resources = list(self.player.current_ship.cargo.keys())
        total_potential_value = 0
        
        for resource_type in cargo_resources:
            amount = self.player.current_ship.cargo[resource_type]
            price = outpost.get_sell_price(resource_type)
            total_value = amount * price
            total_potential_value += total_value
            
            trade_table.add_row(
                resource_type.value,
                str(amount),
                f"{price:.1f}",
                f"{total_value:.0f}"
            )
        
        self.console.print(trade_table)
        self.console.print(f"[bold]Total potential earnings: {total_potential_value:.0f} credits[/bold]")
        
        self.console.print("\nTrading options:")
        self.console.print("1. Sell all cargo")
        self.console.print("2. Sell specific resource")
        self.console.print("0. Leave without trading")
        
        trade_choice = IntPrompt.ask("What would you like to do?", choices=["0", "1", "2"])
        
        if trade_choice == 0:
            return
        elif trade_choice == 1:
            total_earnings = 0
            for resource_type in list(cargo_resources):
                amount = self.player.current_ship.remove_cargo(resource_type, 
                                                             self.player.current_ship.cargo[resource_type])
                earnings = amount * outpost.get_sell_price(resource_type)
                total_earnings += earnings
            
            self.player.credits += total_earnings
            self.console.print(f"[green]Sold all cargo for {total_earnings:.0f} credits![/green]")
            
        elif trade_choice == 2:
            self.console.print("Select resource to sell:")
            for i, resource_type in enumerate(cargo_resources, 1):
                amount = self.player.current_ship.cargo[resource_type]
                self.console.print(f"{i}. {resource_type.value} ({amount} units)")
            
            resource_choice = IntPrompt.ask(
                "Which resource?",
                choices=[str(i) for i in range(1, len(cargo_resources) + 1)]
            )
            
            selected_resource = cargo_resources[resource_choice - 1]
            max_amount = self.player.current_ship.cargo[selected_resource]
            
            amount_to_sell = IntPrompt.ask(
                f"How many units to sell? (1-{max_amount})",
                choices=[str(i) for i in range(1, max_amount + 1)]
            )
            
            removed_amount = self.player.current_ship.remove_cargo(selected_resource, amount_to_sell)
            earnings = removed_amount * outpost.get_sell_price(selected_resource)
            self.player.credits += earnings
            
            self.console.print(f"[green]Sold {removed_amount} {selected_resource.value} for {earnings:.0f} credits![/green]")
    
    def travel_to_location(self):
        current_location = self.player.current_location
        ship = self.player.current_ship
        
        available_locations = [body for body in self.celestial_bodies if body != current_location]
        
        if not available_locations:
            self.console.print("[red]No other locations available![/red]")
            return
        
        self.console.print("Available destinations:")
        for i, body in enumerate(available_locations, 1):
            fuel_cost = int(abs(body.distance_from_start - current_location.distance_from_start) * 10)
            fuel_status = "[green]✓[/green]" if ship.current_fuel >= fuel_cost else "[red]✗[/red]"
            self.console.print(f"{i}. {body.name} (Distance: {body.distance_from_start:.1f} AU, Fuel cost: {fuel_cost}) {fuel_status}")
        
        choice = IntPrompt.ask(
            "Where would you like to travel? (0 to cancel)",
            choices=[str(i) for i in range(len(available_locations) + 1)]
        )
        
        if choice == 0:
            return
        
        destination = available_locations[choice - 1]
        fuel_cost = int(abs(destination.distance_from_start - current_location.distance_from_start) * 10)
        
        if ship.current_fuel < fuel_cost:
            self.console.print(f"[red]Not enough fuel! Need {fuel_cost}, have {ship.current_fuel}[/red]")
            return
        
        ship.current_fuel -= fuel_cost
        self.player.current_location = destination
        
        self.console.print(f"[green]Traveled to {destination.name}! Used {fuel_cost} fuel.[/green]")
        self.console.print(f"Remaining fuel: {ship.current_fuel}/{ship.fuel_capacity}")
    
    def visit_ship_shop(self):
        self.console.print("\n[bold]Welcome to the Ship Shop![/bold]")
        self.console.print("1. View ship upgrades")
        self.console.print("2. Buy new ship")
        self.console.print("3. Switch active ship")
        self.console.print("0. Leave shop")
        
        choice = IntPrompt.ask("What would you like to do?", choices=["0", "1", "2", "3"])
        
        if choice == 0:
            return
        elif choice == 1:
            self.show_upgrades()
        elif choice == 2:
            self.show_ships()
        elif choice == 3:
            self.switch_ships()
    
    def show_upgrades(self):
        self.console.print("\n[bold]Available Upgrades:[/bold]")
        
        upgrade_table = Table(title="Ship Upgrades")
        upgrade_table.add_column("Upgrade", style="green")
        upgrade_table.add_column("Description", style="yellow")
        upgrade_table.add_column("Cost", style="cyan")
        upgrade_table.add_column("Affordable", style="magenta")
        
        for upgrade in self.shop.upgrades:
            affordable = "✓" if self.shop.can_afford_upgrade(self.player, upgrade) else "✗"
            upgrade_table.add_row(
                upgrade.name,
                upgrade.description,
                f"{upgrade.cost:.0f}",
                affordable
            )
        
        self.console.print(upgrade_table)
        
        self.console.print("\nSelect upgrade to purchase:")
        for i, upgrade in enumerate(self.shop.upgrades, 1):
            self.console.print(f"{i}. {upgrade.name}")
        
        choice = IntPrompt.ask(
            "Which upgrade? (0 to cancel)",
            choices=[str(i) for i in range(len(self.shop.upgrades) + 1)]
        )
        
        if choice == 0:
            return
        
        upgrade = self.shop.upgrades[choice - 1]
        
        if not self.shop.can_afford_upgrade(self.player, upgrade):
            self.console.print(f"[red]Not enough credits! Need {upgrade.cost:.0f}, have {self.player.credits:.0f}[/red]")
            return
        
        self.player.credits -= upgrade.cost
        self.shop.apply_upgrade(self.player.current_ship, upgrade)
        self.console.print(f"[green]Purchased {upgrade.name}! Credits remaining: {self.player.credits:.0f}[/green]")
    
    def show_ships(self):
        self.console.print("\n[bold]Available Ships:[/bold]")
        
        ship_table = Table(title="Ship Catalog")
        ship_table.add_column("Ship", style="green")
        ship_table.add_column("Description", style="yellow")
        ship_table.add_column("Cost", style="cyan")
        ship_table.add_column("Affordable", style="magenta")
        
        for ship_blueprint in self.shop.ships:
            affordable = "✓" if self.shop.can_afford_ship(self.player, ship_blueprint) else "✗"
            ship_table.add_row(
                ship_blueprint.name,
                ship_blueprint.description,
                f"{ship_blueprint.cost:.0f}",
                affordable
            )
        
        self.console.print(ship_table)
        
        self.console.print("\nSelect ship to purchase:")
        for i, ship_blueprint in enumerate(self.shop.ships, 1):
            self.console.print(f"{i}. {ship_blueprint.name}")
        
        choice = IntPrompt.ask(
            "Which ship? (0 to cancel)",
            choices=[str(i) for i in range(len(self.shop.ships) + 1)]
        )
        
        if choice == 0:
            return
        
        ship_blueprint = self.shop.ships[choice - 1]
        
        if not self.shop.can_afford_ship(self.player, ship_blueprint):
            self.console.print(f"[red]Not enough credits! Need {ship_blueprint.cost:.0f}, have {self.player.credits:.0f}[/red]")
            return
        
        self.player.credits -= ship_blueprint.cost
        new_ship = self.shop.create_ship(ship_blueprint)
        self.player.ships.append(new_ship)
        self.console.print(f"[green]Purchased {new_ship.name}! Credits remaining: {self.player.credits:.0f}[/green]")
    
    def switch_ships(self):
        if len(self.player.ships) <= 1:
            self.console.print("[yellow]You only have one ship![/yellow]")
            return
        
        self.console.print("Available ships:")
        for i, ship in enumerate(self.player.ships, 1):
            active = " [ACTIVE]" if ship == self.player.current_ship else ""
            self.console.print(f"{i}. {ship.name}{active}")
        
        choice = IntPrompt.ask(
            "Which ship to activate? (0 to cancel)",
            choices=[str(i) for i in range(len(self.player.ships) + 1)]
        )
        
        if choice == 0:
            return
        
        self.player.current_ship = self.player.ships[choice - 1]
        self.console.print(f"[green]Switched to {self.player.current_ship.name}![/green]")
    
    def show_main_menu(self):
        self.console.print("\n[bold]What would you like to do?[/bold]")
        self.console.print("1. Mine resources")
        self.console.print("2. View location details")
        self.console.print("3. Travel to another location")
        self.console.print("4. Visit outpost (trade)")
        self.console.print("5. Visit ship shop")
        self.console.print("6. View ship status")
        self.console.print("7. End turn")
        self.console.print("0. Quit game")
        
        return IntPrompt.ask("Choose an action", choices=["0", "1", "2", "3", "4", "5", "6", "7"])
    
    def run(self):
        self.initialize_game()
        
        while True:
            self.console.clear()
            self.display_status()
            
            choice = self.show_main_menu()
            
            if choice == 0:
                self.console.print("[yellow]Thanks for playing Space Mining Empire![/yellow]")
                break
            elif choice == 1:
                self.mine_resources()
            elif choice == 2:
                self.display_location_info()
            elif choice == 3:
                self.travel_to_location()
            elif choice == 4:
                self.trade_resources()
            elif choice == 5:
                self.visit_ship_shop()
            elif choice == 6:
                self.display_status()
            elif choice == 7:
                self.current_turn += 1
                self.console.print(f"[blue]Turn {self.current_turn} begins![/blue]")
            
            if choice != 0:
                Prompt.ask("\nPress Enter to continue")