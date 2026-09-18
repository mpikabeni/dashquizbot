import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN est introuvable. "
        "Ajoute la variable BOT_TOKEN dans les variables d'environnement."
    )
