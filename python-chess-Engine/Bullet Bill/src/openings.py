import random

OPENINGS = {
    "Italian Game": [
        "e2e4", "e7e5",
        "g1f3", "b8c6",
        "f1c4"
    ],

    "Ruy Lopez": [
        "e2e4", "e7e5",
        "g1f3", "b8c6",
        "f1b5"
    ],

    "Queen's Gambit": [
        "d2d4", "d7d5",
        "c2c4"
    ],

    "London System": [
        "d2d4", "d7d5",
        "c1f4"
    ],

    "Sicilian Defence": [
        "e2e4", "c7c5"
    ]
}

def get_random_opening():
    name = random.choice(list(OPENINGS.keys()))
    return name, OPENINGS[name]