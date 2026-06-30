# ==========================================================
# Import required modules and classes
# ==========================================================

# Import global constants such as board dimensions.
from const import *

# Import the Square class used to represent each board square.
from square import Square

# Import all chess piece classes (Pawn, Rook, Knight, etc.).
from piece import *

# Import the Move class used to represent chess moves.
from move import Move

# Import the Sound class for playing move and capture sounds.
from sound import Sound

# Used to create independent copies of the board when checking
# future moves without affecting the real game.
import copy

# Used to build file paths for loading sound files.
import os

# ==========================================================
# Piece-Square Tables
# These tables assign positional bonuses to each piece.
# Positive values encourage the AI to place pieces on
# stronger squares during the game.
# ==========================================================

# Pawn positional bonuses.
# Rewards advancing pawns and controlling the centre.
PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

# Knight positional bonuses.
# Rewards centralised knights and discourages edge positions.
KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,0,0,0,0,-20,-40],
    [-30,0,10,15,15,10,0,-30],
    [-30,5,15,20,20,15,5,-30],
    [-30,0,15,20,20,15,0,-30],
    [-30,5,10,15,15,10,5,-30],
    [-40,-20,0,5,5,0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

# Bishop positional bonuses.
# Encourages bishops to occupy long diagonals.
BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,0,0,0,0,0,0,-10],
    [-10,0,5,10,10,5,0,-10],
    [-10,5,5,10,10,5,5,-10],
    [-10,0,10,10,10,10,0,-10],
    [-10,10,10,10,10,10,10,-10],
    [-10,5,0,0,0,0,5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

# Rook positional bonuses.
# Rewards active rooks and control of open files.
ROOK_TABLE = [
    [0,0,0,5,5,0,0,0],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [-5,0,0,0,0,0,0,-5],
    [5,10,10,10,10,10,10,5],
    [0,0,0,0,0,0,0,0]
]

# Queen positional bonuses.
# Encourages central control while avoiding poor squares.
QUEEN_TABLE = [
    [-20,-10,-10,-5,-5,-10,-10,-20],
    [-10,0,0,0,0,0,0,-10],
    [-10,0,5,5,5,5,0,-10],
    [-5,0,5,5,5,5,0,-5],
    [0,0,5,5,5,5,0,-5],
    [-10,5,5,5,5,5,0,-10],
    [-10,0,5,0,0,0,0,-10],
    [-20,-10,-10,-5,-5,-10,-10,-20]
]

# King positional bonuses.
# Keeps the king protected during the opening and middlegame.
KING_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20,20,0,0,0,0,20,20],
    [20,30,10,0,0,10,30,20]
]

