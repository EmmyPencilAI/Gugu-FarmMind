"""
Gugu FarmMind Self-Contained Competition Submission File
Target file for direct single-file Kaggle CLI submission:
kaggle competitions submit -c kaggriculture -f submission.py -m "Gugu FarmMind"
"""

import math

# =====================================================================
# 1. CONSTANTS & ENVIRONMENT CATALOGS
# =====================================================================
TOTAL_DAYS = 30
TURNS_PER_DAY = 24
TOTAL_TURNS = TOTAL_DAYS * TURNS_PER_DAY  # 720 turns

CROP_SPECS = {
    "WHEAT": {"cost": 10.0, "growth_days": 2, "base_price": 22.0, "water_freq": 1, "fert_boost": 1.25, "space_required": 1},
    "CORN": {"cost": 18.0, "growth_days": 3, "base_price": 42.0, "water_freq": 1, "fert_boost": 1.30, "space_required": 1},
    "SOY": {"cost": 25.0, "growth_days": 3, "base_price": 58.0, "water_freq": 2, "fert_boost": 1.35, "space_required": 1},
    "TOMATOES": {"cost": 35.0, "growth_days": 4, "base_price": 90.0, "water_freq": 2, "fert_boost": 1.40, "space_required": 1},
    "BERRIES": {"cost": 50.0, "growth_days": 5, "base_price": 140.0, "water_freq": 2, "fert_boost": 1.50, "space_required": 1}
}

ANIMAL_SPECS = {
    "CHICKEN": {"cost": 30.0, "feed_cost_per_day": 2.0, "yield_item": "EGGS", "base_yield_price": 6.0, "shed_capacity": 1},
    "COW": {"cost": 120.0, "feed_cost_per_day": 8.0, "yield_item": "MILK", "base_yield_price": 24.0, "shed_capacity": 4},
    "SHEEP": {"cost": 80.0, "feed_cost_per_day": 5.0, "yield_item": "WOOL", "base_yield_price": 28.0, "shed_capacity": 2}
}

DEFAULT_STRATEGY = {
    "strategy_id": "champ_gugu_v1.0.0",
    "version": "1.0.0",
    "cash_reserve": 110.0,
    "crop_allocation": 0.55,
    "animal_allocation": 0.45,
    "land_threshold": 320.0,
    "hire_threshold": 220.0,
    "fertilizer_threshold": 1.10,
    "sell_threshold": 0.88,
    "market_pressure_weight": 1.30,
    "opponent_weight": 0.90,
    "risk_tolerance": 0.75,
    "endgame_threshold": 24,
    "crop_weights": {"WHEAT": 0.25, "CORN": 0.30, "SOY": 0.20, "TOMATOES": 0.15, "BERRIES": 0.10},
    "animal_weights": {"CHICKEN": 0.50, "COW": 0.30, "SHEEP": 0.20}
}

