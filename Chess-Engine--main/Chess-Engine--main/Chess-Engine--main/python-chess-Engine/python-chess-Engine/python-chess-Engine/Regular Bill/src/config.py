import pygame
import os

from sound import Sound
from theme import Theme


class Config:

    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------
    # Initialises the game's configuration settings,
    # including:
    # • Available board themes
    # • Default theme
    # • Font used throughout the interface
    # • Sound effects
    # ------------------------------------------------------
    def __init__(self):

        # List containing every available board theme.
        self.themes = []

        # Create and store all built-in themes.
        self._add_themes()

        # Start using the first theme in the list.
        self.idx = 0
        self.theme = self.themes[self.idx]

        # Default font used for labels and messages.
        self.font = pygame.font.SysFont(
            'monospace',
            18,
            bold=True
        )

        # Sound played whenever a normal move occurs.
        self.move_sound = Sound(
            os.path.join('assets/sounds/move.wav')
        )

        # Sound played whenever a piece is captured.
        self.capture_sound = Sound(
            os.path.join('assets/sounds/capture.wav')
        )

    # ------------------------------------------------------
    # Change Theme
    # ------------------------------------------------------
    # Cycles to the next available board theme.
    # Once the final theme is reached, it loops back
    # to the first theme.
    # ------------------------------------------------------
    def change_theme(self):

        # Move to the next theme index.
        self.idx += 1

        # Wrap back to the first theme if necessary.
        self.idx %= len(self.themes)

        # Apply the selected theme.
        self.theme = self.themes[self.idx]

    # ------------------------------------------------------
    # Add Themes
    # ------------------------------------------------------
    # Creates every built-in colour theme available
    # in the chess engine.
    #
    # Each theme contains:
    # • Light square colour
    # • Dark square colour
    # • Highlight colours
    # • Last move colours
    # ------------------------------------------------------
    def _add_themes(self):

        # Classic green chess board.
        green = Theme(
            (234, 235, 200),
            (119, 154, 88),
            (244, 247, 116),
            (172, 195, 51),
            '#C86464',
            '#C84646'
        )

        # Traditional wooden brown board.
        brown = Theme(
            (235, 209, 166),
            (165, 117, 80),
            (245, 234, 100),
            (209, 185, 59),
            '#C86464',
            '#C84646'
        )

        # Modern blue board theme.
        blue = Theme(
            (229, 228, 200),
            (60, 95, 135),
            (123, 187, 227),
            (43, 119, 191),
            '#C86464',
            '#C84646'
        )

        # Dark grey board theme.
        gray = Theme(
            (120, 119, 118),
            (86, 85, 84),
            (99, 126, 143),
            (82, 102, 128),
            '#C86464',
            '#C84646'
        )

        # Store every available theme.
        self.themes = [
            green,
            brown,
            blue,
            gray
        ]
