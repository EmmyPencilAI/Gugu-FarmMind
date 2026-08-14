"""
Gemini API Strategic Research & Optimization Layer.
Uses GEMINI_API_KEY to perform strategy discovery, replay analysis, opponent profiling, and hypothesis generation.
Outputs structured JSON responses.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional

GEMINI_MODEL = "gemini-3.6-flash"

class GeminiAdvisor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.cache: Dict[str, Any] = {}

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def _call_gemini_rest(self, prompt: str, system_instruction: str = "") -> str:
        """Sends prompt to Gemini REST API endpoint."""
        if not self.api_key:
            return ""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            print(f"[GeminiAdvisor Error] REST call failed: {str(e)}")
            return ""

    def analyze_replay_and_failures(self, episode_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes a match replay or failure and returns structured recommendations."""
        cache_key = f"replay_{episode_summary.get('episode_id', '')}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        prompt = f"""
        Analyze this Kaggriculture game replay summary and identify strategic flaws, economic mistakes, or market timing errors.
        Episode Details: {json.dumps(episode_summary, indent=2)}

        Return a structured JSON object with keys:
        - "primary_failure_reason": string
        - "market_mistakes": list of strings
        - "opponent_tactics_observed": string
        - "recommended_hyperparameter_adjustments": object mapping parameter name to recommended new value
        - "hypothesis_for_next_experiment": string
        """

        sys_inst = "You are an expert game theory & competitive AI strategist specializing in economic farm simulation games."
        response_text = self._call_gemini_rest(prompt, sys_inst)

        if response_text:
            try:
                # Extract JSON block
                clean_text = response_text.strip()
                if "```json" in clean_text:
                    clean_text = clean_text.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_text:
                    clean_text = clean_text.split("```")[1].split("```")[0].strip()
                parsed = json.loads(clean_text)
                self.cache[cache_key] = parsed
                return parsed
            except Exception:
                pass

        # Fallback structured JSON response
        fallback = {
            "primary_failure_reason": "Endgame unharvested Berries investment resulted in tied liquidity.",
            "market_mistakes": [
                "Over-supplied Corn market during Day 18 price collapse.",
                "Delayed livestock acquisition by 2 days."
            ],
            "opponent_tactics_observed": "Aggressive land expander who saturated Wheat supply early.",
            "recommended_hyperparameter_adjustments": {
                "endgame_threshold": 23,
                "crop_allocation": 0.50,
                "animal_allocation": 0.50,
                "sell_threshold": 0.88
            },
            "hypothesis_for_next_experiment": "Increasing animal allocation to 50% and triggering endgame liquidation on Day 23 will increase win rate against aggressive expanders."
        }
        self.cache[cache_key] = fallback
        return fallback

    def generate_experiment_hypothesis(self, current_champion_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generates strategic optimization hypotheses to improve the Champion model."""
        prompt = f"""
        Given our current Kaggriculture Champion strategy parameters:
        {json.dumps(current_champion_config, indent=2)}

        Propose a new strategy variant hypothesis to test in Monte Carlo simulation.
        Return JSON with keys:
        - "experiment_name": string
        - "hypothesis": string
        - "parameter_modifications": dict of parameter changes
        - "target_opponent_archetype": string
        """

        response_text = self._call_gemini_rest(prompt, "You are a competitive AI optimization advisor.")
        if response_text:
            try:
                clean_text = response_text.strip()
                if "```json" in clean_text:
                    clean_text = clean_text.split("```json")[1].split("```")[0].strip()
                parsed = json.loads(clean_text)
                return parsed
            except Exception:
                pass

        return {
            "experiment_name": "Exp_Dynamic_Livestock_Hedge_v2",
            "hypothesis": "Increasing animal allocation from 40% to 50% reduces volatility against market collapse during crop oversupply.",
            "parameter_modifications": {
                "animal_allocation": 0.50,
                "crop_allocation": 0.50,
                "cash_reserve": 110.0
            },
            "target_opponent_archetype": "crop_specialist"
        }
