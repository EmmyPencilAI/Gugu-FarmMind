"""
PostgreSQL / SQLite Database Persistence Client for Kaggriculture Platform.
Supports strategies, experiments, simulations, submissions, episodes, opponents, market_observations, strategy_events, optimization_runs.
"""

import sqlite3
import json
import os
import time
from typing import Dict, List, Any, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "kaggriculture.db")

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create Tables if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategies (
        strategy_id TEXT PRIMARY KEY,
        version TEXT,
        name TEXT,
        status TEXT,
        config_json TEXT,
        win_rate REAL,
        avg_cash REAL,
        simulation_count INTEGER,
        created_at REAL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        experiment_id TEXT PRIMARY KEY,
        hypothesis TEXT,
        strategy_id TEXT,
        status TEXT,
        benchmark_results_json TEXT,
        created_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulations (
        sim_id TEXT PRIMARY KEY,
        strategy_id TEXT,
        num_games INTEGER,
        win_rate REAL,
        avg_cash REAL,
        worst_case REAL,
        best_case REAL,
        details_json TEXT,
        created_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        submission_id TEXT PRIMARY KEY,
        strategy_id TEXT,
        version TEXT,
        kaggle_submission_id TEXT,
        status TEXT,
        score REAL,
        leaderboard_rank INTEGER,
        submitted_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        episode_id TEXT PRIMARY KEY,
        submission_id TEXT,
        opponent_name TEXT,
        result TEXT,
        our_cash REAL,
        opp_cash REAL,
        replay_url TEXT,
        created_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opponents (
        opponent_id TEXT PRIMARY KEY,
        rating REAL,
        estimated_strategy TEXT,
        win_count INTEGER,
        loss_count INTEGER,
        observed_weaknesses_json TEXT,
        last_seen REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS optimization_runs (
        run_id TEXT PRIMARY KEY,
        generation INTEGER,
        best_strategy_id TEXT,
        win_rate REAL,
        log_message TEXT,
        created_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_observations (
        observation_id TEXT PRIMARY KEY,
        day INTEGER,
        item_name TEXT,
        current_price REAL,
        velocity REAL,
        regime TEXT,
        created_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS replay_analysis (
        analysis_id TEXT PRIMARY KEY,
        episode_id TEXT,
        diagnostics TEXT,
        weaknesses TEXT,
        hypotheses TEXT,
        created_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        job_type TEXT,
        status TEXT,
        idempotency_key TEXT UNIQUE,
        logs TEXT,
        created_at REAL,
        updated_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_events (
        event_id TEXT PRIMARY KEY,
        event_type TEXT,
        payload_json TEXT,
        created_at REAL
    )
    """)

    conn.commit()
    conn.close()

# Initialize DB on load
init_db()

def save_strategy(strategy_dict: Dict[str, Any]):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO strategies 
    (strategy_id, version, name, status, config_json, win_rate, avg_cash, simulation_count, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        strategy_dict.get("strategy_id"),
        strategy_dict.get("version"),
        strategy_dict.get("name"),
        strategy_dict.get("status"),
        json.dumps(strategy_dict),
        strategy_dict.get("win_rate", 0.0),
        strategy_dict.get("average_final_cash", 0.0),
        strategy_dict.get("simulation_count", 0),
        strategy_dict.get("timestamp", time.time())
    ))
    conn.commit()
    conn.close()

def get_all_strategies() -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT config_json FROM strategies ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [json.loads(row["config_json"]) for row in rows]

def get_champion_strategy() -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT config_json FROM strategies WHERE status = 'CHAMPION' ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row["config_json"])
    return None
