"""
Strategy Evolution Optimizer CLI Entry Point.
"""

from optimizer import StrategyOptimizer
import json

def main():
    print("Launching Kaggriculture Autonomous Optimization Loop...")
    opt = StrategyOptimizer(quality_threshold_win_rate_boost=0.015, min_games=30)
    results = opt.run_optimization_cycle()
    
    print("==================================================")
    print(" OPTIMIZATION CYCLE COMPLETED")
    print(f" Variant ID: {results['variant_id']}")
    print(f" Win Rate: {round(results['variant_win_rate']*100, 2)}%")
    print(f" Avg Cash: ${results['variant_avg_cash']}")
    print(f" Decision: {results['decision']}")
    print("==================================================")

if __name__ == "__main__":
    main()
