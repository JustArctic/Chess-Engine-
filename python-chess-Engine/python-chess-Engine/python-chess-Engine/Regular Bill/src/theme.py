from color import Color

class Theme:

    # Creates a theme containing all colours used by the chess game.
    # Each theme stores colours for the board, previous move highlights,
    # and legal move highlights.
    def __init__(self,
                 light_bg, dark_bg,
                 light_trace, dark_trace,
                 light_moves, dark_moves):

        # Board square colours
        self.bg = Color(light_bg, dark_bg)

        # Colours used to highlight the previous move made
        self.trace = Color(light_trace, dark_trace)

        # Colours used to highlight all legal moves
        # for the currently selected piece
        self.moves = Color(light_moves, dark_moves)
