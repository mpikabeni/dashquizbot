import os

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")


if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN est introuvable. "
        "Ajoute BOT_TOKEN dans les variables d'environnement."
    )


# ============================================================
# DASHQUIZ
# ============================================================

BOT_NAME = "DashQuiz"

# Un quiz automatique toutes les heures
DEFAULT_INTERVAL_MINUTES = 60

# Durée pendant laquelle les membres peuvent répondre
DEFAULT_QUIZ_DURATION = 60

# Points pour une bonne réponse
POINTS_CORRECT = 10

# Nombre maximum de joueurs affichés dans le classement
LEADERBOARD_LIMIT = 10
