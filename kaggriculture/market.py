"""
Market Mechanics, Regime Detection, Price Velocity, Acceleration, and Forecasting.
"""

from typing import Dict, List, Any, Tuple
import math

REGIME_SCARCITY = "SCARCITY"
REGIME_NORMAL = "NORMAL"
REGIME_OVERSUPPLY = "OVERSUPPLY"
REGIME_PRICE_COLLAPSE = "PRICE_COLLAPSE"
REGIME_RECOVERY = "RECOVERY"

class MarketEngine:
    def __init__(self):
        # Base market equilibrium prices
        self.base_prices = {
            "WHEAT": 22.0,
            "CORN": 42.0,
            "SOY": 58.0,
            "TOMATOES": 90.0,
            "BERRIES": 140.0,
            "EGGS": 6.0,
            "MILK": 24.0,
            "WOOL": 28.0
        }
        
        # Price history per commodity
        self.price_history: Dict[str, List[float]] = {k: [v] for k, v in self.base_prices.items()}
        self.town_demand: Dict[str, float] = {k: 100.0 for k in self.base_prices}
        self.market_inventory: Dict[str, float] = {k: 50.0 for k in self.base_prices}

    def update_market_state(self, current_day: int, sales_this_turn: Dict[str, float], opponent_sales: Dict[str, float]):
        """Updates supply/demand dynamics, calculates price velocity and acceleration."""
        for item, base in self.base_prices.items():
            our_supply = sales_this_turn.get(item, 0.0)
            opp_supply = opponent_sales.get(item, 0.0)
            total_supply = our_supply + opp_supply
            
            # Inventory decay and supply inflow
            self.market_inventory[item] = max(0.0, self.market_inventory[item] * 0.85 + total_supply - self.town_demand[item] * 0.15)
            
            # Demand fluctuation based on day
            demand_factor = 1.0 + 0.2 * math.sin(current_day * 0.4)
            self.town_demand[item] = 100.0 * demand_factor
            
            # Price elastic response
            supply_demand_ratio = (self.market_inventory[item] + 10.0) / (self.town_demand[item] + 10.0)
            price_multiplier = math.exp(-0.8 * (supply_demand_ratio - 0.5))
            price_multiplier = max(0.4, min(1.8, price_multiplier))
            
            new_price = round(base * price_multiplier, 2)
            self.price_history[item].append(new_price)

    def get_velocity_and_acceleration(self, commodity: str) -> Tuple[float, float]:
        """Calculates 1st derivative (velocity) and 2nd derivative (acceleration) of price."""
        history = self.price_history.get(commodity, [self.base_prices.get(commodity, 10.0)])
        if len(history) < 2:
            return 0.0, 0.0
        
        v_current = history[-1] - history[-2]
        if len(history) < 3:
            return v_current, 0.0
        
        v_previous = history[-2] - history[-3]
        acceleration = v_current - v_previous
        return v_current, acceleration

    def detect_regime(self, commodity: str) -> str:
        """Classifies commodity market into SCARCITY, NORMAL, OVERSUPPLY, PRICE_COLLAPSE, or RECOVERY."""
        history = self.price_history.get(commodity, [self.base_prices.get(commodity, 10.0)])
        current_price = history[-1]
        base_price = self.base_prices.get(commodity, 10.0)
        price_ratio = current_price / base_price
        
        v, a = self.get_velocity_and_acceleration(commodity)
        
        if price_ratio >= 1.25 and v >= 0:
            return REGIME_SCARCITY
        elif price_ratio <= 0.65 or (v < -3.0 and a < 0):
            return REGIME_PRICE_COLLAPSE
        elif price_ratio <= 0.85:
            return REGIME_OVERSUPPLY
        elif v > 2.0 and a > 0:
            return REGIME_RECOVERY
        else:
            return REGIME_NORMAL

    def forecast_price(self, commodity: str, horizon_days: int = 3) -> List[float]:
        """Predicts expected price curve for the next N days using damped velocity extrapolation."""
        history = self.price_history.get(commodity, [self.base_prices.get(commodity, 10.0)])
        current_price = history[-1]
        base_price = self.base_prices.get(commodity, 10.0)
        v, a = self.get_velocity_and_acceleration(commodity)
        
        forecast = []
        p = current_price
        v_damped = v
        for day in range(1, horizon_days + 1):
            p += v_damped
            # Mean reversion towards base price
            p = p * 0.8 + base_price * 0.2
            p = max(base_price * 0.35, min(base_price * 2.0, p))
            v_damped *= 0.6 # Damping
            forecast.append(round(p, 2))
            
        return forecast

    def get_market_summary(self) -> Dict[str, Any]:
        """Returns market snapshot for strategic advisor and UI dashboard."""
        summary = {}
        for commodity in self.base_prices:
            v, a = self.get_velocity_and_acceleration(commodity)
            regime = self.detect_regime(commodity)
            forecast = self.forecast_price(commodity, 3)
            current_p = self.price_history[commodity][-1]
            summary[commodity] = {
                "current_price": current_p,
                "base_price": self.base_prices[commodity],
                "velocity": round(v, 2),
                "acceleration": round(a, 2),
                "regime": regime,
                "forecast_3d": forecast
            }
        return summary
