"""
Crop definitions, growth parameters, and profitability calculations.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CropType:
    name: str
    cost: float
    growth_days: int
    base_harvest_value: float
    fertilizer_cost: float = 5.0
    fertilizer_yield_multiplier: float = 1.30
    water_req_per_day: int = 1

CROPS: Dict[str, CropType] = {
    "WHEAT": CropType(
        name="WHEAT",
        cost=10.0,
        growth_days=2,
        base_harvest_value=22.0,
        fertilizer_cost=4.0,
        fertilizer_yield_multiplier=1.25
    ),
    "CORN": CropType(
        name="CORN",
        cost=18.0,
        growth_days=3,
        base_harvest_value=42.0,
        fertilizer_cost=6.0,
        fertilizer_yield_multiplier=1.28
    ),
    "SOY": CropType(
        name="SOY",
        cost=25.0,
        growth_days=3,
        base_harvest_value=58.0,
        fertilizer_cost=7.0,
        fertilizer_yield_multiplier=1.30
    ),
    "TOMATOES": CropType(
        name="TOMATOES",
        cost=35.0,
        growth_days=4,
        base_harvest_value=90.0,
        fertilizer_cost=10.0,
        fertilizer_yield_multiplier=1.35
    ),
    "BERRIES": CropType(
        name="BERRIES",
        cost=50.0,
        growth_days=5,
        base_harvest_value=140.0,
        fertilizer_cost=12.0,
        fertilizer_yield_multiplier=1.40
    )
}

def calculate_crop_roi(crop_key: str, market_price_multiplier: float = 1.0, fertilized: bool = False, current_day: int = 1, max_days: int = 30) -> float:
    """Calculates Net Expected ROI per day for planting a crop given market conditions and remaining days."""
    if crop_key not in CROPS:
        return 0.0
    crop = CROPS[crop_key]
    
    # Check if crop can mature before day 30
    if current_day + crop.growth_days > max_days:
        return -1.0 # Crop cannot mature before competition end
    
    total_cost = crop.cost + (crop.fertilizer_cost if fertilized else 0.0)
    expected_yield = crop.base_harvest_value * (crop.fertilizer_yield_multiplier if fertilized else 1.0)
    expected_revenue = expected_yield * market_price_multiplier
    
    net_profit = expected_revenue - total_cost
    roi_per_day = (net_profit / total_cost) / crop.growth_days
    return roi_per_day
