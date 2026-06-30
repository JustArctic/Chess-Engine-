import random

# ==========================================================
# Chess Opening Book
# ==========================================================
# Coordinate notation:
# e2e4 = piece moves from e2 to e4
# ==========================================================

OPENINGS = {

    # ======================================================
    # King's Pawn
    # ======================================================

    "Italian Game": [
        "e2e4","e7e5",
        "g1f3","b8c6",
        "f1c4"
    ],

    "Evans Gambit": [
        "e2e4","e7e5",
        "g1f3","b8c6",
        "f1c4","f8c5",
        "b2b4"
    ],

    "Giuoco Piano": [
        "e2e4","e7e5",
        "g1f3","b8c6",
        "f1c4","f8c5",
        "c2c3"
    ],

    "Ruy Lopez": [
        "e2e4","e7e5",
        "g1f3","b8c6",
        "f1b5"
    ],

    "Berlin Defence": [
        "e2e4","e7e5",
        "g1f3","b8c6",
        "f1b5","g8f6"
    ],

    "Morphy Defence": [
        "e2e4","e7e5",
        "g1f3","b8c6",
        "f1b5","a7a6"
    ],

    "Scotch Game": [
        "e2e4","e7e5",
        "g1f3","b8c6",
        "d2d4"
    ],

    "Four Knights": [
        "e2e4","e7e5",
        "g1f3","b8c6",
        "b1c3","g8f6"
    ],

    "Petrov Defence": [
        "e2e4","e7e5",
        "g1f3","g8f6"
    ],

    "Vienna Game": [
        "e2e4","e7e5",
        "b1c3"
    ],

    "King's Gambit": [
        "e2e4","e7e5",
        "f2f4"
    ],

    "Bishop's Opening": [
        "e2e4","e7e5",
        "f1c4"
    ],

    "Center Game": [
        "e2e4","e7e5",
        "d2d4"
    ],

    # ======================================================
    # Sicilian
    # ======================================================

    "Sicilian Defence": [
        "e2e4","c7c5"
    ],

    "Open Sicilian": [
        "e2e4","c7c5",
        "g1f3","d7d6",
        "d2d4"
    ],

    "Najdorf": [
        "e2e4","c7c5",
        "g1f3","d7d6",
        "d2d4","c5d4",
        "f3d4","g8f6",
        "b1c3","a7a6"
    ],

    "Dragon": [
        "e2e4","c7c5",
        "g1f3","d7d6",
        "d2d4","c5d4",
        "f3d4","g8f6",
        "b1c3","g7g6"
    ],

    "Accelerated Dragon": [
        "e2e4","c7c5",
        "g1f3","b8c6",
        "d2d4","c5d4",
        "f3d4","g7g6"
    ],

    "Classical Sicilian": [
        "e2e4","c7c5",
        "g1f3","d7d6",
        "d2d4","c5d4",
        "f3d4","g8f6",
        "b1c3","b8c6"
    ],

    "Scheveningen": [
        "e2e4","c7c5",
        "g1f3","d7d6",
        "d2d4","c5d4",
        "f3d4","e7e6"
    ],

    # ======================================================
    # French
    # ======================================================

    "French Defence": [
        "e2e4","e7e6"
    ],

    "Advance French": [
        "e2e4","e7e6",
        "d2d4","d7d5",
        "e4e5"
    ],

    "Tarrasch French": [
        "e2e4","e7e6",
        "d2d4","d7d5",
        "b1d2"
    ],

    # ======================================================
    # Caro-Kann
    # ======================================================

    "Caro-Kann": [
        "e2e4","c7c6"
    ],

    "Advance Caro-Kann": [
        "e2e4","c7c6",
        "d2d4","d7d5",
        "e4e5"
    ],

    # ======================================================
    # Scandinavian
    # ======================================================

    "Scandinavian": [
        "e2e4","d7d5"
    ],

    # ======================================================
    # Alekhine
    # ======================================================

    "Alekhine Defence": [
        "e2e4","g8f6"
    ],

    # ======================================================
    # Pirc
    # ======================================================

    "Pirc Defence": [
        "e2e4","d7d6",
        "d2d4","g8f6"
    ],

    # ======================================================
    # Queen Pawn
    # ======================================================

    "Queen's Gambit": [
        "d2d4","d7d5",
        "c2c4"
    ],

    "Queen's Gambit Declined": [
        "d2d4","d7d5",
        "c2c4","e7e6"
    ],

    "Queen's Gambit Accepted": [
        "d2d4","d7d5",
        "c2c4","d5c4"
    ],

    "Slav Defence": [
        "d2d4","d7d5",
        "c2c4","c7c6"
    ],

    "Semi-Slav": [
        "d2d4","d7d5",
        "c2c4","e7e6",
        "g1f3","c7c6"
    ],

    "London System": [
        "d2d4","d7d5",
        "c1f4"
    ],

    "Colle System": [
        "d2d4","d7d5",
        "g1f3","g8f6",
        "e2e3"
    ],

    "Torre Attack": [
        "d2d4","g8f6",
        "c1g5"
    ],

    # ======================================================
    # Indian Defences
    # ======================================================

    "King's Indian": [
        "d2d4","g8f6",
        "c2c4","g7g6"
    ],

    "Grunfeld": [
        "d2d4","g8f6",
        "c2c4","g7g6",
        "b1c3","d7d5"
    ],

    "Nimzo-Indian": [
        "d2d4","g8f6",
        "c2c4","e7e6",
        "b1c3","f8b4"
    ],

    "Queen's Indian": [
        "d2d4","g8f6",
        "c2c4","e7e6",
        "g1f3","b7b6"
    ],

    "Bogo-Indian": [
        "d2d4","g8f6",
        "c2c4","e7e6",
        "g1f3","f8b4"
    ],

    "Benoni": [
        "d2d4","g8f6",
        "c2c4","c7c5"
    ],

    "Benko Gambit": [
        "d2d4","g8f6",
        "c2c4","c7c5",
        "d4d5","b7b5"
    ],

    "Dutch Defence": [
        "d2d4","f7f5"
    ],

    # ======================================================
    # Flank Openings
    # ======================================================

    "English Opening": [
        "c2c4"
    ],

    "English Symmetrical": [
        "c2c4","c7c5"
    ],

    "Reti Opening": [
        "g1f3"
    ],

    "Bird Opening": [
        "f2f4"
    ],

    "Larsen Opening": [
        "b2b3"
    ],

    "Polish Opening": [
        "b2b4"
    ],

    "Sokolsky": [
        "b2b4"
    ],

    "King's Fianchetto": [
        "g2g3"
    ],

    "Hungarian Opening": [
        "g2g3","d7d5"
    ],

    "Van't Kruijs Opening": [
        "e2e3"
    ],

    "Anderssen Opening": [
        "a2a3"
    ],

    "Ware Opening": [
        "a2a4"
    ]
}

# ==========================================================
# Returns one random opening
# ==========================================================

def get_random_opening():
    name = random.choice(list(OPENINGS.keys()))
    return name, OPENINGS[name]