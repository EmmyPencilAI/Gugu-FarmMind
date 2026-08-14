"""
Gugu FarmMind Economic Evaluation Module
Evaluates expected revenue, ROI, opportunity costs, and expected final cash (EFC).
"""

from agent.constants import CROP_SPECS, ANIMAL_SPECS, DEFAULT_STRATEGY

class EconomyEvaluator:
    def __init__(self, config=None):
        self.config = config or DEFAULT_STRATEGY

    def can_afford(self, current_cash, cost):
        reserve = self.config.get("cash_reserve", 120.0)
        return current_cash - cost >= reserve

    def calculate_crop_roi(self, crop_name, current_price, current_day):
        spec = CROP_SPECS.get(crop_name)
        if not spec:
            return -1.0

        growth = spec["growth_days"]
        if current_day + growth > 30:
            return -1.0  # Will not mature before season ends

        cost = spec["cost"]
        expected_revenue = current_price * spec["fert_boost"]  # optimistic yield
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

    def estimate_expected_final_cash(self, state):
        """Estimates Expected Final Cash (EFC) at Day 30 based on current inventory and crops"""
        cash = state.cash
        # Estimate inventory liquidation value
        for item, qty in state.inventory.items():
            price = state.market_prices.get(item, 10.0)
            cash += qty * price

        # Estimate growing crops value if they mature before Day 30
        for crop in state.crops_planted:
            c_name = crop.get("name", "WHEAT")
            days_left = crop.get("days_to_mature", 1)
            if state.day + days_left <= 30:
                p = state.market_prices.get(c_name, 22.0)
                cash += p

        return cash
