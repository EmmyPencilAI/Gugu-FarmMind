# Gugu FarmMind

Gugu FarmMind is an autonomous economic strategy agent specifically engineered for the Kaggle Kaggriculture competition. The agent couples real-time portfolio optimization, dynamic price regime classification, opponent modeling, and endgame liquidation planning to maximize final bank balance over a 30-day season.

## Overview

Gugu FarmMind is built specifically for the turn-based Kaggriculture competition environment on Kaggle. In each match, two competing farms operate concurrently across a shared economic environment governed by the following dynamics:

- **Match Horizon**: 30-day season spanning 720 discrete turns (24 turns per day).
- **Two Competing Farms**: Competitors make decisions simultaneously with publicly observable farm layouts.
- **Dynamic Market**: Commodity prices fluctuate dynamically based on overall market supply and town demand.
- **Agricultural Production**: Multiple crop varieties with distinct growth cycles, watering schedules, and fertilizer responses.
- **Livestock Management**: Animal assets requiring daily feed expenses in exchange for recurring product yields.
- **Infrastructure Expansion**: Strategic investment opportunities in additional land tiles, shed capacity, and hired farm hands.
- **Winning Condition**: Final bank balance at the conclusion of turn 720 determines the match winner. Unsold inventory does not count toward the final score.

## Core Strategy

The agent's decision engine is structured around five strategic pillars designed to maximize expected final cash ($EFC$):

### Economic Optimization

Every potential investment (crop seed, livestock, land tile, farm hand, fertilizer) is evaluated using a continuous return-on-investment (ROI) framework:

$$\text{ROI}_{\text{daily}} = \frac{\mathbb{E}[\text{Revenue}] - \text{Total Cost}}{\text{Capital Invested} \times \text{Days to Maturity}}$$

Decisions explicitly factor in:
- Expected gross revenue and input resource costs
- Time-to-production vs. days remaining in the season
- Land footprint and shed capacity utilization
- Labor and watering requirements
- Capital liquidity constraints and cash safety buffers
- Opportunity cost relative to alternative asset classes

### Dynamic Market Intelligence

The market engine tracks price histories, velocity ($\Delta P / \Delta t$), and demand regimes for each commodity, classifying market states into:
- **SCARCITY**: Price $\ge 1.3\times$ baseline; priority trigger for inventory liquidation.
- **NORMAL**: Balanced supply and demand; selective harvesting and standard sales.
- **OVERSUPPLY / CRASH**: Price depressed or rapidly falling; withholding non-perishable inventory until recovery.
- **RECOVERY**: Positive price momentum following a market trough; timed opportunistic selling.

### Production Planning

Production coordinates crops and livestock into an integrated portfolio:
- **Fast-Cycle Crops (Wheat/Corn)**: Rapid capital turnover during early season liquidity generation.
- **High-Yield Crops (Soy/Tomatoes/Berries)**: Mid-season margin expansion boosted by strategic fertilizer application.
- **Livestock (Chickens/Cows/Sheep)**: Consistent daily cash-flow streams that cushion against crop price volatility.
- **Labor & Infrastructure**: Farm hand hiring and land expansion executed only when projected marginal yield exceeds fixed and wage costs.

### Opponent Awareness

Because the opponent's farm state is publicly observable, Gugu FarmMind profiles opponent behavior into strategic archetypes (e.g., *Aggressive Expansion*, *Crop Specialist*, *Animal Specialist*, *Balanced*). The agent detects supply shocks before they materialize in market prices and diversifies into non-competing commodity sectors.

### Endgame Optimization

Because unsold inventory and unharvested crops hold zero value at match completion, Gugu FarmMind transitions into an aggressive liquidation policy during the final days (Days 24–30):
- Halts planting of crops whose growth duration exceeds the remaining days in the season.
- Ceases long-term capital expenditures (land purchases, livestock acquisitions).
- Systematically liquidates all stored goods to convert all physical assets into liquid bank balance.

## Decision Architecture

At every turn, the agent processes the latest match observation through a sequential evaluation pipeline:

```
Observation
    ↓
State Extraction
    ↓
Economic Evaluation
    ↓
Market Analysis
    ↓
Opponent Analysis
    ↓
Strategic Planning
    ↓
Action Selection
    ↓
Environment
    ↓
New Observation
```

The agent continuously recalculates its operational plan from the latest observed game state, ensuring adaptive responses to price movements and opponent actions.

## Architecture

The competition agent is completely self-contained within the execution environment:

```
Kaggle Environment
    ↓
submission.py (or main.py)
    ↓
Gugu FarmMind Decision Engine
```

The competition submission has **zero runtime dependencies** on external networks, databases, cloud servers, or API calls during active gameplay. All state parsing, economic models, heuristic planning, and action formatting execute locally and deterministically within Kaggle's per-turn time limits.

*(Note: Offline research tools, such as evolutionary parameter optimizers, historical replay analyzers, and local benchmarking suites, exist solely for development and do not run during live competition matches.)*

## Competition Runtime

Kaggle's evaluation engine directly invokes the top-level handler:

```python
def agent(obs):
    """
    Kaggriculture agent entry point.
    Receives competition observation dictionary, returns action dictionary.
    """
    return planner.plan_turn(obs)
```

The agent processes the observation dictionary and returns a validated action payload (e.g., `{"action": "PLANT", "crop": "WHEAT"}`, `{"action": "SELL", "item": "TOMATOES", "quantity": 5}`, `{"action": "BUY_LAND"}`, `{"action": "PASS"}`).

## Strategy Components

