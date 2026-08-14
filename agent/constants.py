"""
Gugu FarmMind Competition Agent Constants
Kaggriculture Environment Parameters & Specifications
"""

TOTAL_DAYS = 30
TURNS_PER_DAY = 24
TOTAL_TURNS = TOTAL_DAYS * TURNS_PER_DAY  # 720 turns

# Crop Catalog: Cost, Growth Days, Base Market Value, Water Needs, Fertilizer Yield Boost
CROP_SPECS = {
    "WHEAT": {
        "cost": 10.0,
        "growth_days": 2,
        "base_price": 22.0,
        "water_freq": 1,
        "fert_boost": 1.25,
        "space_required": 1
    },
    "CORN": {
        "cost": 18.0,
        "growth_days": 3,
        "base_price": 42.0,
        "water_freq": 1,
        "fert_boost": 1.30,
        "space_required": 1
    },
    "SOY": {
        "cost": 25.0,
        "growth_days": 3,
        "base_price": 58.0,
        "water_freq": 2,
        "fert_boost": 1.35,
        "space_required": 1
    },
    "TOMATOES": {
        "cost": 35.0,
        "growth_days": 4,
        "base_price": 90.0,
        "water_freq": 2,
        "fert_boost": 1.40,
        "space_required": 1
    },
    "BERRIES": {
        "cost": 50.0,
        "growth_days": 5,
        "base_price": 140.0,
        "water_freq": 2,
        "fert_boost": 1.50,
        "space_required": 1
    }
}

# Animal Catalog: Cost, Daily Feed Cost, Daily Yield Item, Base Yield Value, Shed Requirement
ANIMAL_SPECS = {
    "CHICKEN": {
        "cost": 30.0,
        "feed_cost_per_day": 2.0,
        "yield_item": "EGGS",
        "base_yield_price": 6.0,
        "shed_capacity": 1
    },
    "COW": {
        "cost": 120.0,
        "feed_cost_per_day": 8.0,
        "yield_item": "MILK",
        "base_yield_price": 24.0,
        "shed_capacity": 4
    },
    "SHEEP": {
        "cost": 80.0,
        "feed_cost_per_day": 5.0,
        "yield_item": "WOOL",
        "base_yield_price": 28.0,
        "shed_capacity": 2
    }
}

# Land & Infrastructure Expansion Costs
LAND_EXPANSION_COST = 350.0
FARM_HAND_HIRE_COST = 220.0
FARM_HAND_DAILY_WAGE = 15.0
SHED_EXPANSION_COST = 200.0
FERTILIZER_BAG_COST = 15.0

# Default Strategy Parameters
DEFAULT_STRATEGY = {
    "strategy_id": "champ_gugu_v1.0.0",
    "version": "1.0.0",
    "cash_reserve": 120.0,
    "crop_allocation": 0.60,
    "animal_allocation": 0.40,
    "land_threshold": 350.0,
    "hire_threshold": 220.0,
    "fertilizer_threshold": 1.10,
    "sell_threshold": 0.90,
    "market_pressure_weight": 1.30,
    "opponent_weight": 0.90,
    "risk_tolerance": 0.75,
    "endgame_threshold": 24,
    "crop_weights": {
        "WHEAT": 0.25,
        "CORN": 0.30,
        "SOY": 0.20,
        "TOMATOES": 0.15,
        "BERRIES": 0.10
    },
    "animal_weights": {
        "CHICKEN": 0.50,
        "COW": 0.30,
        "SHEEP": 0.20
    }
}
