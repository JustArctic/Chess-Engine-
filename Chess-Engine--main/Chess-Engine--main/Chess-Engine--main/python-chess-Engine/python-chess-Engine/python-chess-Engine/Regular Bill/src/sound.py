import pygame

class Sound:
    """
    Handles loading and playing sound effects.

    Used throughout the game for actions such as:
    - Moving a piece
    - Capturing a piece
    """

    def __init__(self, path):
        """
        Loads a sound file from the specified path.

        Args:
            path (str): File path to the sound effect.
        """

        # Store the sound file path
        self.path = path

        # Load the sound into memory
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        """
        Plays the loaded sound effect once.
        """

        pygame.mixer.Sound.play(self.sound)
