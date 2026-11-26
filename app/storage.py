"""Where the data is kept.

Players and their scores live in a SQLite database file (pypython.db in the
project folder; set the environment variable PYPYTHON_DB to use another file).

The rest of the app only uses the functions below, so main.py does not need to
know how the data is stored.

The two functions at the bottom (all_entries, add_entry) are left over from the
"Things to bring" example. They are still used by the start page and will be
removed when the page is replaced.
"""

import os
import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(os.environ.get("PYPYTHON_DB", Path(__file__).parent.parent / "pypython.db"))


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the tables if they do not exist yet."""
    with closing(_connect()) as conn, conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                username   TEXT PRIMARY KEY COLLATE NOCASE,
                high_score INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS scores (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE REFERENCES users(username),
                score    INTEGER NOT NULL,
                mode     TEXT NOT NULL
            );
            """
        )


def get_user(name):
    """Return {"username", "high_score"} for this name (any spelling of upper and lower case), or None."""
    with closing(_connect()) as conn:
        row = conn.execute("SELECT username, high_score FROM users WHERE username = ?", (name,)).fetchone()
    return dict(row) if row else None


def create_user(name):
    """Create a player and return it, or return None if the name is already taken."""
    try:
        with closing(_connect()) as conn, conn:
            conn.execute("INSERT INTO users (username) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        return None
    return {"username": name, "high_score": 0}


def add_score(name, score, mode):
    """Save one finished game. Return {"high_score", "new_record"}, or None if the player does not exist."""
    with closing(_connect()) as conn, conn:
        user = conn.execute("SELECT username, high_score FROM users WHERE username = ?", (name,)).fetchone()
        if user is None:
            return None
        conn.execute(
            "INSERT INTO scores (username, score, mode) VALUES (?, ?, ?)", (user["username"], score, mode)
        )
        record = score > user["high_score"]
        if record:
            conn.execute("UPDATE users SET high_score = ? WHERE username = ?", (score, user["username"]))
    return {"high_score": max(score, user["high_score"]), "new_record": record}


def top_scores(mode, limit=10):
    """Each player's best score in one game mode, highest first: [{"username", "score"}, ...]."""
    with closing(_connect()) as conn:
        rows = conn.execute(
            "SELECT username, MAX(score) AS score FROM scores WHERE mode = ? "
            "GROUP BY username ORDER BY score DESC, username LIMIT ?",
            (mode, limit),
        ).fetchall()
    return [dict(r) for r in rows]


# --- left over from the example, removed later -------------------------------

_entries = []
_next_id = 1


def all_entries():
    """Return a copy of all entries, oldest first."""
    return list(_entries)


def add_entry(thing, person):
    """Store a new entry and return it."""
    global _next_id
    entry = {"id": _next_id, "thing": thing, "person": person}
    _entries.append(entry)
    _next_id += 1
    return entry
