import sqlite3
from contextlib import closing

DB_NAME = "dashquiz.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        # Groupes Telegram
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                chat_id INTEGER PRIMARY KEY,
                title TEXT DEFAULT '',
                language TEXT DEFAULT 'fr',
                quiz_enabled INTEGER DEFAULT 1,
                interval_minutes INTEGER DEFAULT 60,
                difficulty TEXT DEFAULT 'all',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Scores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                chat_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT DEFAULT '',
                first_name TEXT DEFAULT '',
                points INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                wrong_answers INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                PRIMARY KEY (chat_id, user_id)
            )
        """)

        conn.commit()


# ============================================================
# GROUPES
# ============================================================

def save_group(chat_id, title=""):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO groups (chat_id, title)
            VALUES (?, ?)
            ON CONFLICT(chat_id)
            DO UPDATE SET title = excluded.title
        """, (chat_id, title))

        conn.commit()


def get_group(chat_id):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM groups
            WHERE chat_id = ?
        """, (chat_id,))

        return cursor.fetchone()


def get_all_groups():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM groups
            WHERE quiz_enabled = 1
        """)

        return cursor.fetchall()


def set_language(chat_id, language):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE groups
            SET language = ?
            WHERE chat_id = ?
        """, (language, chat_id))

        conn.commit()


def set_quiz_enabled(chat_id, enabled):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE groups
            SET quiz_enabled = ?
            WHERE chat_id = ?
        """, (1 if enabled else 0, chat_id))

        conn.commit()


def set_interval(chat_id, minutes):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE groups
            SET interval_minutes = ?
            WHERE chat_id = ?
        """, (minutes, chat_id))

        conn.commit()


def set_difficulty(chat_id, difficulty):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE groups
            SET difficulty = ?
            WHERE chat_id = ?
        """, (difficulty, chat_id))

        conn.commit()


# ============================================================
# SCORES
# ============================================================

def ensure_user(chat_id, user_id, username="", first_name=""):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO scores (
                chat_id,
                user_id,
                username,
                first_name
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(chat_id, user_id)
            DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name
        """, (
            chat_id,
            user_id,
            username or "",
            first_name or ""
        ))

        conn.commit()


def add_correct_answer(chat_id, user_id, username, first_name):
    ensure_user(
        chat_id,
        user_id,
        username,
        first_name
    )

    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE scores
            SET
                points = points + 10,
                correct_answers = correct_answers + 1,
                streak = streak + 1,
                best_streak = CASE
                    WHEN streak + 1 > best_streak
                    THEN streak + 1
                    ELSE best_streak
                END
            WHERE chat_id = ?
            AND user_id = ?
        """, (chat_id, user_id))

        conn.commit()


def add_wrong_answer(chat_id, user_id, username, first_name):
    ensure_user(
        chat_id,
        user_id,
        username,
        first_name
    )

    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE scores
            SET
                wrong_answers = wrong_answers + 1,
                streak = 0
            WHERE chat_id = ?
            AND user_id = ?
        """, (chat_id, user_id))

        conn.commit()


def get_user_score(chat_id, user_id):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM scores
            WHERE chat_id = ?
            AND user_id = ?
        """, (chat_id, user_id))

        return cursor.fetchone()


def get_leaderboard(chat_id, limit=10):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM scores
            WHERE chat_id = ?
            ORDER BY points DESC, correct_answers DESC
            LIMIT ?
        """, (chat_id, limit))

        return cursor.fetchall()
