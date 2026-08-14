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

export interface DailyQuotaInfo {
  used_today: number;
  max_daily: number;
  remaining_today: number;
  can_submit: boolean;
  active_ladder_bots: Array<{
    submission_id: string;
    version: string;
    score?: number;
    estimated_rating?: number;
    status: string;
    is_active_ladder?: boolean;
    submitted_at?: number;
  }>;
  all_recent_submissions?: any[];
}

export interface MistakeRecord {
  mistake_id: string;
  opponent_archetype: string;
  turn_failed: number;
  failure_category: string;
  root_cause: string;
  counter_action_taken: string;
  loss_margin: number;
  created_at: number;
}

export interface PlatformStatus {
  status: string;
  platform: string;
  autonomous?: {
    is_running: boolean;
    started_at: number | null;
    generations_completed: number;
    last_log: string;
    last_result?: any;
  };
  quota?: DailyQuotaInfo;
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
    rules?: {
      max_daily_submissions: number;
      active_tracked_submissions: number;
      scoring_system: string;
    };
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
