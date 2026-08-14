"""
Monte Carlo Benchmark Runner CLI Tool.
"""

import sys
import json
from kaggriculture.strategy import get_default_champion
from kaggriculture.simulation import MonteCarloSimulator

def main():
    num_games = 50
    if len(sys.argv) > 1:
        try:
            num_games = int(sys.argv[1])
        except ValueError:
            pass

    champion = get_default_champion()
    simulator = MonteCarloSimulator(seed=100)
    
    print(f"Running Monte Carlo Benchmark ({num_games} games)...")
    res = simulator.run_benchmark(champion, num_simulations=num_games)
    
    print("==================================================")
    print(f" Strategy: {res['strategy_id']} ({res['version']})")
    print(f" Win Rate: {round(res['win_rate']*100, 2)}%")
    print(f" Avg Cash: ${res['average_final_cash']}")
    print(f" Median Cash: ${res['median_final_cash']}")
    print(f" Worst Case: ${res['worst_case_cash']}")
    print(f" Best Case: ${res['best_case_cash']}")
    print(f" 95% Confidence Interval: {res['confidence_interval_95']}")
    print("==================================================")

    with open("benchmark_summary.json", "w") as f:
        json.dump(res, f, indent=2)

if __name__ == "__main__":
    main()
