"""
Livestock definitions, daily feed costs, yield cycles, and liquidation values.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AnimalType:
    name: str
    cost: float
    daily_feed_cost: float
    daily_output_value: float
    yield_frequency_days: int
    slaughter_value: float
    land_space_req: int = 1

ANIMALS: Dict[str, AnimalType] = {
    "CHICKEN": AnimalType(
        name="CHICKEN",
        cost=30.0,
        daily_feed_cost=2.0,
        daily_output_value=6.0,      # Eggs
        yield_frequency_days=1,
        slaughter_value=20.0
    ),
    "COW": AnimalType(
        name="COW",
        cost=120.0,
        daily_feed_cost=8.0,
        daily_output_value=24.0,    # Milk
        yield_frequency_days=1,
        slaughter_value=95.0
    ),
    "SHEEP": AnimalType(
        name="SHEEP",
        cost=80.0,
        daily_feed_cost=5.0,
        daily_output_value=28.0,    # Wool every 2 days (avg 14.0/day)
        yield_frequency_days=2,
        slaughter_value=65.0
    )
}

def calculate_animal_expected_profit(animal_key: str, remaining_days: int, market_multiplier: float = 1.0) -> float:
    """Calculates expected net profit of buying an animal for the remaining game duration."""
    if animal_key not in ANIMALS or remaining_days <= 0:
        return 0.0
    animal = ANIMALS[animal_key]
    
    total_feed = animal.daily_feed_cost * remaining_days
    if animal.yield_frequency_days == 1:
        total_yield = animal.daily_output_value * remaining_days * market_multiplier
    else:
        cycles = remaining_days // animal.yield_frequency_days
        total_yield = cycles * animal.daily_output_value * market_multiplier
        
    net_value = (total_yield + animal.slaughter_value) - (animal.cost + total_feed)
    return net_value
