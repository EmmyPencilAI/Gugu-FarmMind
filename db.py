"""
PostgreSQL (Supabase / Render) & SQLite Database Persistence Client for Gugu FarmMind Platform.
Supports strategies, experiments, simulations, submissions, episodes, opponents, market_observations, jobs, system_events.
Self-healing with automatic fallback, recovery, and connection management.
"""

import os
import time
import json
import sqlite3
from typing import Dict, List, Any, Optional

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
DB_FILE = os.path.join(os.path.dirname(__file__), "kaggriculture.db")

IS_POSTGRES = bool(DATABASE_URL and DATABASE_URL.startswith(("postgres://", "postgresql://")))

if IS_POSTGRES:
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
    except ImportError:
        IS_POSTGRES = False

class DBConnection:
    def __init__(self):
        self.is_pg = IS_POSTGRES
        self.conn = None

    def __enter__(self):
        if self.is_pg:
            try:
                import psycopg2
                from psycopg2.extras import RealDictCursor
                # Fix postgres:// URI for newer psycopg2 if needed
                pg_url = DATABASE_URL
                if pg_url.startswith("postgres://"):
                    pg_url = pg_url.replace("postgres://", "postgresql://", 1)
                self.conn = psycopg2.connect(pg_url, cursor_factory=RealDictCursor)
                return self.conn
            except Exception as e:
                print(f"[DB Warning] Failed connecting to PostgreSQL ({e}). Falling back to SQLite.")
                self.is_pg = False

        # SQLite Connection with automatic corruption recovery
        try:
            self.conn = sqlite3.connect(DB_FILE)
            self.conn.row_factory = sqlite3.Row
            # Quick integrity check
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA quick_check;")
            row = cursor.fetchone()
            if row and row[0] != "ok":
                raise sqlite3.DatabaseError("Corrupted database detected by PRAGMA quick_check")
        except (sqlite3.DatabaseError, Exception) as e:
            print(f"[DB Recovery] Detected corrupted SQLite database ({e}). Rebuilding clean database...")
            try:
                if self.conn:
                    self.conn.close()
            except Exception:
                pass
            if os.path.exists(DB_FILE):
                try:
                    os.remove(DB_FILE)
                except Exception:
                    pass
            self.conn = sqlite3.connect(DB_FILE)
            self.conn.row_factory = sqlite3.Row

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            try:
                if exc_type is None:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception:
                pass
            finally:
                try:
                    self.conn.close()
                except Exception:
                    pass

def get_connection():
    return DBConnection()

def init_db():
    """Initializes schema on PostgreSQL or SQLite safely."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # SQLite schema
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
            idempotency_key TEXT,
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

def save_strategy(strategy_dict: Dict[str, Any]):
    with get_connection() as conn:
        cursor = conn.cursor()
        # Use portable parameter query
        strategy_id = strategy_dict.get("strategy_id")
        # Try update first
        cursor.execute("""
        DELETE FROM strategies WHERE strategy_id = ?
        """, (strategy_id,))
        
        cursor.execute("""
        INSERT INTO strategies 
        (strategy_id, version, name, status, config_json, win_rate, avg_cash, simulation_count, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            strategy_id,
            strategy_dict.get("version", "1.0.0"),
            strategy_dict.get("name", "Gugu FarmMind Strategy"),
            strategy_dict.get("status", "CHAMPION"),
            json.dumps(strategy_dict),
            float(strategy_dict.get("win_rate", 0.0)),
            float(strategy_dict.get("average_final_cash", 0.0)),
            int(strategy_dict.get("simulation_count", 0)),
            float(strategy_dict.get("timestamp", time.time()))
        ))

def get_all_strategies() -> List[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT config_json FROM strategies ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [json.loads(row["config_json"] if isinstance(row, dict) or hasattr(row, "keys") else row[0]) for row in rows]
    except Exception as e:
        print(f"[DB Error] get_all_strategies: {e}")
        return []

def get_champion_strategy() -> Optional[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT config_json FROM strategies WHERE status = 'CHAMPION' ORDER BY created_at DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                config_str = row["config_json"] if isinstance(row, dict) or hasattr(row, "keys") else row[0]
                return json.loads(config_str)
    except Exception as e:
        print(f"[DB Error] get_champion_strategy: {e}")
    return None

# Safe initial table creation on module import
try:
    init_db()
except Exception as err:
    print(f"[DB Error during init_db]: {err}")
