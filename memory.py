"""
Short-term conversational memory backed by SQLite.

Stores chat messages per Streamlit session so follow-up questions can use
prior context during retrieval and answer generation.
"""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent
MEMORY_DB_PATH = PROJECT_ROOT / "data" / "chat_memory.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, id);
"""


def _connect() -> sqlite3.Connection:
    MEMORY_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(MEMORY_DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(CREATE_TABLE_SQL)


def new_session_id() -> str:
    return str(uuid.uuid4())


def add_message(session_id: str, role: str, content: str) -> None:
    init_db()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content),
        )
        conn.commit()


def get_messages(session_id: str, *, limit: int = 20) -> list[dict]:
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT role, content FROM messages
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit),
        ).fetchall()
    return [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]


def clear_session(session_id: str) -> None:
    init_db()
    with _connect() as conn:
        conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        conn.commit()


def sync_messages(session_id: str, messages: list[dict]) -> None:
    """Replace DB history with the in-memory message list (e.g. after clear)."""
    clear_session(session_id)
    for msg in messages:
        add_message(session_id, msg["role"], msg["content"])
