-- Kaggriculture PostgreSQL Database Schema for Render Cloud SQL / Postgres

CREATE TABLE IF NOT EXISTS strategies (
    strategy_id VARCHAR(64) PRIMARY KEY,
    version VARCHAR(32) NOT NULL,
    name VARCHAR(128) NOT NULL,
    status VARCHAR(32) NOT NULL, -- EXPERIMENTAL, CANDIDATE, CHAMPION, RETIRED
    config_json JSONB NOT NULL,
    win_rate DOUBLE PRECISION DEFAULT 0.0,
    avg_cash DOUBLE PRECISION DEFAULT 0.0,
    simulation_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS experiments (
    experiment_id VARCHAR(64) PRIMARY KEY,
    hypothesis TEXT NOT NULL,
    strategy_id VARCHAR(64) REFERENCES strategies(strategy_id),
    status VARCHAR(32) NOT NULL,
    benchmark_results_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS simulations (
    sim_id VARCHAR(64) PRIMARY KEY,
    strategy_id VARCHAR(64) REFERENCES strategies(strategy_id),
    num_games INTEGER NOT NULL,
    win_rate DOUBLE PRECISION NOT NULL,
    avg_cash DOUBLE PRECISION NOT NULL,
    worst_case DOUBLE PRECISION NOT NULL,
    best_case DOUBLE PRECISION NOT NULL,
    details_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS submissions (
    submission_id VARCHAR(64) PRIMARY KEY,
    strategy_id VARCHAR(64) REFERENCES strategies(strategy_id),
    version VARCHAR(32) NOT NULL,
    kaggle_submission_id VARCHAR(64),
    status VARCHAR(32) NOT NULL,
    score DOUBLE PRECISION DEFAULT 0.0,
    leaderboard_rank INTEGER,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS episodes (
    episode_id VARCHAR(64) PRIMARY KEY,
    submission_id VARCHAR(64) REFERENCES submissions(submission_id),
    opponent_name VARCHAR(128) NOT NULL,
    result VARCHAR(16) NOT NULL,
    our_cash DOUBLE PRECISION NOT NULL,
    opp_cash DOUBLE PRECISION NOT NULL,
    replay_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS opponents (
    opponent_id VARCHAR(64) PRIMARY KEY,
    rating DOUBLE PRECISION DEFAULT 1500.0,
    estimated_strategy VARCHAR(64) NOT NULL,
    win_count INTEGER DEFAULT 0,
    loss_count INTEGER DEFAULT 0,
    observed_weaknesses_json JSONB,
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS optimization_runs (
    run_id VARCHAR(64) PRIMARY KEY,
    generation INTEGER NOT NULL,
    best_strategy_id VARCHAR(64) REFERENCES strategies(strategy_id),
    win_rate DOUBLE PRECISION NOT NULL,
    log_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_observations (
    observation_id VARCHAR(64) PRIMARY KEY,
    day INTEGER NOT NULL,
    item_name VARCHAR(64) NOT NULL,
    current_price DOUBLE PRECISION NOT NULL,
    velocity DOUBLE PRECISION DEFAULT 0.0,
    regime VARCHAR(32) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS replay_analysis (
    analysis_id VARCHAR(64) PRIMARY KEY,
    episode_id VARCHAR(64) REFERENCES episodes(episode_id),
    diagnostics TEXT NOT NULL,
    weaknesses TEXT NOT NULL,
    hypotheses TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(64) PRIMARY KEY,
    job_type VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL,
    idempotency_key VARCHAR(128) UNIQUE,
    logs TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_events (
    event_id VARCHAR(64) PRIMARY KEY,
    event_type VARCHAR(64) NOT NULL,
    payload_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
