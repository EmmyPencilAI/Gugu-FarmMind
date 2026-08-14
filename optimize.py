"""
Strategy Evolution Optimizer CLI Entry Point.
Runs evolutionary simulations to generate, evaluate, benchmark, and promote candidate strategies.
"""

import os
import sys
import time
import json
from optimizer import StrategyOptimizer

def run_single_cycle(opt: StrategyOptimizer):
    print("--------------------------------------------------")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting Strategy Optimization Cycle...")
    results = opt.run_optimization_cycle()
    print(f"✓ Cycle Finished: Variant={results['variant_id']}")
    print(f"  Win Rate: {round(results['variant_win_rate']*100, 2)}% | Avg Cash: ${results['variant_avg_cash']}")
    print(f"  Decision: {results['decision']}")
    if results.get("promoted"):
        print("  🎉 CANDIDATE PROMOTED TO CHAMPION!")
    print("--------------------------------------------------")
    return results

def main():
    print("==================================================")
    print(" GUGU FARMMIND STRATEGY OPTIMIZATION SERVICE")
    print("==================================================")
    
    is_continuous = os.environ.get("CONTINUOUS_OPTIMIZATION", "false").lower() in ("true", "1", "yes")
    interval = int(os.environ.get("OPTIMIZE_INTERVAL_SECONDS", "3600")) # Default 1 hour
    
    # Check command line flags
    if "--once" in sys.argv or "-1" in sys.argv:
        is_continuous = False
    elif "--continuous" in sys.argv:
        is_continuous = True

    opt = StrategyOptimizer(quality_threshold_win_rate_boost=0.015, min_games=30)
    
    if not is_continuous:
        run_single_cycle(opt)
    else:
        print(f"Running continuous optimization loop (Interval: {interval}s)...")
        while True:
            try:
                run_single_cycle(opt)
            except Exception as e:
                print(f"[Optimizer Warning] Cycle encountered an error: {e}")
            print(f"Sleeping for {interval} seconds until next cycle...")
            time.sleep(interval)

if __name__ == "__main__":
    main()
