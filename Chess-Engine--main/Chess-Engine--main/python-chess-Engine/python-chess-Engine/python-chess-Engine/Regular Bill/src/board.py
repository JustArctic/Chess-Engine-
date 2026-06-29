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

        # Store the starting and ending squares.
        initial = move.initial
        final = move.final

        # Determine whether an en passant capture is occurring.
        en_passant_empty = self.squares[final.row][final.col].isempty()

        # Remove the piece from its original square.
        self.squares[initial.row][initial.col].piece = None

        # Place the piece onto its destination square.
        self.squares[final.row][final.col].piece = piece

        # --------------------------
        # Pawn-specific rules
        # --------------------------
        if isinstance(piece, Pawn):

            # Calculate horizontal movement.
            diff = final.col - initial.col

            # En passant capture.
            if diff != 0 and en_passant_empty:

                # Remove the captured pawn.
                self.squares[initial.row][initial.col + diff].piece = None

                # Place the moving pawn.
                self.squares[final.row][final.col].piece = piece

                # Play capture sound during a real game only.
                if not testing:
                    sound = Sound(
                        os.path.join('assets/sounds/capture.wav')
                    )
                    sound.play()

            # Check whether the pawn should promote.
            else:
                self.check_promotion(piece, final)

        # --------------------------
        # King-specific rules
        # --------------------------
        if isinstance(piece, King):

            # Handle castling.
            if self.castling(initial, final) and not testing:

                diff = final.col - initial.col

                # Determine which rook is castling.
                rook = (
                    piece.left_rook
                    if diff < 0
                    else piece.right_rook
                )

                # Move the rook automatically.
                self.move(rook, rook.moves[-1])

        # Mark the piece as having moved.
        piece.moved = True

        # Remove outdated legal moves.
        piece.clear_moves()

        # Store the move as the most recent move played.
        self.last_move = move

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

        # Check for automatic draw by insufficient material.
        if self.insufficient_material():
            return "draw"

        # Determine whether the player has any legal moves.
        has_moves = self.has_legal_moves(color)

        # If moves exist, the game continues.
        if has_moves:
            return None

        # No legal moves remain.
        # If the king is currently in check,
        # the player has been checkmated.
        if self.player_in_check(color):
            return "checkmate"

        # Otherwise, it is a stalemate.
        return "stalemate"

    # ------------------------------------------------------
    # get_all_legal_moves()
    # ------------------------------------------------------
    # Generates every legal move available for the specified
    # player.
    #
    # Returns a list containing:
    # (piece, move)
    #
    # This function is primarily used by the AI engine during
    # move selection and Minimax searching.
    # ------------------------------------------------------
    def get_all_legal_moves(self, color):

        legal_moves = []

        # Search every square on the chess board.
        for row in range(ROWS):
            for col in range(COLS):

                square = self.squares[row][col]

                if square.has_piece():

                    piece = square.piece

                    # Only generate moves for the selected colour.
                    if piece.color == color:

                        # Clear any previous move list.
                        piece.clear_moves()

                        # Generate all legal moves.
                        self.calc_moves(piece, row, col, bool=True)

                        # Store each move together with
                        # the piece that can perform it.
                        for move in piece.moves:
                            legal_moves.append((piece, move))

        return legal_moves

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

        pieces = []

        # Collect every remaining piece.
        for row in range(8):
            for col in range(8):

                square = self.squares[row][col]

                if square.has_piece():
                    pieces.append(square.piece)

        # If only two kings remain,
        # checkmate is impossible.
        if len(pieces) == 2:
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
                    # Material evaluation
                    # -----------------------

                    if piece.color == "white":
                        score += value
                    else:
                        score -= value

                    # -----------------------
                    # Knight centralisation
                    # -----------------------

                    if piece.name == "knight":

                        # Reward knights positioned
                        # closer to the centre.
                        center_distance = abs(row - 3.5) + abs(col - 3.5)

                        if piece.color == "white":
                            score += int((7 - center_distance) * 4)
                        else:
                            score -= int((7 - center_distance) * 4)

                    # -----------------------
                    # Bishop development
                    # -----------------------

                    if piece.name == "bishop":

                        if piece.color == "white" and row != 7:
                            score += 8

                        elif piece.color == "black" and row != 0:
                            score -= 8

                    # -----------------------
                    # Early queen penalty
                    # -----------------------

                    # Discourages bringing the queen
                    # out too early in the opening.
                    if piece.name == "queen":

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

                    # Slight penalty to discourage
                    # moving rooks before development.
                    if piece.name == "rook" and piece.moved:

                        if piece.color == "white":
                            score -= 10
                        else:
                            score += 10

                    # -----------------------
                    # King safety
                    # -----------------------

                    # Small bonus once the king has
                    # moved (usually after castling).
                    if piece.name == "king":

                        if piece.moved:

                            if piece.color == "white":
                                score += 5
                            else:
                                score -= 5

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
