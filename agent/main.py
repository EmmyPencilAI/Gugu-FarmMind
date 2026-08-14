"""
Gugu FarmMind Production Agent Entry Point
Target submission file for Kaggle Kaggriculture competition.
Self-contained, fast, deterministic local execution without network dependencies.
"""

try:
    from agent.planner import MasterPlanner
    planner_instance = MasterPlanner()
except ImportError:
    # Standalone execution fallback if bundled without package relative import
    import math

    STRATEGY_CONFIG = {
        "cash_reserve": 120.0,
        "sell_threshold": 0.90,
        "land_threshold": 350.0,
        "endgame_threshold": 24,
        "crop_weights": {"WHEAT": 0.25, "CORN": 0.30, "SOY": 0.20, "TOMATOES": 0.15, "BERRIES": 0.10},
        "animal_weights": {"CHICKEN": 0.50, "COW": 0.30, "SHEEP": 0.20}
    }

    class FallbackPlanner:
        def plan_turn(self, obs):
            obs_data = obs if isinstance(obs, dict) else getattr(obs, "observation", {})
            day = obs_data.get("day", 1)
            cash = float(obs_data.get("cash", 200.0))
            inventory = obs_data.get("inventory", {})

            # Endgame liquidation
            if day >= STRATEGY_CONFIG["endgame_threshold"]:
                for item, qty in inventory.items():
                    if qty > 0:
                        return {"action": "SELL", "item": item, "quantity": qty, "reasoning": "Fallback Endgame Liquidation"}

            # Standard sales
            for item, qty in inventory.items():
                if qty > 0:
                    return {"action": "SELL", "item": item, "quantity": qty, "reasoning": "Fallback Market Sale"}

            # Expansion
            if cash >= STRATEGY_CONFIG["land_threshold"]:
                return {"action": "BUY_LAND", "reasoning": "Fallback Expansion"}

            # Planting
            if cash >= STRATEGY_CONFIG["cash_reserve"] + 20.0:
                return {"action": "PLANT", "crop": "CORN", "reasoning": "Fallback Corn Planting"}

            return {"action": "PASS", "reasoning": "Fallback Hold"}

    planner_instance = FallbackPlanner()

def agent(obs):
    """
    Main entry point invoked by Kaggle environment.
    """
    try:
        action = planner_instance.plan_turn(obs)
        return action
    except Exception as e:
        # Ultimate fallback safety rule: never crash match execution
        return {
            "action": "PASS",
            "reasoning": f"Safety fallback exception catch: {str(e)}"
        }
