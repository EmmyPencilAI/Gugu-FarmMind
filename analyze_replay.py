"""
Replay Analysis CLI Tool powered by Gemini Advisor.
"""

import sys
import json
from gemini_advisor import GeminiAdvisor
from kaggle_client import KaggleClient

def main():
    print("Fetching recent match episode replays from Kaggle API...")
    kaggle = KaggleClient()
    episodes = kaggle.list_episodes()
    
    if not episodes:
        print("No episodes found.")
        return
        
    latest_ep = episodes[0]
    print(f"Analyzing Episode {latest_ep['episode_id']} vs {latest_ep['opponent']}...")

    gemini = GeminiAdvisor()
    analysis = gemini.analyze_replay_and_failures(latest_ep)
    
    print("==================================================")
    print(" GEMINI REPLAY ANALYSIS & STRATEGIC FEEDBACK")
    print(f" Failure / Flaw: {analysis.get('primary_failure_reason')}")
    print(f" Observed Opponent Tactics: {analysis.get('opponent_tactics_observed')}")
    print(f" Recommended Parameter Adjustments: {json.dumps(analysis.get('recommended_hyperparameter_adjustments'), indent=2)}")
    print(f" Next Experiment Hypothesis: {analysis.get('hypothesis_for_next_experiment')}")
    print("==================================================")

if __name__ == "__main__":
    main()
