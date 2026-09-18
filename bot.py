import time
import uuid


# ============================================================
# QUIZ ACTIFS
# ============================================================

active_quizzes = {}


# ============================================================
# CRÉER UN QUIZ
# ============================================================

def create_quiz(chat_id, question_data, duration=60):
    """
    Crée un quiz actif.

    Un quiz possède un ID unique afin que chaque bouton
    de réponse puisse être relié au bon quiz.
    """

    quiz_id = str(uuid.uuid4())

    quiz = {
        "id": quiz_id,
        "chat_id": chat_id,

        "question_id": question_data["id"],

        "anime": question_data["anime"],
        "difficulty": question_data["difficulty"],

        "question": question_data["question"],
        "options": question_data["options"],
        "answer": question_data["answer"],

        "duration": duration,
        "created_at": time.time(),

        # Utilisateurs ayant déjà répondu
        "answered_users": set(),

        # Nombre de bonnes réponses
        "correct_count": 0,

        # Nombre de mauvaises réponses
        "wrong_count": 0,
    }

    active_quizzes[quiz_id] = quiz

    return quiz


# ============================================================
# RÉCUPÉRER UN QUIZ
# ============================================================

def get_quiz(quiz_id):
    return active_quizzes.get(quiz_id)


# ============================================================
# TEMPS RESTANT
# ============================================================

def get_remaining_time(quiz_id):

    quiz = get_quiz(quiz_id)

    if not quiz:
        return 0

    elapsed = time.time() - quiz["created_at"]

    remaining = quiz["duration"] - elapsed

    return max(0, int(remaining))


# ============================================================
# QUIZ EXPIRÉ ?
# ============================================================

def is_expired(quiz_id):

    quiz = get_quiz(quiz_id)

    if not quiz:
        return True

    elapsed = time.time() - quiz["created_at"]

    return elapsed >= quiz["duration"]


# ============================================================
# UTILISATEUR A DÉJÀ RÉPONDU ?
# ============================================================

def has_answered(quiz_id, user_id):

    quiz = get_quiz(quiz_id)

    if not quiz:
        return False

    return user_id in quiz["answered_users"]


# ============================================================
# RÉPONDRE AU QUIZ
# ============================================================

def answer_quiz(
    quiz_id,
    user_id,
    selected_answer
):

    quiz = get_quiz(quiz_id)

    # --------------------------------------------------------
    # Quiz inexistant
    # --------------------------------------------------------

    if not quiz:

        return {
            "success": False,
            "reason": "not_found"
        }

    # --------------------------------------------------------
    # Quiz terminé
    # --------------------------------------------------------

    if is_expired(quiz_id):

        return {
            "success": False,
            "reason": "expired"
        }

    # --------------------------------------------------------
    # Déjà répondu
    # --------------------------------------------------------

    if user_id in quiz["answered_users"]:

        return {
            "success": False,
            "reason": "already_answered"
        }

    # --------------------------------------------------------
    # Enregistrer l'utilisateur
    # --------------------------------------------------------

    quiz["answered_users"].add(user_id)

    # --------------------------------------------------------
    # Vérifier la réponse
    # --------------------------------------------------------

    correct = (
        selected_answer == quiz["answer"]
    )

    if correct:

        quiz["correct_count"] += 1

    else:

        quiz["wrong_count"] += 1

    return {
        "success": True,

        "correct": correct,

        "correct_answer": quiz["answer"],

        "selected_answer": selected_answer,

        "question_id": quiz["question_id"],

        "anime": quiz["anime"],
    }


# ============================================================
# SUPPRIMER UN QUIZ
# ============================================================

def delete_quiz(quiz_id):

    active_quizzes.pop(
        quiz_id,
        None
    )


# ============================================================
# NETTOYER LES QUIZ EXPIRÉS
# ============================================================

def cleanup_quizzes():

    expired_ids = []

    for quiz_id in list(active_quizzes.keys()):

        if is_expired(quiz_id):

            expired_ids.append(quiz_id)

    for quiz_id in expired_ids:

        delete_quiz(quiz_id)


# ============================================================
# LETTRES DES RÉPONSES
# ============================================================

ANSWER_LABELS = [
    "A",
    "B",
    "C",
    "D"
]


def get_option_label(index):

    if 0 <= index < len(ANSWER_LABELS):

        return ANSWER_LABELS[index]

    return "?"


# ============================================================
# FORMATAGE DES OPTIONS
# ============================================================

def format_option(index, option):

    label = get_option_label(index)

    return f"{label}. {option}"


# ============================================================
# TEXTE DU QUIZ
# ============================================================

