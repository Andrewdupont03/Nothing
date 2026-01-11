import sqlite3
from config import FREE_TRIALS

DB = "database.db"


def init_db():
    """Initialise la base SQLite et la table users"""
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            trials INTEGER,
            premium INTEGER DEFAULT 0
        )
        """)


def get_user(user_id: int):
    """
    Récupère le nombre d'essais et le statut premium
    Crée l'utilisateur s'il n'existe pas
    """
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


def can_use(user_id: int) -> bool:
    """
    Retourne True si l'utilisateur peut utiliser le bot
    (soit premium, soit essais restants > 0)
    """
    trials, premium = get_user(user_id)
    return premium == 1 or trials > 0


def consume_trial(user_id: int):
    """
    Décrémente un essai si l'utilisateur n'est pas premium
    """
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "UPDATE users SET trials = trials - 1 WHERE user_id=? AND premium=0 AND trials>0",
            (user_id,)
        )
        conn.commit()


def set_premium(user_id: int):
    """
    Active le premium pour un utilisateur
    """
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "UPDATE users SET premium=1 WHERE user_id=?",
            (user_id,)
        )
        conn.commit()


def trials_left(user_id: int) -> int:
    """
    Retourne le nombre d'essais restants (0 si épuisés)
    """
    trials, premium = get_user(user_id)
    return trials if premium == 0 else float('inf')
