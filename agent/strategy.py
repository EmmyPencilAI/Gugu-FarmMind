"""
Gugu FarmMind Hierarchical Strategy Engine
Coordinates Levels 1 to 6 decision layers with 720-turn horizon & dynamic opponent counter-tactics.
"""

from agent.constants import DEFAULT_STRATEGY, TOTAL_TURNS, TURNS_PER_DAY

class HierarchicalStrategy:
    def __init__(self, config=None):
        self.config = config or DEFAULT_STRATEGY

    def evaluate_levels(self, state, economy, market, crops, animals, opponent):
        # LEVEL 6: Strict Endgame Liquidation (Turns 672-720 / Days 28-30)
        # Guarantees maximum coins in the bank at turn 720 for Bradley-Terry rating victory
        endgame_day_thresh = self.config.get("endgame_threshold", 24)
        if state.day >= endgame_day_thresh or state.step >= 660:
            # Sell any available inventory immediately at market price
            for item, qty in state.inventory.items():
                if qty > 0:
                    return {
                        "action": "SELL",
                        "item": item,
                        "quantity": qty,
                        "level": 6,
                        "reasoning": f"Level 6 Endgame Liquidation: Converting {qty} {item} to bank coins (Day {state.day}, Turn {state.step})"
                    }

        # LEVEL 5: Dynamic Opponent Counter-Tactic
        opp_archetype = opponent.classify(state.opponent)
        
        # LEVEL 4: Market Opportunistic Sales (High Regime Dumping)
        sell_thresh = self.config.get("sell_threshold", 0.88)
        for item, qty in state.inventory.items():
            if qty > 0:
                current_price = state.market_prices.get(item, 20.0)
                if market.should_sell(item, current_price, sell_thresh):
                    return {
                        "action": "SELL",
                        "item": item,
                        "quantity": qty,
                        "level": 4,
                        "reasoning": f"Level 4 Market Strategy: Selling {item} at peak market price (${current_price})"
                    }

        # LEVEL 3: Production Infrastructure Expansion (Land Tiles)
        # Expand land early (Days 1-18) when capital compounding has maximum runway
        land_thresh = self.config.get("land_threshold", 320.0)
        if state.day <= 18 and economy.can_afford(state.cash, land_thresh):
            return {
                "action": "BUY_LAND",
                "level": 3,
                "reasoning": f"Level 3 Production Expansion: Purchasing land tile (Day {state.day})"
            }

        # LEVEL 2: Crop & Livestock Daily Allocation (Only if harvest matures before turn 720)
        if state.day < 27:
            # Crop Selection with growth runway check
            best_crop = crops.select_best_crop_to_plant(state, economy)
            if best_crop:
                return {
                    "action": "PLANT",
                    "crop": best_crop,
                    "level": 2,
                    "reasoning": f"Level 2 Crop Allocation: Planting high ROI crop {best_crop} (Countering {opp_archetype})"
                }

            # Animal Purchase (compounding daily yields: Eggs/Milk/Wool)
            if state.day <= 22:
                best_animal = animals.select_best_animal_to_buy(state, economy)
                if best_animal:
                    return {
                        "action": "BUY_ANIMAL",
                        "animal": best_animal,
                        "level": 2,
                        "reasoning": f"Level 2 Livestock Allocation: Purchasing {best_animal} for daily compounding yields"
                    }

        # LEVEL 1: Cash Reserve Buffer / Pass
        return {
            "action": "PASS",
            "level": 1,
            "reasoning": f"Level 1 Hold: Maintaining safety reserve (${state.cash:.1f}) for next turn opportunity"
        }
