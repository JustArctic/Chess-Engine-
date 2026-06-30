class Color:

    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------
    # Creates a colour theme consisting of a light colour
    # and a dark colour.
    #
    # Parameters:
    # light - RGB value for the light colour.
    # dark  - RGB value for the dark colour.
    #
    # Used throughout the game to define:
    # • Chess board colours
    # • Highlight colours
    # • Theme colour combinations
    # ------------------------------------------------------
    def __init__(self, light, dark):

        # Store the light colour.
        self.light = light

        # Store the dark colour.
        self.dark = dark
