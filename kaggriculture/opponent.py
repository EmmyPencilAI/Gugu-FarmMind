"""
Opponent Farm Observation, Probabilistic Inventory Estimation, Strategy Classification, and Counter-Tactics.
"""

from typing import Dict, List, Any
import math

OPP_TYPE_BALANCED = "BALANCED"
OPP_TYPE_AGGRESSIVE_EXPANDER = "AGGRESSIVE_EXPANDER"
OPP_TYPE_CROP_SPECIALIST = "CROP_SPECIALIST"
OPP_TYPE_ANIMAL_SPECIALIST = "ANIMAL_SPECIALIST"
OPP_TYPE_ECONOMIC_HOARDER = "ECONOMIC_HOARDER"
OPP_TYPE_RANDOM = "RANDOM"

class OpponentModel:
    def __init__(self):
        self.opponent_id: str = "opp_unknown"
        self.history: List[Dict[str, Any]] = []
        self.estimated_cash: float = 200.0
        self.classification: str = OPP_TYPE_BALANCED
        self.observed_weaknesses: List[str] = []

    def observe_turn(self, obs: Dict[str, Any]):
        """Parses visible opponent state from raw observation dict."""
        opp_obs = obs.get("opponent", {})
        
        crops = opp_obs.get("crops", {})          # e.g., {"WHEAT": 4, "CORN": 2}
        animals = opp_obs.get("animals", {})      # e.g., {"CHICKEN": 3, "COW": 1}
        land_tiles = opp_obs.get("land_tiles", 10)
        farmhands = opp_obs.get("farmhands", 1)
        visible_cash = opp_obs.get("cash", self.estimated_cash)
        
        self.estimated_cash = visible_cash
        
        turn_data = {
            "day": obs.get("day", 1),
            "crops": crops,
            "animals": animals,
            "land_tiles": land_tiles,
            "farmhands": farmhands,
            "cash": visible_cash
        }
        self.history.append(turn_data)
        
        self.classify_strategy()
        self.detect_weaknesses()

    def classify_strategy(self):
        """Classifies opponent archetype based on asset ratio history."""
        if not self.history:
            return
            
        latest = self.history[-1]
        crop_count = sum(latest["crops"].values())
        animal_count = sum(latest["animals"].values())
        land = latest["land_tiles"]
        
        if land >= 16:
            self.classification = OPP_TYPE_AGGRESSIVE_EXPANDER
        elif crop_count > 3 * max(1, animal_count):
            self.classification = OPP_TYPE_CROP_SPECIALIST
        elif animal_count > 3 * max(1, crop_count):
            self.classification = OPP_TYPE_ANIMAL_SPECIALIST
        elif latest["cash"] > 1000 and crop_count + animal_count < 4:
            self.classification = OPP_TYPE_ECONOMIC_HOARDER
        else:
            self.classification = OPP_TYPE_BALANCED

    def detect_weaknesses(self):
        """Identifies exploitable vulnerabilities in opponent setup."""
        weaknesses = []
        if not self.history:
            return
            
        latest = self.history[-1]
        
        # Weakness 1: Over-investment in slow crops near endgame
        day = latest["day"]
        if day >= 22 and latest["crops"].get("BERRIES", 0) > 0:
            weaknesses.append("PLANTED_UNHARVESTABLE_ENDGAME_BERRIES")
            
        # Weakness 2: Low liquidity / cash reserve
        if latest["cash"] < 30.0:
            weaknesses.append("CRITICAL_CASH_STARVATION")
            
        # Weakness 3: Mono-culture risk (flooding one commodity)
        crops = latest["crops"]
        if len(crops) == 1 and list(crops.values())[0] >= 5:
            single_crop = list(crops.keys())[0]
            weaknesses.append(f"MONO_CROP_DEPENDENCE_{single_crop}")
            
        # Weakness 4: Under-utilized land
        total_used = sum(latest["crops"].values()) + sum(latest["animals"].values())
        if latest["land_tiles"] - total_used >= 6:
            weaknesses.append("IDLE_LAND_INEFFICIENCY")
            
        self.observed_weaknesses = weaknesses

    def predict_future_harvests(self, horizon_days: int = 4) -> Dict[str, float]:
        """Predicts upcoming opponent commodity production that might crash prices."""
        if not self.history:
            return {}
            
        latest = self.history[-1]
        crops = latest["crops"]
        animals = latest["animals"]
        
        # Estimate expected market supply in next N days
        projected = {}
        projected["WHEAT"] = crops.get("WHEAT", 0) * 22.0
        projected["CORN"] = crops.get("CORN", 0) * 42.0
        projected["EGGS"] = animals.get("CHICKEN", 0) * 6.0 * horizon_days
        projected["MILK"] = animals.get("COW", 0) * 24.0 * horizon_days
        
        return projected

    def get_counter_strategy_recommendation(self) -> Dict[str, Any]:
        """Provides direct tactical recommendation for counter-playing this opponent."""
        if self.classification == OPP_TYPE_CROP_SPECIALIST:
            return {
                "pivot": "ANIMAL_HEAVY",
                "reasoning": "Opponent flooding crop market. Shift to livestock milk/eggs for stable non-correlated revenue.",
                "target_crop_boost": 0.2
            }
        elif self.classification == OPP_TYPE_ANIMAL_SPECIALIST:
            return {
                "pivot": "HIGH_VALUE_CROPS",
                "reasoning": "Opponent focused on animals. Capitalize on scarcity in Tomatoes and Berries.",
                "target_crop_boost": 1.5
            }
        elif self.classification == OPP_TYPE_AGGRESSIVE_EXPANDER:
            return {
                "pivot": "FAST_TURNOVER_CASH",
                "reasoning": "Opponent spending cash on land expansion. Undercut them with fast Wheat cycles.",
                "target_crop_boost": 1.2
            }
        else:
            return {
                "pivot": "OPTIMAL_PORTFOLIO",
                "reasoning": "Opponent balanced. Follow core Expected Final Cash optimization model.",
                "target_crop_boost": 1.0
            }
