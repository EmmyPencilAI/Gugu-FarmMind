"""
Multi-Bot Monte Carlo Simulation Engine.
Runs games against 8 distinct bot archetypes and calculates win rate & financial variance.
"""

from typing import Dict, List, Any, Tuple
import random
import statistics
import math
from kaggriculture.state import GameState
from kaggriculture.strategy import StrategyConfig, get_default_champion
from kaggriculture.market import MarketEngine
from kaggriculture.planner import MPCPlanner
from kaggriculture.crops import CROPS
from kaggriculture.animals import ANIMALS

BOT_TYPES = [
    "random",
    "starter",
    "champion",
    "aggressive",
    "economic",
    "animal_bot",
    "crop_bot",
    "market_bot"
]

class MonteCarloSimulator:
    def __init__(self, seed: int = 42):
        self.seed: int = seed

    def run_single_match(self, agent_strategy: StrategyConfig, opponent_type: str, game_seed: int) -> Dict[str, Any]:
        """Simulates 1 complete 30-day game between agent_strategy and opponent_type."""
        rng = random.Random(game_seed)
        
        agent_state = GameState(day=1, cash=200.0, max_days=30)
        opp_state = GameState(day=1, cash=200.0, max_days=30)
        market = MarketEngine()
        planner = MPCPlanner(agent_strategy)

        for day in range(1, 31):
            prices = {k: v[-1] for k, v in market.price_history.items()}
            
            # --- AGENT TURN ---
            actions = planner.plan_next_actions(agent_state, market)
            sales_this_turn = {}
            for act in actions:
                atype = act["action_type"]
                if atype == "SELL_INVENTORY":
                    item = act["item"]
                    qty = agent_state.inventory.get(item, 0.0)
                    if qty > 0:
                        revenue = qty * prices.get(item, 10.0)
                        agent_state.cash += revenue
                        sales_this_turn[item] = sales_this_turn.get(item, 0.0) + qty
                        agent_state.inventory[item] = 0.0
                elif atype == "PLANT_CROP" and agent_state.cash >= act["cost"]:
                    free_pos = agent_state.get_free_grid_positions()
                    if free_pos:
                        agent_state.cash -= act["cost"]
                        c_name = act["crop_name"]
                        from kaggriculture.state import PlantedTile
                        agent_state.crop_tiles[free_pos[0]] = PlantedTile(
                            crop_name=c_name,
                            planted_day=day,
                            growth_days=CROPS[c_name].growth_days
                        )
                elif atype == "BUY_ANIMAL" and agent_state.cash >= act["cost"]:
                    free_pos = agent_state.get_free_grid_positions()
                    if free_pos:
                        agent_state.cash -= act["cost"]
                        a_name = act["animal_name"]
                        from kaggriculture.state import AnimalTile
                        agent_state.animal_tiles[free_pos[0]] = AnimalTile(
                            animal_name=a_name,
                            purchased_day=day
                        )
                elif atype == "BUY_LAND" and agent_state.cash >= act["cost"]:
                    agent_state.cash -= act["cost"]
                    agent_state.land_tiles += 2

            # --- OPPONENT TURN (Simulated Archetype) ---
            opp_sales = self._simulate_opponent_turn(opp_state, opponent_type, day, prices, rng)

            # --- MARKET UPDATE ---
            market.update_market_state(day, sales_this_turn, opp_sales)
            
            # --- DAY ADVANCE ---
            agent_state.advance_day(prices)
            opp_state.advance_day(prices)

        # Final Liquidation Score
        final_prices = {k: v[-1] for k, v in market.price_history.items()}
        agent_final_cash = agent_state.liquidate_all(final_prices)
        opp_final_cash = opp_state.liquidate_all(final_prices)

        win = agent_final_cash > opp_final_cash

        return {
            "seed": game_seed,
            "opponent_type": opponent_type,
            "agent_final_cash": agent_final_cash,
            "opp_final_cash": opp_final_cash,
            "win": win,
            "cash_margin": round(agent_final_cash - opp_final_cash, 2)
        }

    def _simulate_opponent_turn(
        self,
        opp_state: GameState,
        opp_type: str,
        day: int,
        prices: Dict[str, float],
        rng: random.Random
    ) -> Dict[str, float]:
        """Simulates opponent decisions based on their bot archetype."""
        opp_sales = {}
        
        # Simple heuristic logic per bot type
        if opp_type == "random":
            if rng.random() > 0.5 and opp_state.cash >= 20.0:
                opp_state.cash -= 18.0
                opp_state.inventory["CORN"] = opp_state.inventory.get("CORN", 0) + 1.0
            if rng.random() > 0.4:
                for k, qty in list(opp_state.inventory.items()):
                    if qty > 0:
                        opp_sales[k] = qty
                        opp_state.cash += qty * prices.get(k, 10.0)
                        opp_state.inventory[k] = 0.0

        elif opp_type in ["starter", "crop_bot"]:
            # Always plant Wheat/Corn and sell immediately
            if opp_state.cash >= 18.0 and day <= 26:
                opp_state.cash -= 18.0
                opp_state.inventory["CORN"] = opp_state.inventory.get("CORN", 0) + 1.0
            for k, qty in list(opp_state.inventory.items()):
                if qty > 0:
                    opp_sales[k] = qty
                    opp_state.cash += qty * prices.get(k, 10.0)
                    opp_state.inventory[k] = 0.0

        elif opp_type == "aggressive":
            # Buy land aggressively
            if opp_state.cash >= 100.0:
                opp_state.cash -= 100.0
                opp_state.land_tiles += 2
            if opp_state.cash >= 35.0 and day <= 24:
                opp_state.cash -= 35.0
                opp_state.inventory["TOMATOES"] = opp_state.inventory.get("TOMATOES", 0) + 1.0

        elif opp_type == "animal_bot":
            if opp_state.cash >= 120.0:
                opp_state.cash -= 120.0
                opp_state.inventory["MILK"] = opp_state.inventory.get("MILK", 0) + 3.0

        else: # champion / economic / market_bot
            if opp_state.cash >= 50.0 and day <= 24:
                opp_state.cash -= 50.0
                opp_state.inventory["BERRIES"] = opp_state.inventory.get("BERRIES", 0) + 1.0
            for k, qty in list(opp_state.inventory.items()):
                if qty > 0 and prices.get(k, 10.0) >= 15.0:
                    opp_sales[k] = qty
                    opp_state.cash += qty * prices.get(k, 10.0)
                    opp_state.inventory[k] = 0.0

        return opp_sales

    def run_benchmark(
        self,
        strategy: StrategyConfig,
        num_simulations: int = 50,
        opponents: List[str] = None
    ) -> Dict[str, Any]:
        """Runs a batch Monte Carlo benchmark across seeds and opponents."""
        if opponents is None:
            opponents = ["random", "starter", "champion", "aggressive", "economic", "crop_bot"]

        results = []
        wins = 0
        agent_cashes = []

        for i in range(num_simulations):
            opp = opponents[i % len(opponents)]
            seed = self.seed + i
            m_res = self.run_single_match(strategy, opp, seed)
            results.append(m_res)
            
            if m_res["win"]:
                wins += 1
            agent_cashes.append(m_res["agent_final_cash"])

        win_rate = round(wins / num_simulations, 4)
        avg_cash = round(statistics.mean(agent_cashes), 2)
        median_cash = round(statistics.median(agent_cashes), 2)
        stdev_cash = round(statistics.stdev(agent_cashes) if len(agent_cashes) > 1 else 0.0, 2)
        worst_case = round(min(agent_cashes), 2)
        best_case = round(max(agent_cashes), 2)

        # 95% Confidence Interval for Mean Cash
        margin_error = round(1.96 * (stdev_cash / math.sqrt(num_simulations)), 2) if num_simulations > 1 else 0.0

        return {
            "strategy_id": strategy.strategy_id,
            "version": strategy.version,
            "num_simulations": num_simulations,
            "win_rate": win_rate,
            "average_final_cash": avg_cash,
            "median_final_cash": median_cash,
            "variance_stdev": stdev_cash,
            "worst_case_cash": worst_case,
            "best_case_cash": best_case,
            "confidence_interval_95": f"${avg_cash} +/- ${margin_error}",
            "opponents_tested": opponents,
            "detailed_results": results[:10] # Return first 10 for detailed viewing
        }
