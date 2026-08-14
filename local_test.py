"""
Local Agent Test Script.
Runs agent vs random, starter, and champion bots.
Produces results.json.
"""

import json
import time
from kaggriculture.strategy import get_default_champion
from kaggriculture.simulation import MonteCarloSimulator

def run_local_tests():
    print("==================================================")
    print(" KAGGRICULTURE LOCAL AGENT TEST SUITE")
    print("==================================================")
    
    champion_strat = get_default_champion()
    simulator = MonteCarloSimulator(seed=123)

    bots_to_test = ["random", "starter", "champion", "aggressive", "economic"]
    test_results = {}

    for bot in bots_to_test:
        print(f"Testing Agent vs {bot.upper()} Bot...")
        match_info = simulator.run_single_match(champion_strat, bot, game_seed=42)
        test_results[bot] = match_info
        status = "PASSED (WIN)" if match_info["win"] else "FAILED (LOSS)"
        print(f"  Result: {status} | Agent Cash: ${match_info['agent_final_cash']} | Opp Cash: ${match_info['opp_final_cash']} | Margin: ${match_info['cash_margin']}")

    output = {
        "timestamp": time.time(),
        "agent_strategy_id": champion_strat.strategy_id,
        "results": test_results
    }

    with open("results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\nSaved test results to results.json")
    print("Local Test Suite Completed Successfully!")

if __name__ == "__main__":
    run_local_tests()
