"""
Continuous Autonomous Strategy Evolution CLI & Background Worker.
Runs endless evolutionary generations until explicitly stopped.
Tracks generational improvements, learns from mistakes, and honors the 5/day Kaggle quota.
"""

import os
import sys
import time
import json
import signal
from optimizer import StrategyOptimizer
from db import get_daily_quota_info

RUNNING = True

def handle_shutdown(signum, frame):
    global RUNNING
    print(f"\n[Optimizer] Received termination signal ({signum}). Gracefully stopping loop...")
    RUNNING = False

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

def run_single_cycle(opt: StrategyOptimizer, gen: int):
    print("==================================================")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] GENERATION {gen} OPTIMIZATION CYCLE")
    print("==================================================")
    results = opt.run_optimization_cycle(generation=gen)
    print(f"✓ Variant Generated: {results['variant_id']}")
    print(f"  Win Rate: {round(results['variant_win_rate']*100, 2)}% | Avg Cash: ${results['variant_avg_cash']}")
    print(f"  Est. Bradley-Terry Rating: {results.get('estimated_bt_rating', 'N/A')}")
    print(f"  Decision: {results['decision']}")
    if results.get("promoted"):
        print("  🎉 PROMOTED TO NEW CHAMPION & ACTIVE LADDER POOL!")
    
    quota = results.get("quota_info", {})
    print(f"  Daily Quota: {quota.get('used_today', 0)}/5 submissions used today ({quota.get('remaining_today', 5)} remaining)")
    print("==================================================")
    return results

def main():
    print("==================================================")
    print(" GUGU FARMMIND CONTINUOUS AUTONOMOUS EVOLUTION")
    print("==================================================")
    
    is_continuous = True
    if "--once" in sys.argv or "-1" in sys.argv:
        is_continuous = False

    interval = int(os.environ.get("OPTIMIZE_INTERVAL_SECONDS", "180")) # Default 3 mins between evolutionary cycles in continuous mode
    opt = StrategyOptimizer(quality_threshold_win_rate_boost=0.012, min_games=35)
    
    generation = 1
    if not is_continuous:
        run_single_cycle(opt, generation)
    else:
        print(f"Starting Endless Autonomous Mode (Cycle Interval: {interval}s)...")
        print("Press Ctrl+C or send SIGTERM to safely stop.")
        while RUNNING:
            try:
                run_single_cycle(opt, generation)
                generation += 1
            except Exception as e:
                print(f"[Optimizer Warning] Generation encountered an error: {e}")
            
            if RUNNING:
                print(f"Resting for {interval}s before Generation {generation}...")
                for _ in range(interval):
                    if not RUNNING:
                        break
                    time.sleep(1)

        print("[Optimizer] Continuous loop finished.")

if __name__ == "__main__":
    main()
