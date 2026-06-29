class Square:

    # Dictionary used to convert column numbers into chess notation.
    # Example: 0 = a, 1 = b, 2 = c, etc.
    ALPHACOLS = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h'
    }

    # Creates a square on the chess board.
    # Each square stores its row, column and any piece occupying it.
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    # Allows two squares to be compared using ==.
    # Squares are equal if they have the same row and column.
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # Returns True if the square currently contains a piece.
    def has_piece(self):
        return self.piece is not None

    # Returns True if the square is empty.
    def isempty(self):
        return not self.has_piece()

    # Returns True if the square contains one of the current player's pieces.
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    # Returns True if the square contains an opponent's piece.
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    # Returns True if the square is either empty or occupied by an enemy piece.
    # Used when generating legal moves.
    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)

    # Checks whether one or more board coordinates are inside the chess board.
    # Returns False if any coordinate is outside the range 0-7.
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True

    # Converts a column number into its chess notation letter.
    # Example: 4 -> "e"
    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h'
        }
        return ALPHACOLS[col]