# =====================================================================
# 2. STATE MANAGEMENT
# =====================================================================
class GameState:
    def __init__(self):
        self.step = 0
        self.day = 1
        self.turn_in_day = 1
        self.cash = 200.0
        self.inventory = {}
        self.market_prices = {}
        self.crops_planted = []
        self.animals_owned = []
        self.land_tiles = 10
        self.farm_hands = 0
        self.shed_capacity = 10
        self.opponent = {
            "classification": "UNKNOWN",
            "estimated_cash": 200.0,
            "observed_crops": [],
            "observed_animals": []
        }
        self.price_history = {}

    def update_from_obs(self, obs):
        if isinstance(obs, dict):
            obs_dict = obs
        else:
            obs_dict = getattr(obs, "observation", {}) if hasattr(obs, "observation") else {}

        self.step = obs_dict.get("step", self.step + 1)
        self.day = obs_dict.get("day", min(TOTAL_DAYS, max(1, (self.step // TURNS_PER_DAY) + 1)))
        self.turn_in_day = (self.step % TURNS_PER_DAY) + 1
        self.cash = float(obs_dict.get("cash", self.cash))
        self.inventory = obs_dict.get("inventory", self.inventory)
        
        raw_prices = obs_dict.get("market_prices", {})
        if raw_prices:
            self.market_prices = raw_prices
            for item, p in raw_prices.items():
                if item not in self.price_history:
                    self.price_history[item] = []
                self.price_history[item].append(float(p))

        self.crops_planted = obs_dict.get("crops_planted", self.crops_planted)
        self.animals_owned = obs_dict.get("animals_owned", self.animals_owned)
        self.land_tiles = obs_dict.get("land_tiles", self.land_tiles)
        self.farm_hands = obs_dict.get("farm_hands", self.farm_hands)

        if "opponent" in obs_dict and isinstance(obs_dict["opponent"], dict):
            self.opponent.update(obs_dict["opponent"])

    def days_remaining(self):
        return max(0, TOTAL_DAYS - self.day)

# =====================================================================
# 3. ECONOMY EVALUATION ENGINE
# =====================================================================
class EconomyEvaluator:
    def __init__(self, config=None):
        self.config = config or DEFAULT_STRATEGY

    def can_afford(self, current_cash, cost):
        reserve = self.config.get("cash_reserve", 110.0)
        return current_cash - cost >= reserve

    def calculate_crop_roi(self, crop_name, current_price, current_day):
        spec = CROP_SPECS.get(crop_name)
        if not spec:
            return -1.0
        growth = spec["growth_days"]
        if current_day + growth > 30:
            return -1.0
        cost = spec["cost"]
        expected_revenue = current_price * spec["fert_boost"]
        net_profit = expected_revenue - cost
        daily_roi = (net_profit / cost) / max(1, growth)
        weight = self.config.get("crop_weights", {}).get(crop_name, 0.20)
        return daily_roi * weight

    def calculate_animal_roi(self, animal_name, yield_price, current_day):
        spec = ANIMAL_SPECS.get(animal_name)
        if not spec:
            return -1.0
        days_left = max(0, 30 - current_day)
        if days_left <= 0:
            return -1.0
        initial_cost = spec["cost"]
        total_feed_cost = spec["feed_cost_per_day"] * days_left
        total_investment = initial_cost + total_feed_cost
        total_yield_rev = spec["base_yield_price"] * yield_price * days_left
        net_profit = total_yield_rev - total_investment
        if total_investment <= 0:
            return 0.0
        roi = net_profit / total_investment
        weight = self.config.get("animal_weights", {}).get(animal_name, 0.30)
        return roi * weight

# =====================================================================
# 4. MARKET INTELLIGENCE ENGINE
# =====================================================================
class MarketIntelligence:
    def __init__(self):
        self.history = {}

    def update(self, prices):
        for item, price in prices.items():
            if item not in self.history:
                self.history[item] = []
            self.history[item].append(float(price))

    def get_velocity(self, item):
        prices = self.history.get(item, [])
        if len(prices) < 2:
            return 0.0
        return (prices[-1] - prices[-2]) / max(1.0, prices[-2])

    def should_sell(self, item, current_price, sell_threshold):
        base_price = CROP_SPECS.get(item, {}).get("base_price", 20.0)
        ratio = current_price / max(1.0, base_price)
        velocity = self.get_velocity(item)
        return ratio >= sell_threshold or (ratio >= 0.85 and velocity < -0.05)

# =====================================================================
# 5. CROP & LIVESTOCK MANAGERS
# =====================================================================
class CropManager:
    def __init__(self, config):
        self.config = config

    def select_best_crop_to_plant(self, state, economy):
        best_crop = None
        best_roi = -1.0
        for crop_name in CROP_SPECS.keys():
            if not economy.can_afford(state.cash, CROP_SPECS[crop_name]["cost"]):
                continue
            current_price = state.market_prices.get(crop_name, CROP_SPECS[crop_name]["base_price"])
            roi = economy.calculate_crop_roi(crop_name, current_price, state.day)
            if roi > best_roi and roi > 0:
                best_roi = roi
                best_crop = crop_name
        return best_crop

class AnimalManager:
    def __init__(self, config):
        self.config = config

    def select_best_animal_to_buy(self, state, economy):
        best_animal = None
        best_roi = -1.0
        for animal_name in ANIMAL_SPECS.keys():
            if not economy.can_afford(state.cash, ANIMAL_SPECS[animal_name]["cost"]):
                continue
            yield_item = ANIMAL_SPECS[animal_name]["yield_item"]
            yield_price = state.market_prices.get(yield_item, ANIMAL_SPECS[animal_name]["base_yield_price"])
            roi = economy.calculate_animal_roi(animal_name, yield_price, state.day)
            if roi > best_roi and roi > 0:
                best_roi = roi
                best_animal = animal_name
        return best_animal

# =====================================================================
# 6. OPPONENT CLASSIFIER
# =====================================================================
class OpponentClassifier:
    def classify(self, opponent_data):
        if not opponent_data or not isinstance(opponent_data, dict):
            return "BALANCED"
        crops = len(opponent_data.get("observed_crops", []))
        animals = len(opponent_data.get("observed_animals", []))
        land = opponent_data.get("land_tiles", 10)
        if land >= 14:
            return "AGGRESSIVE_EXPANSION"
        elif crops > 3 * max(1, animals):
            return "CROP_SPECIALIST"
        elif animals > 2 * max(1, crops):
            return "ANIMAL_SPECIALIST"
        return "BALANCED"

# =====================================================================
# 7. HIERARCHICAL STRATEGY ORCHESTRATION
# =====================================================================
class HierarchicalStrategy:
    def __init__(self, config=None):
        self.config = config or DEFAULT_STRATEGY

    def evaluate_levels(self, state, economy, market, crops, animals, opponent):
        # LEVEL 6: Strict Endgame Liquidation (Turns 672-720 / Days 28-30)
        endgame_thresh = self.config.get("endgame_threshold", 24)
        if state.day >= endgame_thresh or state.step >= 660:
            for item, qty in state.inventory.items():
                if qty > 0:
                    return {
                        "action": "SELL",
                        "item": item,
                        "quantity": qty,
                        "level": 6,
                        "reasoning": f"Endgame Liquidation: Converting {qty} {item} to bank coins"
                    }

        # LEVEL 4: Opportunistic Market Sales
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
                        "reasoning": f"Market Peak Sale: Selling {item} at ${current_price}"
                    }

        # LEVEL 3: Production Expansion (Land Tiles)
        land_thresh = self.config.get("land_threshold", 320.0)
        if state.day <= 18 and economy.can_afford(state.cash, land_thresh):
            return {
                "action": "BUY_LAND",
                "level": 3,
                "reasoning": "Expansion: Purchasing land tile"
            }

        # LEVEL 2: Crop & Livestock Daily Allocation
        if state.day < 27:
            best_crop = crops.select_best_crop_to_plant(state, economy)
            if best_crop:
                return {
                    "action": "PLANT",
                    "crop": best_crop,
                    "level": 2,
                    "reasoning": f"Planting optimal ROI crop {best_crop}"
                }

            if state.day <= 22:
                best_animal = animals.select_best_animal_to_buy(state, economy)
                if best_animal:
                    return {
                        "action": "BUY_ANIMAL",
                        "animal": best_animal,
                        "level": 2,
                        "reasoning": f"Purchasing livestock {best_animal}"
                    }

        # LEVEL 1: Cash Reserve Buffer / Hold
        return {
            "action": "PASS",
            "level": 1,
            "reasoning": f"Holding cash reserve (${state.cash:.1f})"
        }

class MasterPlanner:
    def __init__(self, config=None):
        self.config = config or DEFAULT_STRATEGY
        self.state = GameState()
        self.economy = EconomyEvaluator(self.config)
        self.market = MarketIntelligence()
        self.crops = CropManager(self.config)
        self.animals = AnimalManager(self.config)
        self.opponent = OpponentClassifier()
        self.strategy = HierarchicalStrategy(self.config)

    def plan_turn(self, raw_obs):
        self.state.update_from_obs(raw_obs)
        self.market.update(self.state.market_prices)
        return self.strategy.evaluate_levels(
            self.state,
            self.economy,
            self.market,
            self.crops,
            self.animals,
            self.opponent
        )

# Module singleton instance
_planner = MasterPlanner()

# =====================================================================
# 8. KAGGLE AGENT ENTRY POINT
# =====================================================================
def agent(obs):
    """
    Main entry point invoked by the Kaggle competition execution environment.
    """
    try:
        return _planner.plan_turn(obs)
    except Exception as e:
        return {
            "action": "PASS",
            "reasoning": f"Safety fallback: {str(e)}"
        }

__all__ = ["agent"]
