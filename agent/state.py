"""
Gugu FarmMind Deterministic Game State Tracker
Extracts and maintains structured game state from Kaggle observations.
"""

from agent.constants import CROP_SPECS, ANIMAL_SPECS, TOTAL_DAYS, TURNS_PER_DAY

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
        """Parse raw Kaggle observation dictionary or object"""
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

    def total_turns_remaining(self):
        return max(0, (TOTAL_DAYS * TURNS_PER_DAY) - self.step)
