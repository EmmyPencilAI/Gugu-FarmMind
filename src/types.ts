export interface StrategyConfig {
  strategy_id: string;
  version: string;
  name: string;
  status: "EXPERIMENTAL" | "CANDIDATE" | "CHAMPION" | "RETIRED";
  cash_reserve: number;
  crop_allocation: number;
  animal_allocation: number;
  land_threshold: number;
  hire_threshold: number;
  fertilizer_threshold: number;
  sell_threshold: number;
  market_pressure_weight: number;
  opponent_weight: number;
  risk_tolerance: number;
  endgame_threshold: number;
  simulation_count: number;
  win_rate: number;
  average_final_cash: number;
  median_final_cash: number;
  worst_case_cash: number;
  best_case_cash: number;
  description: string;
}

export interface PlatformStatus {
  status: string;
  platform: string;
  champion: {
    id: string;
    version: string;
    name: string;
    win_rate: number;
    avg_cash: number;
    status: string;
  };
  kaggle: {
    competition: string;
    rank: number;
    rating: number;
    status: string;
  };
  gemini: {
    status: string;
    model: string;
  };
  last_test_run?: any;
}

export interface MarketCommodity {
  current_price: number;
  base_price: number;
  velocity: number;
  regime: string;
  forecast_3d: number[];
}

export interface OpponentProfile {
  opponent_id: string;
  classification: string;
  win_rate_vs_us: number;
  weaknesses: string[];
  counter_tactics: string;
}
