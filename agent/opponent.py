"""
Gugu FarmMind Opponent Meta-Intelligence Module
Classifies opponent archetypes, estimates hidden economic state, and recommends counter-tactics.
"""

class OpponentClassifier:
    ARCHETYPES = [
        "AGGRESSIVE_EXPANSION",
        "CROP_SPECIALIST",
        "ANIMAL_SPECIALIST",
        "MARKET_TRADER",
        "BALANCED",
        "CONSERVATIVE",
        "UNKNOWN"
    ]

    def classify(self, opponent_data):
        if not opponent_data or not isinstance(opponent_data, dict):
            return "BALANCED"

        crops = len(opponent_data.get("observed_crops", []))
        animals = len(opponent_data.get("observed_animals", []))
        land = opponent_data.get("land_tiles", 10)

        if land >= 15:
            return "AGGRESSIVE_EXPANSION"
        elif crops > 3 * max(1, animals):
            return "CROP_SPECIALIST"
        elif animals > 2 * max(1, crops):
            return "ANIMAL_SPECIALIST"
        else:
            return "BALANCED"

    def recommend_counter_tactic(self, archetype):
        if archetype == "AGGRESSIVE_EXPANSION":
            return "Focus on fast-maturing cash crops (Wheat/Corn) to undercut market before opponent yields mature."
        elif archetype == "CROP_SPECIALIST":
            return "Diversify into livestock (Chicken/Cow) to produce steady daily yields resilient to crop price crashes."
        elif archetype == "ANIMAL_SPECIALIST":
            return "Flooding high-value crop markets (Tomatoes/Berries) when price spikes occur."
        else:
            return "Execute balanced optimal ROI allocation strategy."
