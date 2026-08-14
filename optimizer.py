"""
Autonomous Evolutionary Strategy Optimization Loop.
Follows: OBSERVE -> ANALYZE -> FORM HYPOTHESIS -> CREATE VARIANT -> SIMULATE -> BENCHMARK -> COMPARE -> ACCEPT/REJECT -> PACKAGE -> SUBMIT -> LEARN.
"""

import time
import json
import random
import copy
from typing import Dict, List, Any, Tuple
from kaggriculture.strategy import StrategyConfig, get_default_champion, STATUS_EXPERIMENTAL, STATUS_CANDIDATE, STATUS_CHAMPION, STATUS_RETIRED
from kaggriculture.simulation import MonteCarloSimulator
from gemini_advisor import GeminiAdvisor
from kaggle_client import KaggleClient
from db import save_strategy, get_champion_strategy

class StrategyOptimizer:
    def __init__(self, quality_threshold_win_rate_boost: float = 0.02, min_games: int = 40):
        self.quality_threshold_win_rate_boost: float = quality_threshold_win_rate_boost
        self.min_games: int = min_games
        self.simulator = MonteCarloSimulator(seed=int(time.time()))
        self.gemini = GeminiAdvisor()
        self.kaggle = KaggleClient()

    def run_optimization_cycle(self) -> Dict[str, Any]:
        """Executes 1 full evolutionary optimization iteration."""
        # 1. OBSERVE & LOAD CURRENT CHAMPION
        champion_data = get_champion_strategy()
        if champion_data:
            champion = StrategyConfig.from_dict(champion_data)
        else:
            champion = get_default_champion()
            save_strategy(champion.to_dict())

        # 2. ANALYZE & FORM HYPOTHESIS WITH GEMINI ADVISOR
        hypo = self.gemini.generate_experiment_hypothesis(champion.to_dict())
        
        # 3. CREATE STRATEGY VARIANT (MUTATION)
        variant_id = f"strat_var_{int(time.time())}"
        variant_version = f"1.{random.randint(1, 9)}.{random.randint(0, 9)}"
        
        variant = copy.deepcopy(champion)
        variant.strategy_id = variant_id
        variant.version = variant_version
        variant.name = hypo.get("experiment_name", "Mutated Strategy Variant")
        variant.status = STATUS_EXPERIMENTAL
        variant.description = hypo.get("hypothesis", "Mutated parameter set")
        
        # Apply parameter modifications
        modifications = hypo.get("parameter_modifications", {})
        for param, val in modifications.items():
            if hasattr(variant, param):
                setattr(variant, param, val)

        # Additional slight stochastic parameter mutation
        variant.cash_reserve = max(80.0, min(200.0, variant.cash_reserve * random.uniform(0.92, 1.08)))
        variant.sell_threshold = max(0.70, min(1.20, variant.sell_threshold * random.uniform(0.95, 1.05)))

        # 4. SIMULATE & BENCHMARK IN MONTE CARLO
        bench_results = self.simulator.run_benchmark(variant, num_simulations=self.min_games)
        
        variant.win_rate = bench_results["win_rate"]
        variant.average_final_cash = bench_results["average_final_cash"]
        variant.median_final_cash = bench_results["median_final_cash"]
        variant.worst_case_cash = bench_results["worst_case_cash"]
        variant.best_case_cash = bench_results["best_case_cash"]
        variant.simulation_count = self.min_games
        variant.opponents_tested = bench_results["opponents_tested"]

        # 5. COMPARE WITH CURRENT CHAMPION
        win_rate_diff = variant.win_rate - champion.win_rate
        cash_diff = variant.average_final_cash - champion.average_final_cash

        promoted = False
        decision_reasoning = ""

        # Quality Gate Check
        if win_rate_diff >= self.quality_threshold_win_rate_boost or (win_rate_diff >= 0 and cash_diff > 100.0):
            promoted = True
            variant.status = STATUS_CHAMPION
            champion.status = STATUS_RETIRED
            save_strategy(champion.to_dict()) # Save old champion as RETIRED
            save_strategy(variant.to_dict())  # Save new champion
            decision_reasoning = f"ACCEPTED & PROMOTED: Win rate improved by +{round(win_rate_diff*100, 2)}% (Avg Cash diff: +${round(cash_diff, 2)})"
        else:
            variant.status = STATUS_RETIRED
            save_strategy(variant.to_dict())
            decision_reasoning = f"REJECTED: Win rate delta ({round(win_rate_diff*100, 2)}%) failed quality gate threshold (+{self.quality_threshold_win_rate_boost*100}%)."

        # 6. PACKAGE & OPTIONALLY SUBMIT TO KAGGLE
        submission_info = None
        if promoted:
            # Package main.py for Kaggle
            import subprocess
            subprocess.run(["python3", "package_submission.py"], capture_output=True, text=True)
            
            # Optionally submit candidate
            submission_info = self.kaggle.submit_agent_file("submission.tar.gz", f"Promoted Candidate {variant.version} - WinRate {variant.win_rate}")

        return {
            "cycle_timestamp": time.time(),
            "champion_id": champion.strategy_id,
            "champion_win_rate": champion.win_rate,
            "variant_id": variant.strategy_id,
            "variant_win_rate": variant.win_rate,
            "variant_avg_cash": variant.average_final_cash,
            "promoted": promoted,
            "decision": decision_reasoning,
            "benchmark_summary": bench_results,
            "kaggle_submission": submission_info
        }

if __name__ == "__main__":
    opt = StrategyOptimizer()
    res = opt.run_optimization_cycle()
    print(json.dumps(res, indent=2))