# ==========================================================
# Board Class
# ----------------------------------------------------------
# Represents the entire chess board and controls:
# • Piece movement
# • Legal move validation
# • Special chess rules
# • Check detection
# • Board state updates
# ==========================================================
class Board:
    
    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------
    # Creates an empty chess board before placing all pieces
    # into their starting positions.
    # ------------------------------------------------------
    def __init__(self):

        # Create an 8x8 grid of empty squares.
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        # Stores the most recently played move.
        self.last_move = None

        # Initialise every square on the board.
        self._create()

        # Place White and Black pieces in their starting positions.
        self._add_pieces('white')
        self._add_pieces('black')

        # Store the history of moves for undo functionality.
        self.move_history = []

    # ------------------------------------------------------
    # move()
    # ------------------------------------------------------
    # Executes a chess move by updating the board state.
    #
    # Handles:
    # • Normal moves
    # • Captures
    # • En passant
    # • Promotion
    # • Castling
    # ------------------------------------------------------
    def move(self, piece, move, testing=False):

        # Store the starting and ending squares of the move.
        initial = move.initial
        final = move.final

        # Track whether this move captures an opponent's piece.
        # This is returned so the game can play the correct sound.
        captured = False

        # --------------------------
        # Normal capture detection
        # --------------------------

        # If the destination square already contains a piece,
        # this move is a normal capture.
        if self.squares[final.row][final.col].has_piece():
            captured = True

        # Determine whether an en passant capture may occur.
        # For en passant, the destination square is empty.
        en_passant_empty = self.squares[final.row][final.col].isempty()

        # Remove the moving piece from its original square.
        self.squares[initial.row][initial.col].piece = None

        # Place the moving piece onto its destination square.
        self.squares[final.row][final.col].piece = piece

        # --------------------------
        # Pawn-specific rules
        # --------------------------
        if isinstance(piece, Pawn):

            # Horizontal movement determines whether the pawn
            # is moving diagonally (potential capture).
            diff = final.col - initial.col

            # --------------------------
            # En Passant
            # --------------------------
            if diff != 0 and en_passant_empty:

                # En passant is also a capture.
                captured = True

                # Remove the captured pawn.
                self.squares[initial.row][initial.col + diff].piece = None

                # Ensure the moving pawn occupies its destination.
                self.squares[final.row][final.col].piece = piece

            # --------------------------
            # Promotion
            # --------------------------
            else:
                self.check_promotion(piece, final)

        # --------------------------
        # King-specific rules
        # --------------------------
        if isinstance(piece, King):

            # Automatically move the rook when castling.
            if self.castling(initial, final) and not testing:

                diff = final.col - initial.col

                # Determine which rook is involved.
                rook = (
                    piece.left_rook
                    if diff < 0
                    else piece.right_rook
                )

                # Move the rook without triggering additional logic.
                self.move(rook, rook.moves[-1], testing=True)

        # Mark the piece as having moved.
        piece.moved = True

        # Remove any previously generated legal moves.
        piece.clear_moves()

        # Store this move as the most recent move played.
        self.last_move = move

        # Convert the move into algebraic coordinates
        # for the move history.
        start = chr(initial.col + ord("a")) + str(8 - initial.row)
        end = chr(final.col + ord("a")) + str(8 - final.row)

        # Save the move in the move history.
        self.move_history.append(f"{start}-{end}")

        # Return whether this move captured a piece.
        # Used by the game to play the correct sound effect.
        return captured

    # ------------------------------------------------------
    # valid_move()
    # ------------------------------------------------------
    # Returns True if the selected move exists within the
    # piece's list of legal moves.
    # ------------------------------------------------------
    def valid_move(self, piece, move):
        return move in piece.moves

    # ------------------------------------------------------
    # check_promotion()
    # ------------------------------------------------------
    # Promotes a pawn to a queen once it reaches the final
    # rank.
    # ------------------------------------------------------
    def check_promotion(self, piece, final):

        if final.row == 0 or final.row == 7:

            # Replace the pawn with a queen.
            self.squares[final.row][final.col].piece = Queen(piece.color)

    # ------------------------------------------------------
    # castling()
    # ------------------------------------------------------
    # Determines whether a king move is a castling move.
    # ------------------------------------------------------
    def castling(self, initial, final):

        # A king castles by moving exactly two columns.
        return abs(initial.col - final.col) == 2

    # ------------------------------------------------------
    # set_true_en_passant()
    # ------------------------------------------------------
    # Enables en passant for the pawn that has just moved two
    # squares while disabling it for every other pawn.
    # ------------------------------------------------------
    def set_true_en_passant(self, piece):

        # Only pawns can perform en passant.
        if not isinstance(piece, Pawn):
            return

        # Disable en passant for every pawn.
        for row in range(ROWS):
            for col in range(COLS):

                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False

        # Enable en passant for the selected pawn.
        piece.en_passant = True

    # ------------------------------------------------------
    # in_check()
    # ------------------------------------------------------
    # Simulates a move and determines whether it would leave
    # the player's king in check.
    #
    # Used to prevent illegal moves.
    # ------------------------------------------------------
    def in_check(self, piece, move):

        # Create independent copies of the piece and board.
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)

        # Simulate the move.
        temp_board.move(temp_piece, move, testing=True)

        # Search every enemy piece.
        for row in range(ROWS):
            for col in range(COLS):

                if temp_board.squares[row][col].has_enemy_piece(piece.color):

                    p = temp_board.squares[row][col].piece

                    # Generate all enemy attacks.
                    temp_board.calc_moves(p, row, col, bool=False)

                    # If an enemy can capture the king,
                    # the move is illegal.
                    for m in p.moves:

                        if isinstance(m.final.piece, King):
                            return True

        # King is safe.
        return False

    # ------------------------------------------------------
    # calc_moves()
    # ------------------------------------------------------
    # Calculates every legal move available for a given piece.
    #
    # This function contains the movement logic for every
    # chess piece including:
    #
    # • Pawn
    # • Knight
    # • Bishop
    # • Rook
    # • Queen
    # • King
    #
    # It also checks special rules such as castling,
    # en passant and moves that would leave the king in
    # check.
    # ------------------------------------------------------
    def calc_moves(self, piece, row, col, bool=True):
        """
        Calculate every legal move available for the selected
        piece based on the current board position.
        """
        
        # ------------------------------------------------------
        # pawn_moves()
        # ------------------------------------------------------
        # Calculates every legal move available for a pawn.
        #
        # Includes:
        # • Forward movement
        # • Diagonal captures
        # • En passant
        # • Preventing moves that leave the king in check
        # ------------------------------------------------------
        def pawn_moves():

            # Determine how many squares the pawn can move.
            # A pawn may move two squares only if it has not moved before.
            steps = 1 if piece.moved else 2

            # --------------------------------------------------
            # Forward Movement
            # --------------------------------------------------

            # Calculate the first square directly in front of the pawn.
            start = row + piece.dir

            # Calculate the furthest square the pawn can reach.
            end = row + (piece.dir * (1 + steps))

            # Check every square in front of the pawn.
            for possible_move_row in range(start, end, piece.dir):

                # Ensure the square is still on the board.
                if Square.in_range(possible_move_row):

                    # Pawns may only move forward into empty squares.
                    if self.squares[possible_move_row][col].isempty():

                        # Create the starting square.
                        initial = Square(row, col)

                        # Create the destination square.
                        final = Square(possible_move_row, col)

                        # Create the move object.
                        move = Move(initial, final)

                        # Only allow moves that do not place
                        # the player's king in check.
                        if bool:

                            if not self.in_check(piece, move):
                                piece.add_move(move)

                        else:
                            piece.add_move(move)

                    # Stop searching if another piece blocks the path.
                    else:
                        break

                # Stop if movement would leave the board.
                else:
                    break

            # --------------------------------------------------
            # Diagonal Captures
            # --------------------------------------------------

            # Pawns capture one square diagonally forward.
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]

            # Check both diagonal squares.
            for possible_move_col in possible_move_cols:

                # Ensure the destination is on the board.
                if Square.in_range(possible_move_row, possible_move_col):

                    # Only enemy pieces can be captured.
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):

                        # Starting square.
                        initial = Square(row, col)

                        # Piece being captured.
                        final_piece = self.squares[possible_move_row][possible_move_col].piece

                        # Destination square.
                        final = Square(
                            possible_move_row,
                            possible_move_col,
                            final_piece
                        )

                        # Create capture move.
                        move = Move(initial, final)

                        # Reject moves that expose the king.
                        if bool:

                            if not self.in_check(piece, move):
                                piece.add_move(move)

                        else:
                            piece.add_move(move)

            # --------------------------------------------------
            # En Passant
            # --------------------------------------------------
            # En passant is a special pawn capture that may occur
            # immediately after an opposing pawn moves forward
            # two squares.

            # Required row for en passant.
            r = 3 if piece.color == 'white' else 4

            # Destination row after capturing.
            fr = 2 if piece.color == 'white' else 5

            # --------------------------------------------------
            # Left En Passant
            # --------------------------------------------------

            if Square.in_range(col - 1) and row == r:

                if self.squares[row][col - 1].has_enemy_piece(piece.color):

                    p = self.squares[row][col - 1].piece

                    # Only pawns may be captured via en passant.
                    if isinstance(p, Pawn):

                        # The neighbouring pawn must be marked
                        # as vulnerable to en passant.
                        if p.en_passant:

                            initial = Square(row, col)

                            final = Square(fr, col - 1, p)

                            move = Move(initial, final)

                            if bool:

                                if not self.in_check(piece, move):
                                    piece.add_move(move)

                            else:
                                piece.add_move(move)

            # --------------------------------------------------
            # Right En Passant
            # --------------------------------------------------

            if Square.in_range(col + 1) and row == r:

                if self.squares[row][col + 1].has_enemy_piece(piece.color):

                    p = self.squares[row][col + 1].piece

                    if isinstance(p, Pawn):

                        if p.en_passant:

                            initial = Square(row, col)

                            final = Square(fr, col + 1, p)

                            move = Move(initial, final)

                            if bool:

                                if not self.in_check(piece, move):
                                    piece.add_move(move)

                            else:
                                piece.add_move(move)
                # ------------------------------------------------------
        # knight_moves()
        # ------------------------------------------------------
        # Calculates every legal move available for a knight.
        #
        # Knights move in an "L" shape:
        # • Two squares in one direction
        # • One square perpendicular
        #
        # Knights are the only pieces that can jump over
        # other pieces.
        # ------------------------------------------------------
        def knight_moves():

            # All eight possible knight movement patterns.
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            # Check each possible destination.
            for possible_move in possible_moves:

                possible_move_row, possible_move_col = possible_move

                # Ensure the destination is inside the board.
                if Square.in_range(possible_move_row, possible_move_col):

                    # Knights may move onto an empty square
                    # or capture an opposing piece.
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):

                        # Create the starting square.
                        initial = Square(row, col)

                        # Store any piece occupying the destination.
                        final_piece = self.squares[possible_move_row][possible_move_col].piece

                        # Create the destination square.
                        final = Square(
                            possible_move_row,
                            possible_move_col,
                            final_piece
                        )

                        # Create the move object.
                        move = Move(initial, final)

                        # Reject moves that would leave
                        # the player's king in check.
                        if bool:

                            if not self.in_check(piece, move):
                                piece.add_move(move)

                            else:
                                continue

                        else:
                            piece.add_move(move)

        # ------------------------------------------------------
        # straightline_moves()
        # ------------------------------------------------------
        # Calculates movement for sliding pieces:
        # • Bishop
        # • Rook
        # • Queen
        #
        # These pieces continue moving in one direction
        # until blocked by another piece or the board edge.
        # ------------------------------------------------------
        def straightline_moves(incrs):

            # Check each movement direction.
            for incr in incrs:

                row_incr, col_incr = incr

                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                # Continue moving until blocked.
                while True:

                    # Stop if the position leaves the board.
                    if Square.in_range(possible_move_row, possible_move_col):

                        # Create starting square.
                        initial = Square(row, col)

                        # Store any captured piece.
                        final_piece = self.squares[possible_move_row][possible_move_col].piece

                        # Create destination square.
                        final = Square(
                            possible_move_row,
                            possible_move_col,
                            final_piece
                        )

                        # Create move object.
                        move = Move(initial, final)

                        # -----------------------------
                        # Empty square
                        # -----------------------------
                        # Continue travelling further.
                        if self.squares[possible_move_row][possible_move_col].isempty():

                            if bool:

                                if not self.in_check(piece, move):
                                    piece.add_move(move)

                            else:
                                piece.add_move(move)

                        # -----------------------------
                        # Enemy piece
                        # -----------------------------
                        # Capture then stop.
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):

                            if bool:

                                if not self.in_check(piece, move):
                                    piece.add_move(move)

                            else:
                                piece.add_move(move)

                            break

                        # -----------------------------
                        # Friendly piece
                        # -----------------------------
                        # Movement is blocked.
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # Reached board edge.
                    else:
                        break

                    # Continue travelling in the same direction.
                    possible_move_row += row_incr
                    possible_move_col += col_incr

        # ------------------------------------------------------
        # king_moves()
        # ------------------------------------------------------
        # Calculates every legal king move.
        #
        # Includes:
        # • Normal one-square movement
        # • Kingside castling
        # • Queenside castling
        # • Check prevention
        # ------------------------------------------------------
        def king_moves():

            # All adjacent squares around the king.
            adjs = [
                (row-1, col+0),   # Up
                (row-1, col+1),   # Up-right
                (row+0, col+1),   # Right
                (row+1, col+1),   # Down-right
                (row+1, col+0),   # Down
                (row+1, col-1),   # Down-left
                (row+0, col-1),   # Left
                (row-1, col-1),   # Up-left
            ]

            # --------------------------------------------------
            # Normal king movement
            # --------------------------------------------------

            for possible_move in adjs:

                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):

                    # Kings may move to empty squares
                    # or capture enemy pieces.
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):

                        initial = Square(row, col)

                        final_piece = self.squares[possible_move_row][possible_move_col].piece

                        final = Square(
                            possible_move_row,
                            possible_move_col,
                            final_piece
                        )

                        move = Move(initial, final)

                        # Reject illegal moves that leave
                        # the king in check.
                        if bool:

                            if not self.in_check(piece, move):
                                piece.add_move(move)

                            else:
                                continue

                        else:
                            piece.add_move(move)

            # --------------------------------------------------
            # Castling
            # --------------------------------------------------
            # Castling is only allowed if:
            # • The king has not moved.
            # • The rook has not moved.
            # • Squares between them are empty.
            # • Neither piece passes through check.
            # --------------------------------------------------

            if not piece.moved:

                # ==========================
                # Queenside Castling
                # ==========================

                left_rook = self.squares[row][0].piece

                if isinstance(left_rook, Rook):

                    if not left_rook.moved:

                        for c in range(1, 4):

                            # A piece blocks castling.
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:

                                # Link the rook to the king.
                                piece.left_rook = left_rook

                                # Rook move.
                                moveR = Move(
                                    Square(row, 0),
                                    Square(row, 3)
                                )

                                # King move.
                                moveK = Move(
                                    Square(row, col),
                                    Square(row, 2)
                                )

                                if bool:

                                    if (
                                        not self.in_check(piece, moveK)
                                        and not self.in_check(left_rook, moveR)
                                    ):

                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)

                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)

                # ==========================
                # Kingside Castling
                # ==========================

                right_rook = self.squares[row][7].piece

                if isinstance(right_rook, Rook):

                    if not right_rook.moved:

                        for c in range(5, 7):

                            # A piece blocks castling.
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:

                                # Link the rook to the king.
                                piece.right_rook = right_rook

                                # Rook move.
                                moveR = Move(
                                    Square(row, 7),
                                    Square(row, 5)
                                )

                                # King move.
                                moveK = Move(
                                    Square(row, col),
                                    Square(row, 6)
                                )

                                if bool:

                                    if (
                                        not self.in_check(piece, moveK)
                                        and not self.in_check(right_rook, moveR)
                                    ):

                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)

                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)

                # ------------------------------------------------------
        # Select Move Generation Function
        # ------------------------------------------------------
        # Determine the type of chess piece and call the
        # appropriate function to calculate all legal moves.
        # ------------------------------------------------------

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):

            # Bishops move diagonally in all four directions.
            straightline_moves([
                (-1, 1),   # Up-right
                (-1, -1),  # Up-left
                (1, 1),    # Down-right
                (1, -1),   # Down-left
            ])

        elif isinstance(piece, Rook):

            # Rooks move horizontally and vertically.
            straightline_moves([
                (-1, 0),   # Up
                (0, 1),    # Right
                (1, 0),    # Down
                (0, -1),   # Left
            ])

        elif isinstance(piece, Queen):

            # Queens combine the movement of both
            # the rook and bishop.
            straightline_moves([
                (-1, 1),   # Up-right
                (-1, -1),  # Up-left
                (1, 1),    # Down-right
                (1, -1),   # Down-left
                (-1, 0),   # Up
                (0, 1),    # Right
                (1, 0),    # Down
                (0, -1)    # Left
            ])

        elif isinstance(piece, King):
            king_moves()

    # Import the King class for type checking.
    from piece import King

    # ------------------------------------------------------
    # find_king()
    # ------------------------------------------------------
    # Searches the board to locate the king belonging to
    # the specified colour.
    #
    # Returns:
    # • King object
    # • Row position
    # • Column position
    #
    # Returns (None, None, None) if no king is found.
    # ------------------------------------------------------
    def find_king(self, color):

        for row in range(8):
            for col in range(8):

                square = self.squares[row][col]

                if square.has_piece():

                    piece = square.piece

                    if isinstance(piece, King) and piece.color == color:
                        return piece, row, col

        return None, None, None

    # ------------------------------------------------------
    # kings_adjacent()
    # ------------------------------------------------------
    # Checks whether the opposing king is located in any
    # adjacent square.
    #
    # This prevents illegal board positions where both kings
    # are directly next to one another.
    #
    # Returns:
    # • True  - opposing king is adjacent
    # • False - no adjacent opposing king
    # ------------------------------------------------------
    def kings_adjacent(self, row, col, color):

        # Check every surrounding square.
        for r in range(max(0, row - 1), min(8, row + 2)):
            for c in range(max(0, col - 1), min(8, col + 2)):

                # Ignore the king's current square.
                if r == row and c == col:
                    continue

                square = self.squares[r][c]

                if square.has_piece():

                    piece = square.piece

                    from piece import King

                    # If an enemy king is adjacent,
                    # the position is illegal.
                    if isinstance(piece, King) and piece.color != color:
                        return True

        return False
        
    # ------------------------------------------------------
    # has_legal_moves()
    # ------------------------------------------------------
    # Determines whether the specified player has at least
    # one legal move available.
    #
    # This function is used when checking for:
    # • Checkmate
    # • Stalemate
    #
    # Returns:
    # • True  - at least one legal move exists
    # • False - no legal moves are available
    # ------------------------------------------------------
    def has_legal_moves(self, color):

        # Search every square on the board.
        for row in range(ROWS):
            for col in range(COLS):

                square = self.squares[row][col]

                # Only examine occupied squares.
                if square.has_piece():

                    piece = square.piece

                    # Only consider pieces belonging to
                    # the current player.
                    if piece.color == color:

                        # Remove any previously generated moves.
                        piece.clear_moves()

                        # Generate every legal move.
                        self.calc_moves(piece, row, col, bool=True)

                        # If at least one move exists,
                        # the player is not out of moves.
                        if len(piece.moves) > 0:
                            return True

        # No legal moves were found.
        return False

    # ------------------------------------------------------
    # game_state()
    # ------------------------------------------------------
    # Determines the current state of the game for the
    # specified player.
    #
    # Possible return values:
    # • None
    # • "checkmate"
    # • "stalemate"
    # • "draw"
    # ------------------------------------------------------

    def game_state(self, color):
        """
        Determines the current game state for the player whose turn it is.

        Returns:
            "checkmate"
            "stalemate"
            "draw"
            None
        """

        legal_moves = []

        # Search every piece belonging to the player
        for row in range(ROWS):
            for col in range(COLS):

                square = self.squares[row][col]

                if square.has_piece():

                    piece = square.piece

                    if piece.color == color:

                        piece.clear_moves()

                        self.calc_moves(
                            piece,
                            row,
                            col,
                            bool=True
                        )

                        legal_moves.extend(piece.moves)

        # Player has legal moves
        if legal_moves:
            if self.insufficient_material():
                return "draw"

            return None

        # No legal moves
        if self.player_in_check(color):
            return "checkmate"

        return "stalemate"

    # ------------------------------------------------------
    # insufficient_material()
    # ------------------------------------------------------
    # Checks whether there is enough material remaining on
    # the board for either player to force checkmate.
    #
    # Current implementation:
    # • King vs King
    #
    # Returns:
    # • True  - automatic draw
    # • False - sufficient material remains
    #
    # Note:
    # This can be expanded to include:
    # • King + Bishop vs King
    # • King + Knight vs King
    # • King + Bishop vs King + Bishop
    # ------------------------------------------------------
    def insufficient_material(self):
        """
        Returns True if neither side has enough material
        to force checkmate.
        """

        pieces = []

        for row in range(ROWS):
            for col in range(COLS):

                if self.squares[row][col].has_piece():
                    pieces.append(self.squares[row][col].piece)

        # Ignore kings
        others = [
            p for p in pieces
            if not isinstance(p, King)
        ]

        # King vs King
        if len(others) == 0:
            return True

        # King+Bishop vs King
        if len(others) == 1 and isinstance(others[0], Bishop):
            return True

        # King+Knight vs King
        if len(others) == 1 and isinstance(others[0], Knight):
            return True

        # King+Bishop vs King+Bishop
        if (
            len(others) == 2 and
            all(isinstance(p, Bishop) for p in others)
        ):
            return True

        return False
        
    # ------------------------------------------------------
    # player_in_check()
    # ------------------------------------------------------
    # Determines whether the specified player's king is
    # currently under attack by any opposing piece.
    #
    # Returns:
    # • True  - the king is in check
    # • False - the king is safe
    #
    # This function is used for:
    # • Check detection
    # • Checkmate detection
    # • Move validation
    # ------------------------------------------------------
    def player_in_check(self, color):

        # Locate the king on the board.
        king, row, col = self.find_king(color)

        # Safety check in case no king exists.
        if king is None:
            return False

        # Search every square on the board.
        for r in range(8):
            for c in range(8):

                square = self.squares[r][c]

                if square.has_piece():

                    piece = square.piece

                    # Only examine enemy pieces.
                    if piece.color != color:

                        # Generate every possible attack.
                        piece.clear_moves()
                        self.calc_moves(piece, r, c, bool=False)

                        # If any move attacks the king,
                        # the king is in check.
                        for move in piece.moves:

                            if move.final.row == row and move.final.col == col:
                                return True

        return False

    # ------------------------------------------------------
    # square_attacked()
    # ------------------------------------------------------
    # Determines whether a specific square is currently
    # attacked by any opposing piece.
    #
    # Returns:
    # • True  - square is under attack
    # • False - square is safe
    #
    # Used for:
    # • King safety
    # • Castling validation
    # • AI evaluation
    # ------------------------------------------------------
    def square_attacked(self, row, col, color):

        # Search every enemy piece.
        for r in range(8):
            for c in range(8):

                square = self.squares[r][c]

                if square.has_piece():

                    piece = square.piece

                    if piece.color != color:

                        # Generate attack moves.
                        piece.clear_moves()
                        self.calc_moves(piece, r, c, bool=False)

                        # Check whether the square is attacked.
                        for move in piece.moves:

                            if move.final.row == row and move.final.col == col:
                                return True

        return False

    # ------------------------------------------------------
    # square_defended()
    # ------------------------------------------------------
    # Determines whether a specific square is currently
    # defended by any piece of the same color.
    #
    # Returns:
    # • True  - square is defended
    # • False - square is not defended
    #
    # Used for:
    # • King safety
    # • Castling validation
    # • AI evaluation
    # ------------------------------------------------------
    
    def square_defended(self, row, col, color):
        """
        Returns True if the square is defended
        by a piece of the given colour.
        """

        for r in range(ROWS):
            for c in range(COLS):

                if r == row and c == col:
                    continue

                square = self.squares[r][c]

                if not square.has_piece():
                    continue

                piece = square.piece

                if piece.color != color:
                    continue

                piece.clear_moves()

                self.calc_moves(
                    piece,
                    r,
                    c,
                    False
                )

                for move in piece.moves:
                    if move.final.row == row and move.final.col == col:
                        return True

        return False

    def position_bonus(self, piece, row, col):
        """
        Returns the positional bonus for a piece using
        piece-square tables.

        White pieces use the table directly, while black
        pieces use the same table flipped vertically.
        """

        # Dictionary linking each piece type to its
        # corresponding positional evaluation table.
        tables = {
            "pawn": PAWN_TABLE,
            "knight": KNIGHT_TABLE,
            "bishop": BISHOP_TABLE,
            "rook": ROOK_TABLE,
            "queen": QUEEN_TABLE,
            "king": KING_TABLE
        }

        # Select the correct table for the piece.
        table = tables[piece.name]

        # White pieces use the table normally.
        if piece.color == "white":
            return table[row][col]

        # Black pieces use the table upside down so that
        # good positions are mirrored correctly.
        return table[7 - row][col]
    
    # ------------------------------------------------------
    # evaluate()
    # ------------------------------------------------------
    # Evaluates the current chess position from White's
    # perspective.
    #
    # Positive score = White advantage
    # Negative score = Black advantage
    #
    # The evaluation considers:
    # • Material balance
    # • Piece development
    # • Piece centralisation
    # • Pawn advancement
    # • Centre control
    # • King safety
    # • Bishop pair advantage
    # ------------------------------------------------------
    def evaluate(self):

        score = 0

        # Standard chess piece values.
        values = {
            "pawn": 100,
            "knight": 320,
            "bishop": 330,
            "rook": 500,
            "queen": 900,
            "king": 20000
        }

        # Evaluate every piece on the board.
        for row in range(8):
            for col in range(8):

                square = self.squares[row][col]

                if square.has_piece():

                    piece = square.piece
                    value = values[piece.name]

                    # -----------------------
                    # Mobility
                    # -----------------------

                    piece.clear_moves()

                    self.calc_moves(
                        piece,
                        row,
                        col,
                        bool=False
                    )

                    mobility = len(piece.moves)

                    if piece.color == "white":
                        score += mobility
                    else:
                        score -= mobility

                    # -----------------------
                    # Piece protection
                    # -----------------------

                    # Reward pieces that are protected
                    # by another friendly piece.
                    if self.square_defended(row, col, piece.color):

                        if piece.color == "white":
                            score += 8
                        else:
                            score -= 8

                    # Slight penalty if a piece is
                    # currently attacked.
                    enemy = "black" if piece.color == "white" else "white"

                    if self.square_defended(row, col, enemy):

                        if piece.color == "white":
                            score -= 6
                        else:
                            score += 6

                    # -----------------------
                    # Material evaluation
                    # -----------------------

                    if piece.color == "white":
                        score += value
                        score += self.position_bonus(piece, row, col)
                    else:
                        score -= value
                        score -= self.position_bonus(piece, row, col)

                    # -----------------------
                    # Bishop development
                    # -----------------------

                    if piece.name == "bishop":

                        if piece.color == "white" and row != 7:
                            score += 8

                        elif piece.color == "black" and row != 0:
                            score -= 8

                        if len(piece.moves) <= 2:

                            if piece.color == "white":
                                score -= 10
                            else:
                                score += 10
                    # -----------------------
                    # Early queen penalty
                    # -----------------------

                    # Discourages bringing the queen
                    # out too early in the opening.
                    if piece.name == "queen":

                        move_count = len(self.move_history)

                        if move_count < 12:

                            if piece.color == "white" and row < 6:
                                score -= 15

                            elif piece.color == "black" and row > 1:
                                score += 15

                    # -----------------------
                    # Pawn advancement
                    # -----------------------

                    if piece.name == "pawn":

                        if piece.color == "white":
                            score += (6 - row) * 2

                        else:
                            score -= (row - 1) * 2

                    # -----------------------
                    # Centre control
                    # -----------------------

                    # Reward occupying the four
                    # central squares.
                    if piece.name != "king":

                        if row in [3, 4] and col in [3, 4]:

                            if piece.color == "white":
                                score += 15
                            else:
                                score -= 15

                                # -----------------------
                                # Early rook movement
                                # -----------------------

                                if piece.name == "rook" and piece.moved:

                                    # Number of half-moves played
                                    move_count = len(self.move_history)

                                    if move_count < 20:   # first ~10 full moves
                                        if piece.color == "white":
                                            score -= 10
                                        else:
                                            score += 10

                                if piece.name == "rook":

                                    friendly_pawn = False
                                    enemy_pawn = False

                                    for r in range(8):

                                        sq = self.squares[r][col]

                                        if sq.has_piece() and sq.piece.name == "pawn":

                                            if sq.piece.color == piece.color:
                                                friendly_pawn = True
                                            else:
                                                enemy_pawn = True

                                    # -----------------------
                                    # Open file
                                    # -----------------------
                                    if not friendly_pawn and not enemy_pawn:

                                        if piece.color == "white":
                                            score += 20
                                        else:
                                            score -= 20

                                    # -----------------------
                                    # Semi-open file
                                    # -----------------------
                                    elif not friendly_pawn:

                                        if piece.color == "white":
                                            score += 10
                                        else:
                                            score -= 10
                    # -----------------------
                    # King safety
                    # -----------------------

                    # Small bonus once the king has
                    # moved (usually after castling).
                    if piece.name == "king":

                        # Reward castled king positions.

                        if piece.color == "white":

                            if row == 7 and col in [6, 2]:
                                score += 30

                        else:

                            if row == 0 and col in [6, 2]:
                                score -= 30

        # -----------------------
        # King activity
        # -----------------------

        pieces_left = 0

        for row in range(8):
            for col in range(8):

                if self.squares[row][col].has_piece():

                    if self.squares[row][col].piece.name != "king":
                        pieces_left += 1

        # Encourage active kings once
        # most pieces have disappeared.

        if pieces_left <= 10:

            for row in range(8):
                for col in range(8):

                    if self.squares[row][col].has_piece():

                        piece = self.squares[row][col].piece

                        if piece.name == "king":

                            bonus = int((7 - (abs(row - 3.5) + abs(col - 3.5))) * 5)

                            if piece.color == "white":
                                score += bonus
                            else:
                                score -= bonus

        # -----------------------
        # Bishop pair bonus
        # -----------------------

        white_bishops = 0
        black_bishops = 0

        # Count remaining bishops.
        for row in range(8):
            for col in range(8):

                if self.squares[row][col].has_piece():

                    piece = self.squares[row][col].piece

                    if piece.name == "bishop":

                        if piece.color == "white":
                            white_bishops += 1
                        else:
                            black_bishops += 1

        # Reward players who retain
        # both bishops.
        if white_bishops >= 2:
            score += 30

        if black_bishops >= 2:
            score -= 30

        return score

    # ------------------------------------------------------
    # _create()
    # ------------------------------------------------------
    # Creates the 8×8 chess board by filling every
    # position with an empty Square object.
    #
    # Called during board initialisation.
    # ------------------------------------------------------
    def _create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    # ------------------------------------------------------
    # _add_pieces()
    # ------------------------------------------------------
    # Places every chess piece into its standard starting
    # position for the specified colour.
    #
    # Called twice:
    # • White pieces
    # • Black pieces
    # ------------------------------------------------------
    def _add_pieces(self, color):

        # Determine starting rows.
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # -----------------------
        # Place pawns
        # -----------------------
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # -----------------------
        # Place knights
        # -----------------------
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # -----------------------
        # Place bishops
        # -----------------------
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # -----------------------
        # Place rooks
        # -----------------------
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # -----------------------
        # Place queen
        # -----------------------
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # -----------------------
        # Place king
        # -----------------------
        self.squares[row_other][4] = Square(row_other, 4, King(color))
