# Import the random module to introduce small variations in AI move selection.
import random

# Import copy to create deep copies of the chess board for move simulation.
import copy


# ==========================================================
# ChessAI Class
# ----------------------------------------------------------
# Controls all AI behaviour for the computer opponent.
# Uses the Minimax algorithm with Alpha-Beta pruning to
# evaluate legal chess moves and select the strongest one.
# ==========================================================
class ChessAI:

    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------
    # Stores the previous AI move to discourage repetitive
    # back-and-forth play.
    # ------------------------------------------------------
    def __init__(self):
        self.last_move = None

    # ------------------------------------------------------
    # get_best_move()
    # ------------------------------------------------------
    # Finds and returns the highest-scoring legal move for
    # the current player.
    #
    # Parameters:
    # board - Current chess board
    # color - AI colour ("white" or "black")
    # depth - Search depth (currently 1 ply)
    # ------------------------------------------------------
    def get_best_move(self, board, color, depth=1):

        best_move = None

        # White attempts to maximise the evaluation score,
        # while Black attempts to minimise it.
        if color == "white":
            best_score = float("-inf")
        else:
            best_score = float("inf")

        # Generate every legal move available.
        moves = self.get_all_moves(board, color)

        # Evaluate each possible move.
        for piece, move in moves:

            # Create a temporary board so the real game state
            # is not modified during analysis.
            temp_board = copy.deepcopy(board)

            # Retrieve the matching piece from the copied board.
            temp_piece = temp_board.squares[
                move.initial.row
            ][
                move.initial.col
            ].piece

            # Simulate the move.
            temp_board.move(temp_piece, move, testing=True)

            # Determine the opponent's colour.
            enemy_color = "black" if color == "white" else "white"

            # If this move immediately wins the game,
            # return it without further searching.
            state = temp_board.game_state(enemy_color)

            if state == "checkmate":
                self.last_move = (piece, move)
                return (piece, move)

            # Evaluate the resulting position using Minimax.
            score = self.minimax(
                temp_board,
                1,
                float("-inf"),
                float("inf"),
                color == "black"
            )

            # --------------------------------------------------
            # Small bonus for placing the opponent in check.
            # --------------------------------------------------
            if temp_board.player_in_check(enemy_color):
                score += 2 if color == "white" else -2

            # --------------------------------------------------
            # Prevent the AI from endlessly repeating moves.
            # --------------------------------------------------
            if self.last_move:

                last_piece, last_move = self.last_move

                if (
                    move.initial.row == last_move.final.row
                    and move.initial.col == last_move.final.col
                    and move.final.row == last_move.initial.row
                    and move.final.col == last_move.initial.col
                ):
                    score -= 50 if color == "white" else -50

            # --------------------------------------------------
            # Keep track of the strongest move found.
            # --------------------------------------------------
            if color == "white":

                if score > best_score:
                    best_score = score
                    best_move = (piece, move)

            else:

                if score < best_score:
                    best_score = score
                    best_move = (piece, move)

        # Save the chosen move for repetition detection.
        self.last_move = best_move

        return best_move

    # ------------------------------------------------------
    # minimax()
    # ------------------------------------------------------
    # Recursively evaluates future chess positions using the
    # Minimax algorithm with Alpha-Beta pruning.
    #
    # Parameters:
    # board - Current simulated board
    # depth - Remaining search depth
    # alpha - Best score for maximising player
    # beta - Best score for minimising player
    # maximizing - True when White is to move
    # ------------------------------------------------------
    def minimax(self, board, depth, alpha, beta, maximizing):

        # Stop searching once the required depth is reached.
        if depth == 0:
            return board.evaluate()

        # -------------------------------
        # White (Maximising Player)
        # -------------------------------
        if maximizing:

            max_eval = float("-inf")

            for piece, move in self.get_all_moves(board, "white"):

                # Create a simulated board position.
                temp_board = copy.deepcopy(board)

                temp_piece = temp_board.squares[
                    move.initial.row
                ][
                    move.initial.col
                ].piece

                # Apply the move to the simulated board.
                temp_board.move(temp_piece, move, testing=True)

                # Continue searching deeper.
                score = self.minimax(
                    temp_board,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )

                # Small random value prevents predictable play
                # when several moves have identical evaluations.
                score += random.uniform(-0.5, 0.5)

                max_eval = max(max_eval, score)

                # Update Alpha value.
                alpha = max(alpha, score)

                # Alpha-Beta pruning.
                if beta <= alpha:
                    break

            return max_eval

        # -------------------------------
        # Black (Minimising Player)
        # -------------------------------
        else:

            min_eval = float("inf")

            for piece, move in self.get_all_moves(board, "black"):

                temp_board = copy.deepcopy(board)

                temp_piece = temp_board.squares[
                    move.initial.row
                ][
                    move.initial.col
                ].piece

                # Simulate Black's move.
                temp_board.move(temp_piece, move, testing=True)

                score = self.minimax(
                    temp_board,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )

                # Small random variation to reduce repetitive play.
                score += random.uniform(-0.5, 0.5)

                min_eval = min(min_eval, score)

                # Update Beta value.
                beta = min(beta, score)

                # Alpha-Beta pruning.
                if beta <= alpha:
                    break

            return min_eval

    # ------------------------------------------------------
    # get_all_moves()
    # ------------------------------------------------------
    # Generates every legal move available for the specified
    # player and returns them as a list.
    # ------------------------------------------------------
    def get_all_moves(self, board, color):

        moves = []

        # Search every square on the board.
        for row in range(8):
            for col in range(8):

                square = board.squares[row][col]

                # Ignore empty squares.
                if square.has_piece():

                    piece = square.piece

                    # Only generate moves for the current player.
                    if piece.color == color:

                        # Remove any previously stored moves.
                        piece.clear_moves()

                        # Calculate all legal moves.
                        board.calc_moves(
                            piece,
                            row,
                            col,
                            bool=True
                        )

                        # Store each legal move.
                        for move in piece.moves:
                            moves.append((piece, move))

        # Prioritise capture moves first to improve Alpha-Beta
        # pruning efficiency.
        moves.sort(
            key=lambda x: board.squares[
                x[1].final.row
            ][
                x[1].final.col
            ].has_piece(),
            reverse=True
        )

        return moves
