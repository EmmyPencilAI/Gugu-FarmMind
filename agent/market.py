"""
Gugu FarmMind Market Intelligence Module
Tracks price trends, velocity, town demand, and market regimes.
"""

from agent.constants import CROP_SPECS, ANIMAL_SPECS

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
        return prices[-1] - prices[-2]

    def classify_regime(self, item, current_price):
        base_price = 20.0
        if item in CROP_SPECS:
            base_price = CROP_SPECS[item]["base_price"]
        elif item in ANIMAL_SPECS:
            base_price = ANIMAL_SPECS[item]["base_yield_price"]

        ratio = current_price / base_price if base_price > 0 else 1.0
        velocity = self.get_velocity(item)

        if ratio >= 1.3:
            return "SCARCITY"
        elif ratio <= 0.7:
            return "CRASH" if velocity < 0 else "OVERSUPPLY"
        elif velocity > 0.5:
            return "RECOVERY"
        else:
            return "NORMAL"

    def should_sell(self, item, current_price, sell_threshold_ratio=0.9):
        base_price = 20.0
        if item in CROP_SPECS:
            base_price = CROP_SPECS[item]["base_price"]
        elif item in ANIMAL_SPECS:
            base_price = ANIMAL_SPECS[item]["base_yield_price"]

        regime = self.classify_regime(item, current_price)
        if regime in ["SCARCITY", "RECOVERY"]:
            return True
        return (current_price / base_price) >= sell_threshold_ratio
