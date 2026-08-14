"""
Gugu FarmMind Hierarchical Strategy Module
Coordinates Level 1 to Level 6 decision layers.
"""

from agent.constants import DEFAULT_STRATEGY

class HierarchicalStrategy:
    def __init__(self, config=None):
        self.config = config or DEFAULT_STRATEGY

    def evaluate_levels(self, state, economy, market, crops, animals, opponent):
        # LEVEL 6: Endgame Optimization (Days 24-30)
        endgame_thresh = self.config.get("endgame_threshold", 24)
        if state.day >= endgame_thresh:
            for item, qty in state.inventory.items():
                if qty > 0:
                    return {
                        "action": "SELL",
                        "item": item,
                        "quantity": qty,
                        "level": 6,
                        "reasoning": f"Level 6 Endgame Liquidation: Selling {qty} {item}"
                    }

        # LEVEL 4: Market Opportunistic Sales
        sell_thresh = self.config.get("sell_threshold", 0.90)
        for item, qty in state.inventory.items():
            if qty > 0:
                current_price = state.market_prices.get(item, 20.0)
                if market.should_sell(item, current_price, sell_thresh):
                    return {
                        "action": "SELL",
                        "item": item,
                        "quantity": qty,
                        "level": 4,
                        "reasoning": f"Level 4 Market Strategy: Selling {item} at high market regime"
                    }

        # LEVEL 3: Infrastructure Expansion (Land / Farm Hands)
        land_thresh = self.config.get("land_threshold", 350.0)
        if economy.can_afford(state.cash, land_thresh):
            return {
                "action": "BUY_LAND",
                "level": 3,
                "reasoning": "Level 3 Production Expansion: Purchasing additional farm land"
            }

        # LEVEL 2: Crop & Livestock Daily Allocation
        best_crop = crops.select_best_crop_to_plant(state, economy)
        if best_crop:
            return {
                "action": "PLANT",
                "crop": best_crop,
                "level": 2,
                "reasoning": f"Level 2 Daily Allocation: Planting optimal ROI crop {best_crop}"
            }

        best_animal = animals.select_best_animal_to_buy(state, economy)
        if best_animal:
            return {
                "action": "BUY_ANIMAL",
                "animal": best_animal,
                "level": 2,
                "reasoning": f"Level 2 Daily Allocation: Purchasing livestock {best_animal}"
            }

        # LEVEL 1: Pass / Hold Action
        return {
            "action": "PASS",
            "level": 1,
            "reasoning": "Level 1 Immediate Action: Maintaining cash reserve"
        }
