import sqlite3
from contextlib import closing


DB_NAME = "dashquiz.db"


# ============================================================
# CONNEXION
# ============================================================

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# ============================================================
# INITIALISATION
# ============================================================

def init_database():

    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        # ----------------------------------------------------
        # GROUPES TELEGRAM
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # SCORES
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # QUESTIONS UTILISÉES
        #
        # Cette table empêche DashQuiz de répéter
        # une question dans un même groupe.
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS used_questions (
                chat_id INTEGER NOT NULL,
                question_id TEXT NOT NULL,

                used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY (chat_id, question_id)
            )
        """)

        # ----------------------------------------------------
        # CYCLE DES QUESTIONS
        #
        # Permet de savoir quelles questions ont déjà été
        # utilisées dans le cycle actuel.
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_cycles (
                chat_id INTEGER PRIMARY KEY,
                cycle_number INTEGER DEFAULT 1,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            INSERT INTO groups (
                chat_id,
                title
            )
            VALUES (?, ?)

            ON CONFLICT(chat_id)
            DO UPDATE SET
                title = excluded.title
        """, (
            chat_id,
            title or ""
        ))

        # Créer également le cycle du groupe
        cursor.execute("""
            INSERT OR IGNORE INTO question_cycles (
                chat_id,
                cycle_number
            )
            VALUES (?, 1)
        """, (chat_id,))

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


# ============================================================
# LANGUE
# ============================================================

def set_language(chat_id, language):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE groups
            SET language = ?
            WHERE chat_id = ?
        """, (
            language,
            chat_id
        ))

        conn.commit()


# ============================================================
# QUIZ ACTIVÉ / DÉSACTIVÉ
# ============================================================

def set_quiz_enabled(chat_id, enabled):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE groups
            SET quiz_enabled = ?
            WHERE chat_id = ?
        """, (
            1 if enabled else 0,
            chat_id
        ))

        conn.commit()


# ============================================================
# FRÉQUENCE
# ============================================================

def set_interval(chat_id, minutes):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE groups
            SET interval_minutes = ?
            WHERE chat_id = ?
        """, (
            minutes,
            chat_id
        ))

        conn.commit()


# ============================================================
# DIFFICULTÉ
# ============================================================

def set_difficulty(chat_id, difficulty):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE groups
            SET difficulty = ?
            WHERE chat_id = ?
        """, (
            difficulty,
            chat_id
        ))

        conn.commit()


# ============================================================
# QUESTIONS UTILISÉES
# ============================================================

def is_question_used(chat_id, question_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1
            FROM used_questions
            WHERE chat_id = ?
            AND question_id = ?

            LIMIT 1
        """, (
            chat_id,
            question_id
        ))

        return cursor.fetchone() is not None


def mark_question_used(chat_id, question_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO used_questions (
                chat_id,
                question_id
            )
            VALUES (?, ?)
        """, (
            chat_id,
            question_id
        ))

        conn.commit()


def get_used_question_ids(chat_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT question_id
            FROM used_questions
            WHERE chat_id = ?
        """, (chat_id,))

        rows = cursor.fetchall()

        return {
            row["question_id"]
            for row in rows
        }


def count_used_questions(chat_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM used_questions
            WHERE chat_id = ?
        """, (chat_id,))

        row = cursor.fetchone()

        return row["total"]


# ============================================================
# NOUVEAU CYCLE
# ============================================================

def reset_question_cycle(chat_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        # Supprimer les anciennes questions utilisées
        cursor.execute("""
            DELETE FROM used_questions
            WHERE chat_id = ?
        """, (chat_id,))

        # Augmenter le numéro du cycle
        cursor.execute("""
            UPDATE question_cycles

            SET
                cycle_number = cycle_number + 1,
                started_at = CURRENT_TIMESTAMP

            WHERE chat_id = ?
        """, (chat_id,))

        # Si le groupe n'avait pas encore de cycle
        cursor.execute("""
            INSERT OR IGNORE INTO question_cycles (
                chat_id,
                cycle_number
            )
            VALUES (?, 1)
        """, (chat_id,))

        conn.commit()


def get_cycle_number(chat_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT cycle_number
            FROM question_cycles
            WHERE chat_id = ?
        """, (chat_id,))

        row = cursor.fetchone()

        if not row:
            return 1

        return row["cycle_number"]


# ============================================================
# UTILISATEURS / SCORES
# ============================================================

def ensure_user(
    chat_id,
    user_id,
    username="",
    first_name=""
):

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


# ============================================================
# BONNE RÉPONSE
# ============================================================

def add_correct_answer(
    chat_id,
    user_id,
    username="",
    first_name=""
):

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

                correct_answers =
                    correct_answers + 1,

                streak =
                    streak + 1,

                best_streak =
                    CASE

                        WHEN streak + 1 > best_streak
                        THEN streak + 1

                        ELSE best_streak

                    END

            WHERE chat_id = ?
            AND user_id = ?
        """, (
            chat_id,
            user_id
        ))

        conn.commit()


# ============================================================
# MAUVAISE RÉPONSE
# ============================================================

def add_wrong_answer(
    chat_id,
    user_id,
    username="",
    first_name=""
):

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
                wrong_answers =
                    wrong_answers + 1,

                streak = 0

            WHERE chat_id = ?
            AND user_id = ?
        """, (
            chat_id,
            user_id
        ))

        conn.commit()


# ============================================================
# SCORE D'UN UTILISATEUR
# ============================================================

def get_user_score(chat_id, user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM scores

            WHERE chat_id = ?
            AND user_id = ?
        """, (
            chat_id,
            user_id
        ))

        return cursor.fetchone()


# ============================================================
# CLASSEMENT
# ============================================================

def get_leaderboard(
    chat_id,
    limit=10
):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM scores

            WHERE chat_id = ?

            ORDER BY
                points DESC,
                correct_answers DESC,
                best_streak DESC

            LIMIT ?
        """, (
            chat_id,
            limit
        ))

        return cursor.fetchall()
