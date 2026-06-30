import random

# ---------------------------------------------------------
# Opening Book
# ---------------------------------------------------------
# Stores a collection of common chess openings.
# Each opening is represented using coordinate notation:
#
# e2e4 = Move the piece from e2 to e4
#
# The AI can randomly choose one of these openings at
# the start of the game to create more natural play.
# ---------------------------------------------------------

OPENINGS = {

    # King's Pawn Openings
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

    "Scotch Game": [
        "e2e4", "e7e5",
        "g1f3", "b8c6",
        "d2d4"
    ],

    "Four Knights Game": [
        "e2e4", "e7e5",
        "g1f3", "b8c6",
        "b1c3", "g8f6"
    ],

    "Petrov Defence": [
        "e2e4", "e7e5",
        "g1f3", "g8f6"
    ],

    "Vienna Game": [
        "e2e4", "e7e5",
        "b1c3"
    ],

    "King's Gambit": [
        "e2e4", "e7e5",
        "f2f4"
    ],

    # Sicilian Variations
    "Sicilian Defence": [
        "e2e4", "c7c5"
    ],

    "Sicilian Najdorf": [
        "e2e4", "c7c5",
        "g1f3", "d7d6",
        "d2d4", "c5d4",
        "f3d4", "g8f6",
        "b1c3", "a7a6"
    ],

    "Sicilian Dragon": [
        "e2e4", "c7c5",
        "g1f3", "d7d6",
        "d2d4", "c5d4",
        "f3d4", "g8f6",
        "b1c3", "g7g6"
    ],

    # Queen's Pawn Openings
    "Queen's Gambit": [
        "d2d4", "d7d5",
        "c2c4"
    ],

    "Queen's Gambit Declined": [
        "d2d4", "d7d5",
        "c2c4", "e7e6"
    ],

    "Slav Defence": [
        "d2d4", "d7d5",
        "c2c4", "c7c6"
    ],

    "London System": [
        "d2d4", "d7d5",
        "c1f4"
    ],

    "Colle System": [
        "d2d4", "d7d5",
        "g1f3", "g8f6",
        "e2e3"
    ],

    # Indian Defences
    "King's Indian Defence": [
        "d2d4", "g8f6",
        "c2c4", "g7g6"
    ],

    "Nimzo-Indian Defence": [
        "d2d4", "g8f6",
        "c2c4", "e7e6",
        "b1c3", "f8b4"
    ],

    "Grünfeld Defence": [
        "d2d4", "g8f6",
        "c2c4", "g7g6",
        "b1c3", "d7d5"
    ],

    # English Opening
    "English Opening": [
        "c2c4"
    ],

    # Réti Opening
    "Réti Opening": [
        "g1f3"
    ],

    # Bird Opening
    "Bird Opening": [
        "f2f4"
    ]
}


# ---------------------------------------------------------
# Random Opening Selector
# ---------------------------------------------------------
# Randomly chooses one opening from the opening book.
#
# Returns:
#   name (str)   - Name of the opening.
#   moves (list) - List of moves in coordinate notation.
# ---------------------------------------------------------
def get_random_opening():

    # Select a random opening name
    name = random.choice(list(OPENINGS.keys()))

    # Return the opening name and move sequence
    return name, OPENINGS[name]
