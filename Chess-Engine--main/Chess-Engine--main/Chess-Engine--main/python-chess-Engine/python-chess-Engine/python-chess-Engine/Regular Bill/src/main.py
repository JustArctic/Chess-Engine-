import pygame
import sys

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

    def __init__(self):
        # Initialise pygame
        pygame.init()

        # Create the game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')

        # Display the menu and save the player's settings
        menu = MainMenu()
        self.config = menu.run()

        # Create the game and AI objects
        self.game = Game()
        self.ai = ChessAI()

    def mainloop(self):

        # Create local references for easier access
        screen = self.screen
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

            # Draw the dragged piece above everything else
            if dragger.dragging:
                dragger.update_blit(screen)

            # Process all player input
            for event in pygame.event.get():

                # -----------------------------------
                # Mouse Button Pressed
                # -----------------------------------
                if event.type == pygame.MOUSEBUTTONDOWN:

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

                            # Check whether an opponent's piece is captured
                            captured = board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece, move)

                            # Update en passant eligibility
                            board.set_true_en_passant(dragger.piece)

                            # Play move or capture sound
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

                        # AI moves only on its own turn
                        if game.next_player != config.player_color:

                            # Draw the player's move first
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            pygame.display.flip()

                            # Let Pygame update the window
                            pygame.event.pump()

                        # Search for the best move
                        result = ai.get_best_move(board, game.next_player, depth=1)

                        if result is None:
                            print("AI FOUND NO MOVE FOR", game.next_player)

                        elif result:

                            piece, move = result

                            board.move(piece, move)

                            game.next_turn()

                            # Check whether the AI ended the game
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

                    # Both sides are controlled by the AI
                    result = ai.get_best_move(board, game.next_player, depth=2)

                    if result:

                        piece, move = result

                        board.move(piece, move)

                        game.next_turn()

                        # Check for game-ending conditions
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
main.mainloop()