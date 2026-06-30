import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square


class Game:

    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------
    # Initialises the game by creating the chess board,
    # drag-and-drop controller, configuration settings,
    # and game state variables.
    # ------------------------------------------------------
    def __init__(self):

        # White always moves first.
        self.next_player = 'white'

        # Stores the square currently being hovered over.
        self.hovered_sqr = None

        # Create the chess board.
        self.board = Board()

        # Create the drag controller.
        self.dragger = Dragger()

        # Load themes, sounds and fonts.
        self.config = Config()

        # Game over information.
        self.game_over = False
        self.result = ""
        self.ai_thinking = False

        # Move history for undo functionality.
        self.move_history = []

    # ======================================================
    # Drawing Methods
    # ======================================================

    # ------------------------------------------------------
    # Draw Chess Board
    # ------------------------------------------------------
    # Draws the checkerboard pattern together with board
    # coordinates.
    # ------------------------------------------------------
    def show_bg(self, surface):

        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):

                # Determine square colour.
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark

                # Square position and size.
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                # Draw the square.
                pygame.draw.rect(surface, color, rect)

                # Draw row numbers.
                if col == 0:

                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light

                    lbl = self.config.font.render(str(ROWS-row), True, color)

                    surface.blit(lbl, (5, 5 + row * SQSIZE))

                # Draw column letters.
                if row == 7:

                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light

                    lbl = self.config.font.render(
                        Square.get_alphacol(col),
                        True,
                        color
                    )

                    surface.blit(
                        lbl,
                        (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    )

    # ------------------------------------------------------
    # Draw Chess Pieces
    # ------------------------------------------------------
    # Draws every piece currently on the board except the
    # piece being dragged by the player.
    # ------------------------------------------------------
    def show_pieces(self, surface):

        for row in range(ROWS):
            for col in range(COLS):

                if self.board.squares[row][col].has_piece():

                    piece = self.board.squares[row][col].piece

                    # Do not draw the piece already attached
                    # to the mouse cursor.
                    if piece is not self.dragger.piece:

                        piece.set_texture(size=80)

                        img = pygame.image.load(piece.texture)

                        img_center = (
                            col * SQSIZE + SQSIZE // 2,
                            row * SQSIZE + SQSIZE // 2
                        )

                        piece.texture_rect = img.get_rect(center=img_center)

                        surface.blit(img, piece.texture_rect)

    # ------------------------------------------------------
    # Draw Valid Moves
    # ------------------------------------------------------
    # Highlights every legal move available for the piece
    # currently being dragged.
    # ------------------------------------------------------
    def show_moves(self, surface):

        theme = self.config.theme

        if self.dragger.dragging:

            piece = self.dragger.piece

            for move in piece.moves:

                color = (
                    theme.moves.light
                    if (move.final.row + move.final.col) % 2 == 0
                    else theme.moves.dark
                )

                rect = (
                    move.final.col * SQSIZE,
                    move.final.row * SQSIZE,
                    SQSIZE,
                    SQSIZE
                )

                pygame.draw.rect(surface, color, rect)

    # ------------------------------------------------------
    # Highlight Previous Move
    # ------------------------------------------------------
    # Shows the origin and destination of the most recent
    # move played.
    # ------------------------------------------------------
    def show_last_move(self, surface):

        theme = self.config.theme

        if self.board.last_move:

            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:

                color = (
                    theme.trace.light
                    if (pos.row + pos.col) % 2 == 0
                    else theme.trace.dark
                )

                rect = (
                    pos.col * SQSIZE,
                    pos.row * SQSIZE,
                    SQSIZE,
                    SQSIZE
                )

                pygame.draw.rect(surface, color, rect)

    # ------------------------------------------------------
    # Highlight Hovered Square
    # ------------------------------------------------------
    # Draws a border around the square currently underneath
    # the mouse cursor.
    # ------------------------------------------------------
    def show_hover(self, surface):

        if self.hovered_sqr:

            rect = (
                self.hovered_sqr.col * SQSIZE,
                self.hovered_sqr.row * SQSIZE,
                SQSIZE,
                SQSIZE
            )

            pygame.draw.rect(surface, (180, 180, 180), rect, width=3)

    # ======================================================
    # Game Logic
    # ======================================================

    # ------------------------------------------------------
    # Change Turn
    # ------------------------------------------------------
    # Switches between White and Black after every move.
    # ------------------------------------------------------
    def next_turn(self):

        self.next_player = (
            'white'
            if self.next_player == 'black'
            else 'black'
        )

    # ------------------------------------------------------
    # Update Hovered Square
    # ------------------------------------------------------
    # Saves the board square currently underneath the
    # player's mouse cursor.
    # ------------------------------------------------------
    def set_hover(self, row, col):

        if not (0 <= row < ROWS and 0 <= col < COLS):
            self.hovered_sqr = None
            return

        self.hovered_sqr = self.board.squares[row][col]

    # ------------------------------------------------------
    # Change Colour Theme
    # ------------------------------------------------------
    # Cycles through the available board themes.
    # ------------------------------------------------------
    def change_theme(self):

        self.config.change_theme()

    # ------------------------------------------------------
    # Play Sound Effect
    # ------------------------------------------------------
    # Plays either the move sound or capture sound.
    # ------------------------------------------------------
    def play_sound(self, captured=False):

        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    # ======================================================
    # Game Over Screen
    # ======================================================

    # ------------------------------------------------------
    # Display Game Over Overlay
    # ------------------------------------------------------
    # Shows a semi-transparent overlay displaying the game
    # result and restart instructions.
    # ------------------------------------------------------
    def show_game_over(self, surface):

        if not self.game_over:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        surface.blit(overlay, (0, 0))

        font_big = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)

        title = font_big.render(
            self.result,
            True,
            (255, 255, 255)
        )

        restart = font_small.render(
            "Press R to restart",
            True,
            (255, 255, 255)
        )

        surface.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 40)
            )
        )

        surface.blit(
            restart,
            restart.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 30)
            )
        )

    # ------------------------------------------------------
    # Reset Game
    # ------------------------------------------------------
    # Completely recreates the Game object, resetting the
    # board and all game variables.
    # ------------------------------------------------------
    def reset(self):

        self.__init__()

    # ------------------------------------------------------
    # Check Endgame Conditions
    # ------------------------------------------------------
    # Determines whether the current player is in
    # checkmate, stalemate or a draw due to insufficient
    # material.
    # ------------------------------------------------------
    def check_game_over(self):

        state = self.board.game_state(self.next_player)

        if state == "checkmate":

            winner = (
                "White"
                if self.next_player == "black"
                else "Black"
            )

            self.result = f"Checkmate! {winner} wins"
            self.game_over = True

        elif state == "stalemate":

            self.result = "Stalemate!"
            self.game_over = True

        elif state == "draw":

            self.result = "Draw - Insufficient Material"
            self.game_over = True

    def show_move_history(self, surface):
        font = pygame.font.SysFont("Arial", 20)

        x = 820   # right of the board
        y = 20

        for i, move in enumerate(self.board.move_history):
            text = font.render(move, True, (255, 255, 255))
            surface.blit(text, (x, y))

            y += 25

    def show_sidebar(self, surface):

        panel_x = 800

        # Draw the sidebar background
        pygame.draw.rect(
            surface,
            (40, 40, 40),
            (panel_x, 0, 300, 800)
        )

        # Draw a vertical divider between the board and sidebar
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (800, 0),
            (800, 800),
            2
        )

        # Display the sidebar title
        title_font = pygame.font.SysFont("Arial", 28, bold=True)
        title = title_font.render("Move History", True, (255, 255, 255))
        surface.blit(title, (825, 20))

        # Font used for displaying individual moves
        font = pygame.font.SysFont("Arial", 22)

        # Starting vertical position for the first move
        y = 70

        # Display moves two at a time (White and Black)
        history = self.board.move_history

        MAX_ROWS = 23

        start = max(
            0,
            len(history) - MAX_ROWS * 2
        )

        # -----------------------
        # Move History
        # -----------------------

        history = self.board.move_history

        # Maximum number of rows that fit in the sidebar
        MAX_ROWS = 23

        # Only show the newest moves if the history becomes too long
        start = max(
            0,
            len(history) - MAX_ROWS * 2
        )

        # Starting position
        y = 70

        for i in range(start, len(history), 2):

            # White move
            white = history[i]

            # Black move (if available)
            black = ""

            if i + 1 < len(history):
                black = history[i + 1]

            # Draw move number and moves
            text = font.render(
                f"{i//2 + 1}. {white:<8} {black}",
                True,
                (255, 255, 255)
            )

            surface.blit(text, (815, y))

            y += 30

    def show_ai_thinking(self, surface):
        # Display "AI Thinking..." message when the AI is calculating its move
        if self.ai_thinking:

            font = pygame.font.SysFont("arial", 28, bold=True)

            dots = "." * ((pygame.time.get_ticks() // 500) % 4)
            # Create the text surface with the animated dots
            text = font.render(
                f"AI Thinking{dots}",
                True,
                (255, 255, 255)
            )

            surface.blit(text, (835, 650))