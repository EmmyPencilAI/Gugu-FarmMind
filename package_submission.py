"""
Kaggle Submission Packaging Script.
Validates quality gates, verifies main.py execution, and packages submission.tar.gz.
"""

import os
import tarfile
import sys
import subprocess
from kaggriculture.strategy import get_default_champion
from db import get_champion_strategy

def package():
    print("==================================================")
    print(" PACKAGING KAGGRICULTURE AGENT FOR KAGGLE")
    print("==================================================")

    # 1. Verify main.py existence
    if not os.path.exists("main.py"):
        print("ERROR: main.py not found!")
        sys.exit(1)

    # 2. Syntax & Execution Verification of main.py
    print("1. Verifying main.py self-contained agent execution...")
    try:
        from main import agent
        test_obs = {"day": 1, "cash": 200.0, "inventory": {}, "market_prices": {}}
        res = agent(test_obs)
        if not isinstance(res, dict) or "action" not in res:
            raise ValueError("main.py agent() did not return a valid action dictionary.")
        print("   ✓ main.py agent() execution test PASSED.")
    except Exception as e:
        print(f"ERROR: main.py execution check failed: {str(e)}")
        sys.exit(1)

    # 3. Quality Gate Verification
    print("2. Checking Champion Strategy Quality Gate...")
    champ = get_champion_strategy() or get_default_champion().to_dict()
    win_rate = champ.get("win_rate", 0.0)
    print(f"   Champion ID: {champ.get('strategy_id')} | Win Rate: {round(win_rate*100, 2)}%")
    
    if win_rate < 0.50:
        print("WARNING: Champion win rate is below 50% quality threshold. Submitting with caution.")

    # 4. Create submission.tar.gz
    archive_name = "submission.tar.gz"
    print(f"3. Bundling main.py into {archive_name}...")
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add("main.py", arcname="main.py")

    file_size_kb = round(os.path.getsize(archive_name) / 1024, 2)
    print(f"   ✓ Created {archive_name} ({file_size_kb} KB).")
    print("==================================================")
    print(" SUBMISSION ARCHIVE READY FOR KAGGLE DEPLOYMENT!")
    print("==================================================")

if __name__ == "__main__":
    package()