The table below outlines the core implemented modules:

| Component | Purpose |
|---|---|
| **State Management** | Tracks player cash, inventory, planted crops, livestock, land tiles, and game clock |
| **Planner** | Coordinates hierarchical decision levels and generates final per-turn actions |
| **Economy Engine** | Evaluates expected ROI, capital allocation budgets, and cash reserve buffers |
| **Market Engine** | Analyzes commodity price velocity, trend direction, and market supply regimes |
| **Crop Manager** | Schedules planting, growth tracking, watering, and fertilizer application |
| **Animal Manager** | Manages livestock acquisition, daily feed allocation, and yield harvesting |
| **Navigation** | Resolves farm-hand movement, spatial targeting, and grid pathfinding |
| **Opponent Model** | Classifies opponent farm composition to anticipate supply competition |
| **Strategy Engine** | Houses versioned policy parameters and hierarchical execution rules |

## Why Gugu FarmMind

In Kaggriculture, high production volume is not the goal—capital efficiency is.

The objective is to convert:

$$\text{LAND} + \text{TIME} + \text{LABOR} + \text{CAPITAL} + \text{MARKET OPPORTUNITY}$$

into the highest possible final bank balance.

> *"Production is only valuable when it improves the probability of winning."*

## Competition Constraints

Gugu FarmMind explicitly models and respects all competition constraints:
- **720 Total Turns**: Strict 30-day season limit (24 turns per day).
- **Land & Shed Bounds**: Fixed initial capacity requiring capital investment to expand.
- **Dynamic Pricing**: Nonlinear price degradation when markets become saturated.
- **Crop Care Requirements**: Watering cycles and maturity windows before harvest.
- **Livestock Maintenance**: Daily feeding expenses required to sustain product yields.
- **Labor Overhead**: Upfront hiring costs and recurring daily wages for farm hands.
- **Cash-Only Scoring**: Strictly cash-based ranking at turn 720.

## Development & Testing

The agent is validated locally across deterministic test suites and multi-seed Monte Carlo benchmarks against standard baseline archetypes:
- **Random Baseline**: Validates basic economic efficiency and error resilience.
- **Starter Baseline**: Benchmarks fundamental crop rotation and sales timing.
- **Aggressive & Specialist Baselines**: Evaluates counter-strategies against rapid expansion and single-crop market flooding.
- **Previous Champion Iterations**: Ensures that candidate policy mutations demonstrate positive win-rate delta prior to submission.

## Submission

To submit the agent to the Kaggle competition using the Kaggle CLI:

```bash
# Direct single-file submission
kaggle competitions submit -c kaggriculture -f submission.py -m "Gugu FarmMind"

# Root entry point submission
kaggle competitions submit -c kaggriculture -f main.py -m "Gugu FarmMind"

# Package archive submission (if using multi-file bundle)
kaggle competitions submit -c kaggriculture -f submission.tar.gz -m "Gugu FarmMind"
```

## Local Testing

To run the local validation suite and Monte Carlo benchmark:

```bash
# Validate agent imports and turn execution
python validate_agent.py

# Run Monte Carlo benchmark against local baselines
python benchmark.py
```

## Configuration

The competition agent runs with deterministic default parameters embedded in the code. Optional environment variables for the offline development toolchain include:

```bash
# Kaggle API Credentials (for CLI submissions and leaderboard sync)
KAGGLE_USERNAME="your_username"
KAGGLE_API_TOKEN="your_token"

# Offline Replay Analysis (optional development layer)
GEMINI_API_KEY="your_api_key"
```

*Note: The live competition agent does not require or use any API keys or network access during match execution.*

## Design Principles

- **Autonomous Decision-Making**: Independent heuristic decision logic with zero runtime human intervention.
- **Economic Reasoning**: ROI-driven resource allocation prioritizing high-margin capital turnover.
- **Long-Horizon Planning**: Rolling multi-day investment planning bounded by the 30-day season.
- **Market Awareness**: Supply-demand regime tracking to avoid selling into depressed markets.
- **Opponent Awareness**: Behavioral classification to counter opponent production concentrations.
- **Adaptive Strategy**: Dynamic adjustments based on current cash velocity and market shifts.
- **Endgame Awareness**: Strict asset liquidation rules ahead of match termination.
- **Deterministic and Reliable Execution**: Robust exception catching and fallback policies to ensure zero crashed turns.
- **Competition-First Optimization**: Focused strictly on final balance maximization.

## Limitations

- **Opponent Strategy Variance**: Extreme or unpredictable multi-agent behaviors can affect commodity price trajectories.
- **Market Price Volatility**: High-velocity price crashes from simultaneous opponent market dumps introduce unavoidable market risk.
- **Local Simulation Divergence**: Local benchmarks against baseline bots provide directional signal but cannot replicate the full live Kaggle leaderboard distribution.
- **Empirical Dependency**: Policy parameters require continuous empirical evaluation against emerging meta strategies.

## Future Development

- **Enhanced Opponent Modeling**: Bayesian belief updating over opponent cash reserves and unobserved inventory.
- **Nonlinear Price Forecasting**: Multi-step autoregressive price estimators trained on competition replay datasets.
- **Broader Strategy Search**: Covariance matrix adaptation evolution strategy (CMA-ES) for parameter optimization.
- **Fine-Grained Spatial Planning**: Coordinated multi-worker pathfinding optimization on expanded grid layouts.
- **Expanded Benchmark Sets**: Automated adversarial self-play frameworks to discover novel meta-strategies.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Author

**Gugu Robotics**  
Agent: *Gugu FarmMind*
