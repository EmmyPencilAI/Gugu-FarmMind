"""
Gugu FarmMind Livestock Management Module
Handles purchasing, shed capacity, feeding, and product harvesting for livestock.
"""

from agent.constants import ANIMAL_SPECS

class AnimalManager:
    def __init__(self, config):
        self.config = config

    def select_best_animal_to_buy(self, state, economy_evaluator):
        best_animal = None
        best_roi = -1.0

        for animal_name, spec in ANIMAL_SPECS.items():
            if not economy_evaluator.can_afford(state.cash, spec["cost"]):
                continue

            yield_item = spec["yield_item"]
            yield_price = state.market_prices.get(yield_item, spec["base_yield_price"])
            roi = economy_evaluator.calculate_animal_roi(animal_name, yield_price, state.day)

            if roi > best_roi and roi > 0:
                best_roi = roi
                best_animal = animal_name

        return best_animal
