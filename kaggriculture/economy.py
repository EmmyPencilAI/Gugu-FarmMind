"""
Economic Portfolio Evaluator, Expected Final Cash (EFC) and Win Probability Estimator.
"""

from typing import Dict, Any, List
import math
from kaggriculture.crops import CROPS, calculate_crop_roi
from kaggriculture.animals import ANIMALS, calculate_animal_expected_profit
from kaggriculture.state import GameState

class EconomicEngine:
    def __init__(self, cash_reserve: float = 120.0, risk_tolerance: float = 0.75):
        self.cash_reserve: float = cash_reserve
        self.risk_tolerance: float = risk_tolerance

    def calculate_expected_final_cash(
        self,
        state: GameState,
        market_prices: Dict[str, float],
        proposed_action: str = "NONE"
    ) -> float:
        """Projects total expected cash at Day 30 given current state and candidate action."""
        remaining_days = max(0, state.max_days - state.day)
        
        # Base cash
        projected_cash = state.cash
        
        # Subtract safety buffer penalty if below cash reserve
        if projected_cash < self.cash_reserve:
            projected_cash -= (self.cash_reserve - projected_cash) * 0.5
            
        # 1. Existing Inventory Value
        for item, qty in state.inventory.items():
            price = market_prices.get(item, 10.0)
            projected_cash += qty * price
            
        # 2. Existing Crops Value upon maturation
        for pos, crop in state.crop_tiles.items():
            days_left = crop.growth_days - (state.day - crop.planted_day)
            if days_left <= remaining_days:
                crop_def = CROPS.get(crop.crop_name)
                base_val = crop_def.base_harvest_value if crop_def else 20.0
                mult = 1.3 if crop.fertilized else 1.0
                price = market_prices.get(crop.crop_name, base_val)
                projected_cash += price * mult
                
        # 3. Existing Animals Net Yield + Slaughter
        for pos, anim in state.animal_tiles.items():
            net_profit = calculate_animal_expected_profit(anim.animal_name, remaining_days, 1.0)
            projected_cash += net_profit
            
        # 4. Opportunity cost discount for remaining days
        time_discount = math.pow(self.risk_tolerance, (state.day / 30.0))
        
        return round(projected_cash * time_discount, 2)

    def calculate_win_probability(self, expected_cash: float, opponent_expected_cash: float) -> float:
        """Calculates expected win probability vs opponent using a sigmoid probability curve."""
        diff = expected_cash - opponent_expected_cash
        # Sigmoid centered at 0 diff
        win_prob = 1.0 / (1.0 + math.exp(-0.005 * diff))
        return round(win_prob, 4)

    def evaluate_investment_opportunity_cost(
        self,
        capital_cost: float,
        expected_returns: float,
        duration_days: int,
        state: GameState
    ) -> float:
        """Calculates net economic value accounting for capital, space, and time costs."""
        if state.cash - capital_cost < self.cash_reserve:
            return -999.0 # Violates safety threshold
            
        net_return = expected_returns - capital_cost
        roi_per_day = (net_return / capital_cost) / max(1, duration_days)
        
        # Opportunity cost of holding cash vs investing
        opportunity_cost = capital_cost * 0.05 * duration_days
        net_value = net_return - opportunity_cost
        
        return net_value
