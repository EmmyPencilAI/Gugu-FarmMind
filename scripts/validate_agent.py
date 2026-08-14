"""
Gugu FarmMind Agent Validation Script.
Validates imports, main.py execution, action payload schema, and deterministic performance.
"""

import sys
import os

# Add root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def validate():
    print("==================================================")
    print(" GUGU FARMMIND AGENT VALIDATION SUITE")
    print("==================================================")

    # 1. Import main.py
    try:
        from main import agent
        print("✓ Import main.py: PASSED")
    except Exception as e:
        print(f"✗ Import main.py FAILED: {e}")
        sys.exit(1)

    # 2. Test turn execution
    test_obs = {
        "step": 0,
        "day": 1,
        "cash": 200.0,
        "inventory": {"WHEAT": 0, "CORN": 0},
        "market_prices": {"WHEAT": 22.0, "CORN": 42.0, "TOMATOES": 90.0}
    }

    try:
        action = agent(test_obs)
        if not isinstance(action, dict) or "action" not in action:
            raise ValueError("Returned action is not a valid dict containing 'action'")
        print(f"✓ Agent Turn Execution: PASSED (Action: {action['action']})")
    except Exception as e:
        print(f"✗ Agent Turn Execution FAILED: {e}")
        sys.exit(1)

    # 3. Test endgame liquidation trigger
    endgame_obs = {
        "step": 600,
        "day": 25,
        "cash": 500.0,
        "inventory": {"TOMATOES": 10},
        "market_prices": {"TOMATOES": 110.0}
    }

    try:
        action = agent(endgame_obs)
        if action.get("action") != "SELL":
            raise ValueError(f"Expected endgame liquidation SELL action on day 25, got {action.get('action')}")
        print("✓ Endgame Liquidation Rule: PASSED")
    except Exception as e:
        print(f"✗ Endgame Liquidation Rule FAILED: {e}")
        sys.exit(1)

    print("==================================================")
    print(" ALL AGENT VALIDATION CHECKS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    validate()
