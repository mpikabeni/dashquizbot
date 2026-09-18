import json
import random
from pathlib import Path


QUESTIONS_FILE = Path(__file__).parent / "questions.json"


LANGUAGES = {
    "fr": "🇫🇷 Français",
    "en": "🇬🇧 English",
    "es": "🇪🇸 Español",
    "pt": "🇵🇹 Português",
    "it": "🇮🇹 Italiano",
    "de": "🇩🇪 Deutsch",
    "ja": "🇯🇵 日本語",
    "ko": "🇰🇷 한국어",
}


def load_questions():
    if not QUESTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Le fichier {QUESTIONS_FILE} est introuvable."
        )

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "questions.json doit contenir une liste de questions."
        )

    return data


QUESTIONS = load_questions()


def get_animes():
    return sorted({
        question.get("anime", "Inconnu")
        for question in QUESTIONS
    })


def get_question_count():
    return len(QUESTIONS)


def get_available_questions(
    used_question_ids=None,
    language="fr",
    anime=None,
    difficulty="all"
):
    used_question_ids = used_question_ids or set()

    available = []

    for question in QUESTIONS:

        question_id = question.get("id")

        if not question_id:
            continue

        if question_id in used_question_ids:
            continue

        if anime and question.get("anime") != anime:
            continue

        if (
            difficulty != "all"
            and question.get("difficulty") != difficulty
        ):
            continue

        translations = question.get("translations", {})

        if language not in translations:
            continue

        available.append(question)

    return available


def get_random_question(
    used_question_ids=None,
    language="fr",
    anime=None,
    difficulty="all"
):
    available = get_available_questions(
        used_question_ids=used_question_ids,
        language=language,
        anime=anime,
        difficulty=difficulty
    )

    if not available:
        return None

    selected = random.choice(available)

    translation = selected["translations"][language]

    return {
        "id": selected["id"],
        "anime": selected["anime"],
        "difficulty": selected.get(
            "difficulty",
            "all"
        ),
        "question": translation["question"],
        "options": translation["options"],
        "answer": translation["answer"],
    }
