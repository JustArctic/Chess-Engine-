import random
import copy

class ChessAI:

    def __init__(self):
        self.last_move = None

    def get_best_move(self, board, color, depth=1):

        best_move = None

        if color == "white":
            best_score = float("-inf")
        else:
            best_score = float("inf")

        moves = self.get_all_moves(board, color)

        for piece, move in moves:

            temp_board = copy.deepcopy(board)

            temp_piece = temp_board.squares[
                move.initial.row
            ][
                move.initial.col
            ].piece

            temp_board.move(temp_piece, move, testing=True)

            enemy_color = "black" if color == "white" else "white"

            state = temp_board.game_state(enemy_color)

            if state == "checkmate":
                self.last_move = (piece, move)
                return (piece, move)

            score = self.minimax(
                temp_board,
                1,
                float("-inf"),
                float("inf"),
                color == "black"
            )

            # ---------------------
            # Small check bonus
            # ---------------------

            enemy_color = "black" if color == "white" else "white"

            if temp_board.player_in_check(enemy_color):
                score += 2 if color == "white" else -2

            # ---------------------
            # Discourage repetition
            # ---------------------

            if self.last_move:

                last_piece, last_move = self.last_move

                if (
                    move.initial.row == last_move.final.row
                    and move.initial.col == last_move.final.col
                    and move.final.row == last_move.initial.row
                    and move.final.col == last_move.initial.col
                ):
                    score -= 50 if color == "white" else -50

            # ---------------------
            # Pick best move
            # ---------------------

            if color == "white":

                if score > best_score:
                    best_score = score
                    best_move = (piece, move)

            else:

                if score < best_score:
                    best_score = score
                    best_move = (piece, move)

        self.last_move = best_move

        return best_move
        
    def minimax(self, board, depth, alpha, beta, maximizing):

        if depth == 0:
            return board.evaluate()

        if maximizing:

            max_eval = float("-inf")

            for piece, move in self.get_all_moves(board, "white"):

                temp_board = copy.deepcopy(board)

                temp_piece = temp_board.squares[
                    move.initial.row
                ][
                    move.initial.col
                ].piece

                # MISSING MOVE
                temp_board.move(temp_piece, move, testing=True)

                score = self.minimax(
                    temp_board,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )
                score += random.uniform(-0.5, 0.5)

                max_eval = max(max_eval, score)

                alpha = max(alpha, score)

                if beta <= alpha:
                    break

            return max_eval

        else:

            min_eval = float("inf")

            for piece, move in self.get_all_moves(board, "black"):

                temp_board = copy.deepcopy(board)

                temp_piece = temp_board.squares[
                    move.initial.row
                ][
                    move.initial.col
                ].piece

                temp_board.move(temp_piece, move, testing=True)

                score = self.minimax(
                    temp_board,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )
                score += random.uniform(-0.5, 0.5)

                min_eval = min(min_eval, score)

                beta = min(beta, score)

                if beta <= alpha:
                    break

            return min_eval
    
    def get_all_moves(self, board, color):

        moves = []

        for row in range(8):
            for col in range(8):

                square = board.squares[row][col]

                if square.has_piece():

                    piece = square.piece

                    if piece.color == color:

                        piece.clear_moves()

                        board.calc_moves(
                            piece,
                            row,
                            col,
                            bool=True
                        )

                        for move in piece.moves:
                            moves.append((piece, move))

        moves.sort(
            key=lambda x: board.squares[
                x[1].final.row
            ][
                x[1].final.col
            ].has_piece(),
            reverse=True
        )

        return moves