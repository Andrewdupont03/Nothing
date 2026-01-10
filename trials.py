import sqlite3
from config import FREE_TRIALS

DB = "database.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            trials INTEGER,
            premium INTEGER DEFAULT 0
        )
        """)

def get_user(user_id):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT trials, premium FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        if row is None:
            cur.execute(
                "INSERT INTO users (user_id, trials, premium) VALUES (?, ?, 0)",
                (user_id, FREE_TRIALS)
            )
            conn.commit()
            return FREE_TRIALS, 0
        return row

def can_use(user_id) -> bool:
    trials, premium = get_user(user_id)
    return premium == 1 or trials > 0

def consume_trial(user_id):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "UPDATE users SET trials = trials - 1 WHERE user_id=? AND premium=0",
            (user_id,)
        )
        conn.commit()

def set_premium(user_id):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "UPDATE users SET premium=1 WHERE user_id=?",
            (user_id,)
        )
        conn.commit()
