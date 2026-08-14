"""
Rolling-Horizon Model Predictive Control (MPC) Planner.
"""

from typing import Dict, List, Any, Tuple
from kaggriculture.state import GameState
from kaggriculture.strategy import StrategyConfig
from kaggriculture.economy import EconomicEngine
from kaggriculture.market import MarketEngine
from kaggriculture.crops import CROPS
from kaggriculture.animals import ANIMALS

class MPCPlanner:
    def __init__(self, strategy: StrategyConfig):
        self.strategy: StrategyConfig = strategy
        self.economic_engine = EconomicEngine(
            cash_reserve=strategy.cash_reserve,
            risk_tolerance=strategy.risk_tolerance
        )

    def plan_next_actions(
        self,
        state: GameState,
        market: MarketEngine,
        horizon_days: int = 3
    ) -> List[Dict[str, Any]]:
        """Evaluates candidate action combinations using rolling-horizon forward simulation."""
        actions: List[Dict[str, Any]] = []
        current_prices = {k: v[-1] for k, v in market.price_history.items()}
        
        # 1. Check Endgame Liquidation Trigger
        if state.day >= self.strategy.endgame_threshold:
            # Liquidate all mature crops & inventory to town market
            for item, qty in list(state.inventory.items()):
                if qty > 0:
                    actions.append({
                        "action_type": "SELL_INVENTORY",
                        "item": item,
                        "quantity": qty,
                        "price": current_prices.get(item, 10.0),
                        "priority": 100
                    })
            return actions

        # 2. Check Inventory Sales (Sell if price ratio above threshold)
        for item, qty in state.inventory.items():
            if qty > 0:
                base_p = market.base_prices.get(item, 10.0)
                curr_p = current_prices.get(item, base_p)
                if curr_p / base_p >= self.strategy.sell_threshold:
                    actions.append({
                        "action_type": "SELL_INVENTORY",
                        "item": item,
                        "quantity": qty,
                        "price": curr_p,
                        "priority": 80
                    })

        # 3. Check Land Expansion
        if state.cash >= self.strategy.land_threshold and state.get_available_tile_count() <= 1:
            actions.append({
                "action_type": "BUY_LAND",
                "cost": 100.0,
                "priority": 75
            })

        # 4. Evaluate Crop Planting Candidates
        free_tiles = state.get_available_tile_count()
        if free_tiles > 0 and state.cash > self.strategy.cash_reserve:
            # Rank crops by expected EFC
            candidate_crops = []
            for c_name, c_def in CROPS.items():
                if state.day + c_def.growth_days <= state.max_days:
                    weight = self.strategy.crop_weights.get(c_name, 0.2)
                    regime = market.detect_regime(c_name)
                    if regime in ["SCARCITY", "NORMAL", "RECOVERY"]:
                        candidate_crops.append((c_name, weight * c_def.base_harvest_value / c_def.cost))
            
            candidate_crops.sort(key=lambda x: x[1], reverse=True)
            
            if candidate_crops and free_tiles > 0:
                best_crop = candidate_crops[0][0]
                crop_def = CROPS[best_crop]
                if state.cash >= crop_def.cost + self.strategy.cash_reserve:
                    actions.append({
                        "action_type": "PLANT_CROP",
                        "crop_name": best_crop,
                        "cost": crop_def.cost,
                        "priority": 60
                    })

        # 5. Evaluate Livestock Purchase
        if free_tiles > 0 and state.cash >= self.strategy.cash_reserve + 80.0:
            for anim_name, weight in self.strategy.animal_weights.items():
                anim_def = ANIMALS[anim_name]
                if state.cash >= anim_def.cost + self.strategy.cash_reserve:
                    actions.append({
                        "action_type": "BUY_ANIMAL",
                        "animal_name": anim_name,
                        "cost": anim_def.cost,
                        "priority": 50
                    })
                    break

        # Sort actions by priority
        actions.sort(key=lambda x: x.get("priority", 0), reverse=True)
        return actions
