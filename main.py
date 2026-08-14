"""
Gugu FarmMind Production Agent Entry Point (Root)
Target submission entry point for Kaggle Kaggriculture competition.
Self-contained execution for Kaggle competition runner.
"""

from agent.main import agent

# Expose agent function directly at root module level for Kaggle
__all__ = ["agent"]
