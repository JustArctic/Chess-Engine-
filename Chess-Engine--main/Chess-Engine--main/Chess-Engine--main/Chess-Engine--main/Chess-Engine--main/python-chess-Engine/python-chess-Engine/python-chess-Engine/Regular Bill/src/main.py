import copy

import pygame
import sys
import threading

# Import AI opponent
from ai import ChessAI

# Import main menu for game configuration
from menu import MainMenu

# Import constants such as screen dimensions
from const import *

# Import game components
from game import Game
from square import Square
from move import Move


class Main:
    """Main controller for the chess game."""

    def run(self):

        while True:

            menu = MainMenu(self.screen)
            self.config = menu.run()

            self.game = Game()
            self.ai = ChessAI()
            self.ai_thread = None
            self.ai_result = None

            self.mainloop()

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        self.config = None
        self.game = None
        self.ai = None

    def ai_worker(self, board, color):
        self.ai_result = self.ai.get_best_move(board, color, depth=2)

    def mainloop(self):

        # Create local references for easier access
        screen = self.screen
        button_width = 180
        button_height = 45

        sidebar_width = WIDTH - BOARD_SIZE

        button_x = BOARD_SIZE + (sidebar_width - button_width) // 2
        button_y = HEIGHT - 70

        menu_button = pygame.Rect(
            button_x,
            button_y,
            button_width,
            button_height
        )
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        config = self.config
        ai = self.ai

        # Main game loop
        while True:

            # Draw all game elements
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            game.show_game_over(screen)
            game.show_sidebar(screen)
            game.show_ai_thinking(screen)

            mouse = pygame.mouse.get_pos()

            button_color = (80, 80, 80)
            if menu_button.collidepoint(mouse):
                button_color = (110, 110, 110)

            pygame.draw.rect(self.screen, button_color, menu_button, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), menu_button, 2, border_radius=10)

            font = pygame.font.SysFont("arial", 28, bold=True)
            text = font.render("Return to Menu", True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=menu_button.center))

            # Draw the dragged piece above everything else
            if dragger.dragging:
                dragger.update_blit(screen)

            # Process all player input
            for event in pygame.event.get():

                # -----------------------------------
                # Mouse Button Pressed
                # -----------------------------------
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.ai_thread = None
                    self.ai_result = None

                    # Return to menu button
                    if menu_button.collidepoint(event.pos):
                        game.ai_thinking = False
                        self.ai_thread = None
                        self.ai_result = None
                        return

                    # Ignore input if the game has ended
                    if game.game_over:
                        pygame.display.update()
                        continue

                    # Record mouse position
                    dragger.update_mouse(event.pos)

                    clicked_row = event.pos[1] // SQSIZE
                    clicked_col = event.pos[0] // SQSIZE

                    # Check if a piece exists on the selected square
                    if not (0 <= clicked_row < ROWS and 0 <= clicked_col < COLS):
                        continue
                    if board.squares[clicked_row][clicked_col].has_piece():

                        piece = board.squares[clicked_row][clicked_col].piece

                        # Determine whether the selected piece can be moved
                        allow_move = False

                        if config.game_mode == "PVP":
                            allow_move = True

                        elif config.game_mode == "PVA":
                            allow_move = (piece.color == config.player_color)

                        elif config.game_mode == "AVA":
                            allow_move = False

                        # Only allow the current player to move their own piece
                        if piece.color == game.next_player and allow_move:

                            # Calculate all legal moves
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)

                            # Begin dragging the selected piece
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            # Refresh the display
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # -----------------------------------
                # Mouse Movement
                # -----------------------------------
                elif event.type == pygame.MOUSEMOTION:

                    # Update hovered square
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    # Only update the hover square if the mouse is on the board
                    if 0 <= motion_row < ROWS and 0 <= motion_col < COLS:
                        game.set_hover(motion_row, motion_col)
                    else:
                        game.hovered_sqr = None

                    # Move the dragged piece with the cursor
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)

                        dragger.update_blit(screen)

                # -----------------------------------
                # Mouse Button Released
                # -----------------------------------
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:

                        dragger.update_mouse(event.pos)

                        # Get the mouse position
                        mouse_x, mouse_y = event.pos

                        # Ignore releases outside the chess board
                        if mouse_x < 0 or mouse_x >= BOARD_SIZE or mouse_y < 0 or mouse_y >= BOARD_SIZE:
                            dragger.undrag_piece()
                            continue

                        # Convert mouse position to board coordinates
                        released_row = mouse_y // SQSIZE
                        released_col = mouse_x // SQSIZE

                        # Create the attempted move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # Execute the move if it is legal
                        if board.valid_move(dragger.piece, move):

                            captured = board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)

                            print("Captured =", captured)
                            game.play_sound(captured)

                            # Redraw the board
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # Switch to the other player's turn
                            game.next_turn()

                            # Determine whether the game has ended
                            state = board.game_state(game.next_player)

                            if state == "checkmate":
                                game.game_over = True
                                winner = "White" if game.next_player == "black" else "Black"
                                game.result = f"Checkmate! {winner} wins"

                            elif state == "stalemate":
                                game.game_over = True
                                game.result = "Stalemate!"

                            elif state == "draw":
                                game.game_over = True
                                game.result = "Draw"

                    # Stop dragging regardless of whether the move succeeded
                    dragger.undrag_piece()

                # -----------------------------------
                # Keyboard Input
                # -----------------------------------
                elif event.type == pygame.KEYDOWN:

                    # Change board theme
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # Reset the game
                    if event.key == pygame.K_r:
                        game.reset()

                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                    elif event.key == pygame.K_ESCAPE:
                        self.ai_thread = None
                        self.ai_result = None
                        return

                # -----------------------------------
                # Exit Game
                # -----------------------------------
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # ===================================
            # AI Turns
            # ===================================
            if not game.game_over:

                # -----------------------------
                # Player vs AI
                # -----------------------------
                if config.game_mode == "PVA":

                    # AI moves only on its own turn
                    if game.next_player != config.player_color:

                        # Draw the player's move first
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        pygame.display.flip()

                        # Allow the user to return to the menu while the AI is thinking
                        for event in pygame.event.get():

                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    game.ai_thinking = False
                                    self.ai_thread = None
                                    self.ai_result = None
                                    return

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if menu_button.collidepoint(event.pos):
                                    self.ai_thread = None
                                    self.ai_result = None
                                    return

                        game.ai_thinking = True
                        # Start AI if it isn't already thinking
                        if self.ai_thread is None:

                            board_copy = copy.deepcopy(board)

                            self.ai_thread = threading.Thread(
                                target=self.ai_worker,
                                args=(board_copy, game.next_player)
                            )

                            self.ai_thread.start()

                        # AI finished?
                        elif not self.ai_thread.is_alive():

                            result = self.ai_result

                            self.ai_thread = None
                            self.ai_result = None
                            game.ai_thinking = False

                            if result:

                                piece, move = result

                                # Convert copied piece to real piece
                                piece = board.squares[
                                    move.initial.row
                                ][
                                    move.initial.col
                                ].piece

                                captured = board.move(piece, move)

                                game.play_sound(captured)

                                board.set_true_en_passant(piece)

                                game.next_turn()

                                state = board.game_state(game.next_player)

                                if state == "checkmate":
                                    winner = "White" if game.next_player == "black" else "Black"
                                    game.result = f"Checkmate! {winner} wins"
                                    game.game_over = True

                                elif state == "stalemate":
                                    game.result = "Stalemate!"
                                    game.game_over = True

                                elif state == "draw":
                                    game.result = "Draw - Insufficient Material"
                                    game.game_over = True

                        # No delay between AI moves
                        pygame.time.delay(0)

                # -----------------------------
                # AI vs AI
                # -----------------------------
                elif config.game_mode == "AVA":

                    # Allow the user to return to the menu while the AI is thinking
                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                game.ai_thinking = False
                                self.ai_thread = None
                                self.ai_result = None
                                return

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if menu_button.collidepoint(event.pos):
                                self.ai_thread = None
                                self.ai_result = None
                                return
                    
                    game.ai_thinking = True
                    # Start AI if it isn't already thinking
                    if self.ai_thread is None:

                        board_copy = copy.deepcopy(board)

                        self.ai_thread = threading.Thread(
                            target=self.ai_worker,
                            args=(board_copy, game.next_player)
                        )

                        self.ai_thread.start()

                    # AI finished?
                    elif not self.ai_thread.is_alive():

                        result = self.ai_result

                        self.ai_thread = None
                        self.ai_result = None
                        game.ai_thinking = False

                        if result:

                            piece, move = result

                            # Convert copied piece to real piece
                            piece = board.squares[
                                move.initial.row
                            ][
                                move.initial.col
                            ].piece

                            captured = board.move(piece, move)

                            game.play_sound(captured)

                            board.set_true_en_passant(piece)

                            game.next_turn()

                            state = board.game_state(game.next_player)

                            if state == "checkmate":
                                winner = "White" if game.next_player == "black" else "Black"
                                game.result = f"Checkmate! {winner} wins"
                                game.game_over = True

                            elif state == "stalemate":
                                game.result = "Stalemate!"
                                game.game_over = True

                            elif state == "draw":
                                game.result = "Draw - Insufficient Material"
                                game.game_over = True

                    pygame.time.delay(0)

            # Update the display every frame
            pygame.display.update()


# Start the application
main = Main()
main.run()