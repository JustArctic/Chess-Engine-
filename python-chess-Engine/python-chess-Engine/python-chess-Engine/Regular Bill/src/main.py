# main.py
# Part of the Bonnyrigg Chess Engine project.
# Auto-documented with descriptive comments.

import pygame
import sys

from ai import ChessAI
from menu import MainMenu

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')

        menu = MainMenu()
        self.config = menu.run()
        
        self.game = Game()
        self.ai = ChessAI()

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        config = self.config
        ai = self.ai

        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            game.show_game_over(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if game.game_over:
                        pygame.display.update()
                        continue

                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        allow_move = False

                        if config.game_mode == "PVP":
                            allow_move = True

                        elif config.game_mode == "PVA":
                            allow_move = (piece.color == config.player_color)

                        elif config.game_mode == "AVA":
                            allow_move = False

                        if piece.color == game.next_player and allow_move:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)                            

                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()

                            state = board.game_state(game.next_player)

                            if state:

                                game.game_over = True

                                if state:

                                    game.game_over = True
                                    game.result = "Game Over"
                                    winner = "White" if game.next_player == "black" else "Black"
                                    game.result = f"Checkmate! {winner} wins"

                                else:
                                    game.result = "Stalemate!"
                    
                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                     # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # AI turn

            if not game.game_over:

                if config.game_mode == "PVA":

                    if game.next_player != config.player_color:

                        result = ai.get_best_move(board, game.next_player, depth=1)

                        if result is None:
                            print("AI FOUND NO MOVE FOR", game.next_player)

                        elif result:

                            piece, move = result

                            board.move(piece, move)
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

                elif config.game_mode == "AVA":

                    result = ai.get_best_move(board, game.next_player, depth=2)

                    if result:

                        piece, move = result

                        board.move(piece, move)
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
                    
            pygame.display.update()


main = Main()
main.mainloop()
