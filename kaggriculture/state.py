"""
Full Game State representation, grid tracking, state cloning, and transition rules.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional
import copy

GRID_SIZE = 10

@dataclass
class PlantedTile:
    crop_name: str
    planted_day: int
    growth_days: int
    fertilized: bool = False

@dataclass
class AnimalTile:
    animal_name: str
    purchased_day: int

class GameState:
    def __init__(self, day: int = 1, cash: float = 200.0, max_days: int = 30):
        self.day: int = day
        self.max_days: int = max_days
        self.cash: float = cash
        self.land_tiles: int = 10
        self.farmhands: int = 1
        
        # Grid state: (x, y) -> Tile
        self.crop_tiles: Dict[Tuple[int, int], PlantedTile] = {}
        self.animal_tiles: Dict[Tuple[int, int], AnimalTile] = {}
        
        # Inventory held: Commodity -> Quantity
        self.inventory: Dict[str, float] = {
            "WHEAT": 0.0,
            "CORN": 0.0,
            "SOY": 0.0,
            "TOMATOES": 0.0,
            "BERRIES": 0.0,
            "EGGS": 0.0,
            "MILK": 0.0,
            "WOOL": 0.0
        }
        
        # Opponent snapshot
        self.opponent_cash: float = 200.0
        self.opponent_land: int = 10
        self.opponent_crops: int = 0
        self.opponent_animals: int = 0

    def clone(self) -> "GameState":
        """Creates a deep copy of the state for forward simulation / MPC."""
        cloned = GameState(day=self.day, cash=self.cash, max_days=self.max_days)
        cloned.land_tiles = self.land_tiles
        cloned.farmhands = self.farmhands
        cloned.crop_tiles = copy.deepcopy(self.crop_tiles)
        cloned.animal_tiles = copy.deepcopy(self.animal_tiles)
        cloned.inventory = copy.copy(self.inventory)
        cloned.opponent_cash = self.opponent_cash
        cloned.opponent_land = self.opponent_land
        cloned.opponent_crops = self.opponent_crops
        cloned.opponent_animals = self.opponent_animals
        return cloned

    def get_occupied_tile_count(self) -> int:
        return len(self.crop_tiles) + len(self.animal_tiles)

    def get_available_tile_count(self) -> int:
        return max(0, self.land_tiles - self.get_occupied_tile_count())

    def get_free_grid_positions(self) -> List[Tuple[int, int]]:
        """Returns list of unallocated (x,y) positions within owned land boundaries."""
        occupied = set(self.crop_tiles.keys()).union(set(self.animal_tiles.keys()))
        free = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x * GRID_SIZE + y) >= self.land_tiles:
                    break
                if (x, y) not in occupied:
                    free.append((x, y))
                if len(free) >= self.get_available_tile_count():
                    break
        return free

    def advance_day(self, market_prices: Dict[str, float]):
        """Advances state by 1 day: grows crops, produces livestock yields, consumes feed."""
        self.day += 1
        
        # 1. Livestock Yields & Feed
        for pos, anim in list(self.animal_tiles.items()):
            if anim.animal_name == "CHICKEN":
                feed_cost = 2.0
                if self.cash >= feed_cost:
                    self.cash -= feed_cost
                    self.inventory["EGGS"] += 1.0
            elif anim.animal_name == "COW":
                feed_cost = 8.0
                if self.cash >= feed_cost:
                    self.cash -= feed_cost
                    self.inventory["MILK"] += 1.0
            elif anim.animal_name == "SHEEP":
                feed_cost = 5.0
                if self.cash >= feed_cost:
                    self.cash -= feed_cost
                    if (self.day - anim.purchased_day) % 2 == 0:
                        self.inventory["WOOL"] += 1.0

        # 2. Crop Growth & Auto-Harvest
        harvested_positions = []
        for pos, crop in list(self.crop_tiles.items()):
            days_grown = self.day - crop.planted_day
            if days_grown >= crop.growth_days:
                # Harvest into inventory
                yield_qty = 1.0 * (1.3 if crop.fertilized else 1.0)
                self.inventory[crop.crop_name] += yield_qty
                harvested_positions.append(pos)
                
        for pos in harvested_positions:
            del self.crop_tiles[pos]

    def liquidate_all(self, market_prices: Dict[str, float]) -> float:
        """Liquidates inventory and slaughterable animals for cash score."""
        final_cash = self.cash
        
        # Sell inventory at current market prices
        for item, qty in self.inventory.items():
            price = market_prices.get(item, 10.0)
            final_cash += qty * price
            
        # Slaughter animals for residual value
        for pos, anim in self.animal_tiles.items():
            if anim.animal_name == "CHICKEN":
                final_cash += 20.0
            elif anim.animal_name == "COW":
                final_cash += 95.0
            elif anim.animal_name == "SHEEP":
                final_cash += 65.0
                
        return round(final_cash, 2)