def format_quiz_text(
    quiz,
    language="fr"
):

    anime = quiz["anime"]
    difficulty = quiz["difficulty"]
    question = quiz["question"]
    duration = quiz["duration"]

    # --------------------------------------------------------
    # FRANÇAIS
    # --------------------------------------------------------

    if language == "fr":

        return (
            "🎌 <b>DASHQUIZ</b>\n\n"

            f"📺 <b>{anime}</b>\n"
            f"🎯 Difficulté : <b>{difficulty}</b>\n\n"

            f"❓ <b>{question}</b>\n\n"

            f"⏱️ Vous avez <b>{duration} secondes</b>."
        )

    # --------------------------------------------------------
    # ENGLISH
    # --------------------------------------------------------

    if language == "en":

        return (
            "🎌 <b>DASHQUIZ</b>\n\n"

            f"📺 <b>{anime}</b>\n"
            f"🎯 Difficulty: <b>{difficulty}</b>\n\n"

            f"❓ <b>{question}</b>\n\n"

            f"⏱️ You have <b>{duration} seconds</b>."
        )

    # --------------------------------------------------------
    # ESPAÑOL
    # --------------------------------------------------------

    if language == "es":

        return (
            "🎌 <b>DASHQUIZ</b>\n\n"

            f"📺 <b>{anime}</b>\n"
            f"🎯 Dificultad: <b>{difficulty}</b>\n\n"

            f"❓ <b>{question}</b>\n\n"

            f"⏱️ Tienes <b>{duration} segundos</b>."
        )

    # --------------------------------------------------------
    # PORTUGUÊS
    # --------------------------------------------------------

    if language == "pt":

        return (
            "🎌 <b>DASHQUIZ</b>\n\n"

            f"📺 <b>{anime}</b>\n"
            f"🎯 Dificuldade: <b>{difficulty}</b>\n\n"

            f"❓ <b>{question}</b>\n\n"

            f"⏱️ Você tem <b>{duration} segundos</b>."
        )

    # --------------------------------------------------------
    # ITALIANO
    # --------------------------------------------------------

    if language == "it":

        return (
            "🎌 <b>DASHQUIZ</b>\n\n"

            f"📺 <b>{anime}</b>\n"
            f"🎯 Difficoltà: <b>{difficulty}</b>\n\n"

            f"❓ <b>{question}</b>\n\n"

            f"⏱️ Hai <b>{duration} secondi</b>."
        )

    # --------------------------------------------------------
    # DEUTSCH
    # --------------------------------------------------------

    if language == "de":

        return (
            "🎌 <b>DASHQUIZ</b>\n\n"

            f"📺 <b>{anime}</b>\n"
            f"🎯 Schwierigkeit: <b>{difficulty}</b>\n\n"

            f"❓ <b>{question}</b>\n\n"

            f"⏱️ Du hast <b>{duration} Sekunden</b>."
        )

    # --------------------------------------------------------
    # JAPONAIS
    # --------------------------------------------------------

    if language == "ja":

        return (
            "🎌 <b>DASHQUIZ</b>\n\n"

            f"📺 <b>{anime}</b>\n"
            f"🎯 難易度: <b>{difficulty}</b>\n\n"

            f"❓ <b>{question}</b>\n\n"

            f"⏱️ 制限時間: <b>{duration}秒</b>"
        )

    # --------------------------------------------------------
    # CORÉEN
    # --------------------------------------------------------

    if language == "ko":

        return (
            "🎌 <b>DASHQUIZ</b>\n\n"

            f"📺 <b>{anime}</b>\n"
            f"🎯 난이도: <b>{difficulty}</b>\n\n"

            f"❓ <b>{question}</b>\n\n"

            f"⏱️ 제한 시간: <b>{duration}초</b>"
        )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return (
        "🎌 <b>DASHQUIZ</b>\n\n"

        f"📺 <b>{anime}</b>\n\n"

        f"❓ <b>{question}</b>\n\n"

        f"⏱️ {duration} seconds"
    )


# ============================================================
# RÉSULTAT FINAL
# ============================================================

def format_result_text(
    quiz,
    language="fr"
):

    correct_index = quiz["answer"]

    correct_option = quiz["options"][correct_index]

    correct_count = quiz["correct_count"]
    wrong_count = quiz["wrong_count"]

    # --------------------------------------------------------
    # FRANÇAIS
    # --------------------------------------------------------

    if language == "fr":

        return (
            "⏰ <b>QUIZ TERMINÉ !</b>\n\n"

            f"📺 Anime : <b>{quiz['anime']}</b>\n\n"

            f"✅ Bonne réponse : "
            f"<b>{correct_option}</b>\n\n"

            f"👥 Bonnes réponses : <b>{correct_count}</b>\n"
            f"❌ Mauvaises réponses : <b>{wrong_count}</b>"
        )

    # --------------------------------------------------------
    # ENGLISH
    # --------------------------------------------------------

    if language == "en":

        return (
            "⏰ <b>QUIZ FINISHED!</b>\n\n"

            f"📺 Anime: <b>{quiz['anime']}</b>\n\n"

            f"✅ Correct answer: "
            f"<b>{correct_option}</b>\n\n"

            f"👥 Correct answers: <b>{correct_count}</b>\n"
            f"❌ Wrong answers: <b>{wrong_count}</b>"
        )

    # --------------------------------------------------------
    # ESPAÑOL
    # --------------------------------------------------------

    if language == "es":

        return (
            "⏰ <b>¡QUIZ TERMINADO!</b>\n\n"

            f"📺 Anime: <b>{quiz['anime']}</b>\n\n"

            f"✅ Respuesta correcta: "
            f"<b>{correct_option}</b>\n\n"

            f"👥 Respuestas correctas: <b>{correct_count}</b>\n"
            f"❌ Respuestas incorrectas: <b>{wrong_count}</b>"
        )

    # --------------------------------------------------------
    # PORTUGUÊS
    # --------------------------------------------------------

    if language == "pt":

        return (
            "⏰ <b>QUIZ TERMINADO!</b>\n\n"

            f"📺 Anime: <b>{quiz['anime']}</b>\n\n"

            f"✅ Resposta correta: "
            f"<b>{correct_option}</b>\n\n"

            f"👥 Respostas corretas: <b>{correct_count}</b>\n"
            f"❌ Respostas erradas: <b>{wrong_count}</b>"
        )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return (
        "⏰ <b>QUIZ FINISHED!</b>\n\n"

        f"📺 <b>{quiz['anime']}</b>\n\n"

        f"✅ <b>{correct_option}</b>"
    )
