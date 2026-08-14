"""
Gugu FarmMind Crop Management Module
Handles crop selection, watering schedules, fertilizer application, and harvesting.
"""

from agent.constants import CROP_SPECS

class CropManager:
    def __init__(self, config):
        self.config = config

    def select_best_crop_to_plant(self, state, economy_evaluator):
        best_crop = None
        best_roi = -1.0

        for crop_name in CROP_SPECS.keys():
            if not economy_evaluator.can_afford(state.cash, CROP_SPECS[crop_name]["cost"]):
                continue

            current_price = state.market_prices.get(crop_name, CROP_SPECS[crop_name]["base_price"])
            roi = economy_evaluator.calculate_crop_roi(crop_name, current_price, state.day)

            if roi > best_roi and roi > 0:
                best_roi = roi
                best_crop = crop_name

        return best_crop

    def should_apply_fertilizer(self, state, crop_name):
        fert_thresh = self.config.get("fertilizer_threshold", 1.10)
        current_price = state.market_prices.get(crop_name, 20.0)
        base_price = CROP_SPECS.get(crop_name, {}).get("base_price", 20.0)
        return (current_price / base_price) >= fert_thresh
