import os

class Piece:
    """
    Base class for every chess piece.

    Stores common information such as:
    - Piece name
    - Colour
    - Material value
    - Legal moves
    - Whether the piece has moved
    - Image texture
    """

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        # Name of the piece (pawn, knight, bishop, etc.)
        self.name = name

        # Piece colour ("white" or "black")
        self.color = color

        # Give white positive values and black negative values
        # This helps the AI evaluation function.
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign

        # List containing every legal move available
        self.moves = []

        # Tracks whether the piece has moved before
        # Used for castling and pawn double moves.
        self.moved = False

        # Image information
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        """
        Sets the image path for the piece.

        Different image sizes are used while dragging pieces.
        """

        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
        )

    def add_move(self, move):
        """
        Adds a legal move to the piece's move list.
        """

        self.moves.append(move)

    def clear_moves(self):
        """
        Removes all previously generated moves.

        Called before recalculating legal moves.
        """

        self.moves = []


class Pawn(Piece):
    """
    Pawn piece.

    Includes:
    - Movement direction
    - En passant availability
    """

    def __init__(self, color):

        # White pawns move upwards, black pawns move downwards
        self.dir = -1 if color == 'white' else 1

        # True only immediately after moving two squares
        self.en_passant = False

        super().__init__('pawn', color, 1.0)


class Knight(Piece):
    """
    Knight piece.
    """

    def __init__(self, color):
        super().__init__('knight', color, 3.0)


class Bishop(Piece):
    """
    Bishop piece.
    """

    def __init__(self, color):

        # Slightly higher value than a knight
        self.value_bonus = 0.001

        super().__init__('bishop', color, 3.001)


class Rook(Piece):
    """
    Rook piece.
    """

    def __init__(self, color):
        super().__init__('rook', color, 5.0)


class Queen(Piece):
    """
    Queen piece.
    """

    def __init__(self, color):
        super().__init__('queen', color, 9.0)


class King(Piece):
    """
    King piece.

    Stores references to the left and right rooks
    during castling.
    """

    def __init__(self, color):

        # Rooks involved in castling
        self.left_rook = None
        self.right_rook = None

        # Extremely high value because losing the king
        # effectively ends the game.
        super().__init__('king', color, 10000.0)
