import pygame
import sys

# Initialise pygame before using fonts or creating a window
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 800

# Create the menu window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Engine")

# Colour constants
WHITE = (240, 240, 240)
YELLOW = (255, 215, 0)
BLACK = (20, 20, 20)
GRAY = (70, 70, 70)
DARK = (35, 35, 35)

# Fonts used throughout the menu
title_font = pygame.font.SysFont("arial", 72, bold=True)
menu_font = pygame.font.SysFont("arial", 42)
desc_font = pygame.font.SysFont("arial", 24)


class GameConfig:
    """
    Stores the options selected by the player
    before the main chess game starts.
    """

    def __init__(self):

        # Stores the chosen game mode
        self.game_mode = None

        # Stores the chosen player colour
        self.player_color = None


class MainMenu:

    def __init__(self):

        # List of menu options displayed to the user
        self.options = [
            "♔ Player vs Player",
            "♕ Play as White",
            "♚ Play as Black",
            "⚔ AI vs AI",
            "✖ Quit"
        ]

        # Description shown underneath each option
        self.descriptions = [
            "Two human players on one board",
            "You control White pieces",
            "You control Black pieces",
            "Watch two AIs battle it out",
            "Exit the game"
        ]

        # Currently selected menu option
        self.selected = 0

        # Position of the animated selection box
        self.highlight_y = 250

        # Used for fade-in animation
        self.alpha = 0

    def draw_background(self):
        """
        Draws an animated checkerboard background.
        The board slowly scrolls diagonally to give
        the menu a more modern appearance.
        """

        # Animation offset
        offset = (pygame.time.get_ticks() // 40) % 80

        for row in range(12):
            for col in range(12):

                # Alternate between two dark colours
                color = (60, 60, 60) if (row + col) % 2 else (35, 35, 35)

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        col * 80 - offset,
                        row * 80 - offset,
                        80,
                        80
                    )
                )

    def draw(self):
        """
        Draws every element of the menu.
        This function is called every frame.
        """

        # Draw moving background
        self.draw_background()

        # Increase transparency until fully visible
        self.alpha = min(255, self.alpha + 3)

        # Smoothly animate the selection box
        target_y = 250 + self.selected * 80

        self.highlight_y += (
            target_y - self.highlight_y
        ) * 0.15

        # Create a transparent surface for fade-in
        menu_surface = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        menu_surface.set_alpha(self.alpha)

        # Draw game title
        title = title_font.render(
            "CHESS ENGINE",
            True,
            WHITE
        )

        menu_surface.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                80
            )
        )

        # Draw animated highlight box
        pygame.draw.rect(
            menu_surface,
            (90, 90, 90),
            (
                WIDTH // 2 - 250,
                self.highlight_y,
                500,
                60
            ),
            border_radius=15
        )

        # Draw every menu option
        for i, option in enumerate(self.options):

            # Highlight currently selected option
            color = YELLOW if i == self.selected else WHITE

            text = menu_font.render(
                option,
                True,
                color
            )

            menu_surface.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    260 + i * 80
                )
            )

        # Draw description for selected option
        description = desc_font.render(
            self.descriptions[self.selected],
            True,
            (200, 200, 200)
        )

        menu_surface.blit(
            description,
            (
                WIDTH // 2 - description.get_width() // 2,
                700
            )
        )

        # Display controls at the bottom
        version = desc_font.render(
            "F11 = Fullscreen   |   Enter = Select",
            True,
            (140, 140, 140)
        )

        menu_surface.blit(
            version,
            (
                WIDTH // 2 - version.get_width() // 2,
                750
            )
        )

        # Draw the completed menu to the screen
        screen.blit(menu_surface, (0, 0))

        # Update the display
        pygame.display.flip()

    def run(self):
        """
        Main menu loop.
        Waits until the player chooses a game mode,
        then returns the selected configuration.
        """

        # Create configuration object
        config = GameConfig()

        # Used to keep the menu at 60 FPS
        clock = pygame.time.Clock()

        while True:

            # Draw the menu
            self.draw()

            # Check for player input
            for event in pygame.event.get():

                # Close window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Keyboard controls
                elif event.type == pygame.KEYDOWN:

                    # Move selection up
                    if event.key == pygame.K_UP:
                        self.selected = (
                            self.selected - 1
                        ) % len(self.options)

                    # Move selection down
                    elif event.key == pygame.K_DOWN:
                        self.selected = (
                            self.selected + 1
                        ) % len(self.options)

                    # Confirm selection
                    elif event.key == pygame.K_RETURN:

                        print("ENTER PRESSED")
                        print("Selected:", self.selected)

                        # Player vs Player
                        if self.selected == 0:
                            config.game_mode = "PVP"
                            return config

                        # Player vs AI (White)
                        elif self.selected == 1:
                            config.game_mode = "PVA"
                            config.player_color = "white"
                            return config

                        # Player vs AI (Black)
                        elif self.selected == 2:
                            config.game_mode = "PVA"
                            config.player_color = "black"
                            return config

                        # AI vs AI
                        elif self.selected == 3:
                            config.game_mode = "AVA"
                            return config

                        # Quit game
                        elif self.selected == 4:
                            pygame.quit()
                            sys.exit()

            # Limit the menu to 60 FPS
            clock.tick(60)
