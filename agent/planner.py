"""
Gugu FarmMind Master Planner
Main decision orchestration engine.
"""

from agent.state import GameState
from agent.economy import EconomyEvaluator
from agent.market import MarketIntelligence
from agent.crops import CropManager
from agent.animals import AnimalManager
from agent.opponent import OpponentClassifier
from agent.strategy import HierarchicalStrategy
from agent.constants import DEFAULT_STRATEGY

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
        # Update state and sub-systems
        self.state.update_from_obs(raw_obs)
        self.market.update(self.state.market_prices)

        # Decide action through hierarchical strategy
        action_payload = self.strategy.evaluate_levels(
            self.state,
            self.economy,
            self.market,
            self.crops,
            self.animals,
            self.opponent
        )

        return action_payload
