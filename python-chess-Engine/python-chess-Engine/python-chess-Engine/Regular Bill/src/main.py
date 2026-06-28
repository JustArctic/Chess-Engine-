import pygame
import sys

# Import the chess AI.
from ai import ChessAI

# Import the main menu.
from menu import MainMenu

# Import project files.
from const import *
from game import Game
from square import Square
from move import Move


class Main:

    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------
    # Initialises pygame, creates the game window,
    # displays the menu and creates the chess game.
    # ------------------------------------------------------
    def __init__(self):

        # Initialise pygame.
        pygame.init()

        # Create the game window.
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        # Display the main menu.
        menu = MainMenu()
        self.config = menu.run()

        # Create the game.
        self.game = Game()

        # Create the chess AI.
        self.ai = ChessAI()

    # ------------------------------------------------------
    # Main Game Loop
    # ------------------------------------------------------
    # Controls drawing, player input, AI turns,
    # game updates and screen refreshes.
    # ------------------------------------------------------
    def mainloop(self):

        screen = self.screen
        game = self.game
        board = game.board
        dragger = game.dragger
        config = self.config
        ai = self.ai

        while True:

            # ------------------------------------------
            # Draw everything
            # ------------------------------------------

            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            game.show_game_over(screen)

            # Draw the piece currently being dragged.
            if dragger.dragging:
                dragger.update_blit(screen)

            # ==========================================
            # Handle Events
            # ==========================================

            for event in pygame.event.get():

                # --------------------------------------
                # Mouse Button Pressed
                # --------------------------------------
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Ignore input if the game is over.
                    if game.game_over:
                        pygame.display.update()
                        continue

                    # Save mouse position.
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # Check if a piece exists.
                    if board.squares[clicked_row][clicked_col].has_piece():

                        piece = board.squares[clicked_row][clicked_col].piece

                        allow_move = False

                        # Determine who may move.

                        if config.game_mode == "PVP":
                            allow_move = True

                        elif config.game_mode == "PVA":
                            allow_move = (
                                piece.color == config.player_color
                            )

                        elif config.game_mode == "AVA":
                            allow_move = False

                        # Player selected their own piece.
                        if (
                            piece.color == game.next_player
                            and allow_move
                        ):

                            # Calculate legal moves.
                            board.calc_moves(
                                piece,
                                clicked_row,
                                clicked_col,
                                bool=True
                            )

                            # Save starting square.
                            dragger.save_initial(event.pos)

                            # Begin dragging.
                            dragger.drag_piece(piece)

                            # Redraw board.
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # --------------------------------------
                # Mouse Movement
                # --------------------------------------
                elif event.type == pygame.MOUSEMOTION:

                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    # Highlight hovered square.
                    game.set_hover(motion_row, motion_col)

                    # Update dragging.
                    if dragger.dragging:

                        dragger.update_mouse(event.pos)

                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)

                        dragger.update_blit(screen)

                # --------------------------------------
                # Mouse Button Released
                # --------------------------------------
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:

                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # Create attempted move.
                        initial = Square(
                            dragger.initial_row,
                            dragger.initial_col
                        )

                        final = Square(
                            released_row,
                            released_col
                        )

                        move = Move(initial, final)

                        # Execute legal move.
                        if board.valid_move(dragger.piece, move):

                            captured = board.squares[
                                released_row
                            ][released_col].has_piece()

                            board.move(
                                dragger.piece,
                                move
                            )

                            # Update en-passant.
                            board.set_true_en_passant(
                                dragger.piece
                            )

                            # Play sound.
                            game.play_sound(captured)

                            # Redraw board.
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # Switch player.
                            game.next_turn()

                            # Check for endgame.
                            state = board.game_state(
                                game.next_player
                            )

                            if state:

                                game.game_over = True

                                if state == "checkmate":

                                    winner = (
                                        "White"
                                        if game.next_player == "black"
                                        else "Black"
                                    )

                                    game.result = (
                                        f"Checkmate! {winner} wins"
                                    )

                                else:
                                    game.result = "Stalemate!"

                    # Stop dragging.
                    dragger.undrag_piece()

                # --------------------------------------
                # Keyboard Input
                # --------------------------------------
                elif event.type == pygame.KEYDOWN:

                    # Change board theme.
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # Restart game.
                    if event.key == pygame.K_r:

                        game.reset()

                        game = self.game
                        board = game.board
                        dragger = game.dragger

                # --------------------------------------
                # Close Window
                # --------------------------------------
                elif event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

            # ==========================================
            # AI Turn
            # ==========================================

            if not game.game_over:

                # --------------------------------------
                # Player vs AI
                # --------------------------------------
                if config.game_mode == "PVA":

                    if game.next_player != config.player_color:

                        result = ai.get_best_move(
                            board,
                            game.next_player,
                            depth=1
                        )

                        if result is None:

                            print(
                                "AI FOUND NO MOVE FOR",
                                game.next_player
                            )

                        else:

                            piece, move = result

                            board.move(piece, move)

                            game.next_turn()

                            state = board.game_state(
                                game.next_player
                            )

                            if state == "checkmate":

                                winner = (
                                    "White"
                                    if game.next_player == "black"
                                    else "Black"
                                )

                                game.result = (
                                    f"Checkmate! {winner} wins"
                                )

                                game.game_over = True

                            elif state == "stalemate":

                                game.result = "Stalemate!"
                                game.game_over = True

                            elif state == "draw":

                                game.result = (
                                    "Draw - Insufficient Material"
                                )

                                game.game_over = True

                            # No delay for instant AI.
                            pygame.time.delay(0)

                # --------------------------------------
                # AI vs AI
                # --------------------------------------
                elif config.game_mode == "AVA":

                    result = ai.get_best_move(
                        board,
                        game.next_player,
                        depth=2
                    )

                    if result:

                        piece, move = result

                        board.move(piece, move)

                        game.next_turn()

                        state = board.game_state(
                            game.next_player
                        )

                        if state == "checkmate":

                            winner = (
                                "White"
                                if game.next_player == "black"
                                else "Black"
                            )

                            game.result = (
                                f"Checkmate! {winner} wins"
                            )

                            game.game_over = True

                        elif state == "stalemate":

                            game.result = "Stalemate!"
                            game.game_over = True

                        elif state == "draw":

                            game.result = (
                                "Draw - Insufficient Material"
                            )

                            game.game_over = True

                        pygame.time.delay(0)

            # Refresh the display.
            pygame.display.update()


# ----------------------------------------------------------
# Program Entry Point
# ----------------------------------------------------------
# Create the Main object and start the game.
# ----------------------------------------------------------

main = Main()
main.mainloop()
