import random


# ============================================================
# QUESTIONS DASHQUIZ
# ============================================================
#
# Structure :
#
# {
#     "anime": "Naruto",
#     "difficulty": "easy",
#     "languages": {
#         "fr": {
#             "question": "...",
#             "options": ["...", "...", "...", "..."],
#             "answer": 0
#         },
#         "en": {
#             "question": "...",
#             "options": ["...", "...", "...", "..."],
#             "answer": 0
#         }
#     }
# }
#
# answer = position de la bonne réponse
# 0 = première réponse
# 1 = deuxième réponse
# 2 = troisième réponse
# 3 = quatrième réponse


QUESTIONS = [

    # ========================================================
    # NARUTO
    # ========================================================

    {
        "anime": "Naruto",
        "difficulty": "easy",

        "languages": {

            "fr": {
                "question": "Comment s'appelle le démon renard à neuf queues de Naruto ?",
                "options": [
                    "Kurama",
                    "Shukaku",
                    "Gyuki",
                    "Matatabi"
                ],
                "answer": 0
            },

            "en": {
                "question": "What is the name of Naruto's Nine-Tailed Fox?",
                "options": [
                    "Kurama",
                    "Shukaku",
                    "Gyuki",
                    "Matatabi"
                ],
                "answer": 0
            },

            "es": {
                "question": "¿Cómo se llama el zorro de nueve colas de Naruto?",
                "options": [
                    "Kurama",
                    "Shukaku",
                    "Gyuki",
                    "Matatabi"
                ],
                "answer": 0
            },

            "pt": {
                "question": "Qual é o nome da Raposa de Nove Caudas de Naruto?",
                "options": [
                    "Kurama",
                    "Shukaku",
                    "Gyuki",
                    "Matatabi"
                ],
                "answer": 0
            }
        }
    },


    # ========================================================
    # ONE PIECE
    # ========================================================

    {
        "anime": "One Piece",
        "difficulty": "easy",

        "languages": {

            "fr": {
                "question": "Quel est le rêve de Monkey D. Luffy ?",
                "options": [
                    "Devenir le Roi des Pirates",
                    "Devenir Amiral",
                    "Devenir Shichibukai",
                    "Devenir Marine"
                ],
                "answer": 0
            },

            "en": {
                "question": "What is Monkey D. Luffy's dream?",
                "options": [
                    "Become the Pirate King",
                    "Become an Admiral",
                    "Become a Warlord",
                    "Become a Marine"
                ],
                "answer": 0
            },

            "es": {
                "question": "¿Cuál es el sueño de Monkey D. Luffy?",
                "options": [
                    "Convertirse en el Rey de los Piratas",
                    "Convertirse en Almirante",
                    "Convertirse en Shichibukai",
                    "Convertirse en Marine"
                ],
                "answer": 0
            },

            "pt": {
                "question": "Qual é o sonho de Monkey D. Luffy?",
                "options": [
                    "Tornar-se o Rei dos Piratas",
                    "Tornar-se Almirante",
                    "Tornar-se Shichibukai",
                    "Tornar-se Marinheiro"
                ],
                "answer": 0
            }
        }
    },


    # ========================================================
    # BLEACH
    # ========================================================

    {
        "anime": "Bleach",
        "difficulty": "easy",

        "languages": {

            "fr": {
                "question": "Comment s'appelle le protagoniste principal de Bleach ?",
                "options": [
                    "Ichigo Kurosaki",
                    "Byakuya Kuchiki",
                    "Uryu Ishida",
                    "Renji Abarai"
                ],
                "answer": 0
            },

            "en": {
                "question": "What is the name of Bleach's main protagonist?",
                "options": [
                    "Ichigo Kurosaki",
                    "Byakuya Kuchiki",
                    "Uryu Ishida",
                    "Renji Abarai"
                ],
                "answer": 0
            },

            "es": {
                "question": "¿Cómo se llama el protagonista principal de Bleach?",
                "options": [
                    "Ichigo Kurosaki",
                    "Byakuya Kuchiki",
                    "Uryu Ishida",
                    "Renji Abarai"
                ],
                "answer": 0
            },

            "pt": {
                "question": "Qual é o nome do protagonista principal de Bleach?",
                "options": [
                    "Ichigo Kurosaki",
                    "Byakuya Kuchiki",
                    "Uryu Ishida",
                    "Renji Abarai"
                ],
                "answer": 0
            }
        }
    },


    # ========================================================
    # JUJUTSU KAISEN
    # ========================================================

    {
        "anime": "Jujutsu Kaisen",
        "difficulty": "easy",

        "languages": {

            "fr": {
                "question": "Comment s'appelle le personnage qui devient l'hôte de Sukuna ?",
                "options": [
                    "Yuji Itadori",
                    "Megumi Fushiguro",
                    "Satoru Gojo",
                    "Yuta Okkotsu"
                ],
                "answer": 0
            },

            "en": {
                "question": "Who becomes Sukuna's vessel?",
                "options": [
                    "Yuji Itadori",
                    "Megumi Fushiguro",
                    "Satoru Gojo",
                    "Yuta Okkotsu"
                ],
                "answer": 0
            },

            "es": {
                "question": "¿Quién se convierte en el recipiente de Sukuna?",
                "options": [
                    "Yuji Itadori",
                    "Megumi Fushiguro",
                    "Satoru Gojo",
                    "Yuta Okkotsu"
                ],
                "answer": 0
            },

            "pt": {
                "question": "Quem se torna o receptáculo de Sukuna?",
                "options": [
                    "Yuji Itadori",
                    "Megumi Fushiguro",
                    "Satoru Gojo",
                    "Yuta Okkotsu"
                ],
                "answer": 0
            }
        }
    },


    # ========================================================
    # DEMON SLAYER
    # ========================================================

    {
        "anime": "Demon Slayer",
        "difficulty": "easy",

        "languages": {

            "fr": {
                "question": "Comment s'appelle la sœur de Tanjiro ?",
                "options": [
                    "Nezuko",
                    "Shinobu",
                    "Mitsuri",
                    "Kanao"
                ],
                "answer": 0
            },

            "en": {
                "question": "What is Tanjiro's sister's name?",
                "options": [
                    "Nezuko",
                    "Shinobu",
                    "Mitsuri",
                    "Kanao"
                ],
                "answer": 0
            },

            "es": {
                "question": "¿Cómo se llama la hermana de Tanjiro?",
                "options": [
                    "Nezuko",
                    "Shinobu",
                    "Mitsuri",
                    "Kanao"
                ],
                "answer": 0
            },

            "pt": {
                "question": "Qual é o nome da irmã de Tanjiro?",
                "options": [
                    "Nezuko",
                    "Shinobu",
                    "Mitsuri",
                    "Kanao"
                ],
                "answer": 0
            }
        }
    },


    # ========================================================
    # DRAGON BALL
    # ========================================================

    {
        "anime": "Dragon Ball",
        "difficulty": "easy",

        "languages": {

            "fr": {
                "question": "Comment s'appelle le personnage principal de Dragon Ball ?",
                "options": [
                    "Son Goku",
                    "Vegeta",
                    "Gohan",
                    "Piccolo"
                ],
                "answer": 0
            },

            "en": {
                "question": "What is the name of Dragon Ball's main character?",
                "options": [
                    "Son Goku",
                    "Vegeta",
                    "Gohan",
                    "Piccolo"
                ],
                "answer": 0
            },

            "es": {
                "question": "¿Cómo se llama el protagonista principal de Dragon Ball?",
                "options": [
                    "Son Goku",
                    "Vegeta",
                    "Gohan",
                    "Piccolo"
                ],
                "answer": 0
            },

            "pt": {
                "question": "Qual é o nome do protagonista principal de Dragon Ball?",
                "options": [
                    "Son Goku",
                    "Vegeta",
                    "Gohan",
                    "Piccolo"
                ],
                "answer": 0
            }
        }
    },


    # ========================================================
    # SOLO LEVELING
    # ========================================================

    {
        "anime": "Solo Leveling",
        "difficulty": "easy",

        "languages": {

            "fr": {
                "question": "Comment s'appelle le protagoniste de Solo Leveling ?",
                "options": [
                    "Sung Jin-Woo",
                    "Thomas Andre",
                    "Beru",
                    "Igris"
                ],
                "answer": 0
            },

            "en": {
                "question": "What is the name of Solo Leveling's protagonist?",
                "options": [
                    "Sung Jin-Woo",
                    "Thomas Andre",
                    "Beru",
                    "Igris"
                ],
                "answer": 0
            },

            "es": {
                "question": "¿Cómo se llama el protagonista de Solo Leveling?",
                "options": [
                    "Sung Jin-Woo",
                    "Thomas Andre",
                    "Beru",
                    "Igris"
                ],
                "answer": 0
            },

            "pt": {
                "question": "Qual é o nome do protagonista de Solo Leveling?",
                "options": [
                    "Sung Jin-Woo",
                    "Thomas Andre",
                    "Beru",
                    "Igris"
                ],
                "answer": 0
            }
        }
    },


    # ========================================================
    # ATTACK ON TITAN
    # ========================================================

    {
        "anime": "Attack on Titan",
        "difficulty": "easy",

        "languages": {

            "fr": {
                "question": "Comment s'appelle le protagoniste principal de Attack on Titan ?",
                "options": [
                    "Eren Yeager",
                    "Armin Arlert",
                    "Levi Ackerman",
                    "Reiner Braun"
                ],
                "answer": 0
            },

            "en": {
                "question": "What is the name of Attack on Titan's main protagonist?",
                "options": [
                    "Eren Yeager",
                    "Armin Arlert",
                    "Levi Ackerman",
                    "Reiner Braun"
                ],
                "answer": 0
            },

            "es": {
                "question": "¿Cómo se llama el protagonista principal de Attack on Titan?",
                "options": [
                    "Eren Yeager",
                    "Armin Arlert",
                    "Levi Ackerman",
                    "Reiner Braun"
                ],
                "answer": 0
            },

            "pt": {
                "question": "Qual é o nome do protagonista principal de Attack on Titan?",
                "options": [
                    "Eren Yeager",
                    "Armin Arlert",
                    "Levi Ackerman",
                    "Reiner Braun"
                ],
                "answer": 0
            }
        }
    }
]


