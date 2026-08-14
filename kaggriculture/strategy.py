"""
Strategy dataclass and version management for Kaggriculture agent.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
import json
import time

STATUS_EXPERIMENTAL = "EXPERIMENTAL"
STATUS_CANDIDATE = "CANDIDATE"
STATUS_CHAMPION = "CHAMPION"
STATUS_RETIRED = "RETIRED"

@dataclass
class StrategyConfig:
    strategy_id: str
    version: str
    name: str = "Default Strategy"
    status: str = STATUS_EXPERIMENTAL
    
    # Financial & Portfolio Weights
    cash_reserve: float = 150.0            # Minimum cash safety buffer
    crop_allocation: float = 0.55          # Share of budget allocated to crops vs animals (0.0 to 1.0)
    animal_allocation: float = 0.45        # Share allocated to livestock
    
    # Action Triggers & Thresholds
    land_threshold: float = 400.0          # Cash needed before buying new land
    hire_threshold: float = 250.0          # Cash needed before hiring extra farmhand
    fertilizer_threshold: float = 1.15     # Expected ROI multiplier to justify fertilizer cost
    sell_threshold: float = 0.95           # Price ratio vs historic avg to trigger market sale
    
    # Tactical & Opponent Weights
    market_pressure_weight: float = 1.25   # Weight given to market oversupply predictions
    opponent_weight: float = 0.85          # Weight given to countering opponent crop choices
    risk_tolerance: float = 0.70           # Risk discount factor (1.0 = risk neutral, 0.0 = highly risk averse)
    endgame_threshold: int = 24            # Day (1-30) to switch to aggressive liquidation & harvest
    expansion_rate: float = 1.0            # Speed of land acquisition
    
    # Specific Crop Weights (Wheat, Corn, Soy, Tomatoes, Berries)
    crop_weights: Dict[str, float] = field(default_factory=lambda: {
        "WHEAT": 0.25,
        "CORN": 0.30,
        "SOY": 0.20,
        "TOMATOES": 0.15,
        "BERRIES": 0.10
    })
    
    # Specific Animal Weights (Chickens, Cows, Sheep)
    animal_weights: Dict[str, float] = field(default_factory=lambda: {
        "CHICKEN": 0.50,
        "COW": 0.30,
        "SHEEP": 0.20
    })
    
    # Benchmark Metrics
    git_commit: str = "main"
    simulation_count: int = 0
    win_rate: float = 0.0
    average_final_cash: float = 0.0
    median_final_cash: float = 0.0
    worst_case_cash: float = 0.0
    best_case_cash: float = 0.0
    opponents_tested: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    description: str = "Standard baseline strategy config"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StrategyConfig":
        return cls(**data)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


def get_default_champion() -> StrategyConfig:
    """Returns the baseline CHAMPION strategy configuration."""
    return StrategyConfig(
        strategy_id="strat_champ_v1",
        version="1.0.0",
        name="Balanced Portfolio Champion v1",
        status=STATUS_CHAMPION,
        cash_reserve=120.0,
        crop_allocation=0.60,
        animal_allocation=0.40,
        land_threshold=350.0,
        hire_threshold=220.0,
        fertilizer_threshold=1.10,
        sell_threshold=0.90,
        market_pressure_weight=1.30,
        opponent_weight=0.90,
        risk_tolerance=0.75,
        endgame_threshold=24,
        expansion_rate=1.1,
        simulation_count=500,
        win_rate=0.742,
        average_final_cash=2840.50,
        median_final_cash=2790.00,
        worst_case_cash=1950.00,
        best_case_cash=4120.00,
        opponents_tested=["random", "starter", "aggressive", "economic", "animal_bot", "crop_bot"],
        description="Initial baseline Champion model trained on 500 multi-bot simulations."
    )
