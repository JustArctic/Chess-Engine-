# menu.py
# Part of the Bonnyrigg Chess Engine project.
# Auto-documented with descriptive comments.

import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Engine")

WHITE = (240, 240, 240)
YELLOW = (255, 215, 0)
BLACK = (20, 20, 20)
GRAY = (70, 70, 70)
DARK = (35, 35, 35)

title_font = pygame.font.SysFont("arial", 72, bold=True)
menu_font = pygame.font.SysFont("arial", 42)
desc_font = pygame.font.SysFont("arial", 24)


class GameConfig:
    def __init__(self):
        self.game_mode = None
        self.player_color = None


class MainMenu:

    def __init__(self):

        self.options = [
            "♔ Player vs Player",
            "♕ Play as White",
            "♚ Play as Black",
            "⚔ AI vs AI",
            "✖ Quit"
        ]

        self.descriptions = [
            "Two human players on one board",
            "You control White pieces",
            "You control Black pieces",
            "Watch two AIs battle it out",
            "Exit the game"
        ]

        self.selected = 0

        self.highlight_y = 250

        self.alpha = 0

    def draw_background(self):

        offset = (pygame.time.get_ticks() // 40) % 80

        for row in range(12):
            for col in range(12):

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

        self.draw_background()

        self.alpha = min(255, self.alpha + 3)

        target_y = 250 + self.selected * 80

        self.highlight_y += (
            target_y - self.highlight_y
        ) * 0.15

        menu_surface = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        menu_surface.set_alpha(self.alpha)

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

        for i, option in enumerate(self.options):

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

        screen.blit(menu_surface, (0, 0))

        pygame.display.flip()

    def run(self):

        config = GameConfig()

        clock = pygame.time.Clock()

        while True:

            self.draw()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.selected = (
                            self.selected - 1
                        ) % len(self.options)

                    elif event.key == pygame.K_DOWN:
                        self.selected = (
                            self.selected + 1
                        ) % len(self.options)

                    elif event.key == pygame.K_RETURN:

                        print("ENTER PRESSED")
                        print("Selected:", self.selected)

                        if self.selected == 0:
                            config.game_mode = "PVP"
                            return config

                        elif self.selected == 1:
                            config.game_mode = "PVA"
                            config.player_color = "white"
                            return config

                        elif self.selected == 2:
                            config.game_mode = "PVA"
                            config.player_color = "black"
                            return config

                        elif self.selected == 3:
                            config.game_mode = "AVA"
                            return config

                        elif self.selected == 4:
                            pygame.quit()
                            sys.exit()

            clock.tick(60)