# ============================================================
# LANGUES DISPONIBLES
# ============================================================

LANGUAGES = {
    "fr": "🇫🇷 Français",
    "en": "🇬🇧 English",
    "es": "🇪🇸 Español",
    "pt": "🇵🇹 Português",
    "it": "🇮🇹 Italiano",
    "de": "🇩🇪 Deutsch",
    "ja": "🇯🇵 日本語",
    "ko": "🇰🇷 한국어"
}


# ============================================================
# OBTENIR LES ANIMES
# ============================================================

def get_animes():
    return sorted(
        set(question["anime"] for question in QUESTIONS)
    )


# ============================================================
# OBTENIR UNE QUESTION
# ============================================================

def get_random_question(
    language="fr",
    anime=None,
    difficulty="all"
):
    available = []

    for question in QUESTIONS:

        # Filtre anime
        if anime and question["anime"] != anime:
            continue

        # Filtre difficulté
        if difficulty != "all":
            if question["difficulty"] != difficulty:
                continue

        # Vérification de la langue
        if language not in question["languages"]:
            continue

        available.append(question)

    if not available:
        return None

    selected = random.choice(available)

    data = selected["languages"][language]

    return {
        "anime": selected["anime"],
        "difficulty": selected["difficulty"],
        "question": data["question"],
        "options": data["options"],
        "answer": data["answer"]
    }
