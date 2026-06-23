import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Engine")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (30, 30, 30)

font = pygame.font.SysFont("arial", 40)


class GameConfig:
    def __init__(self):
        self.game_mode = None
        self.player_color = None


class MainMenu:
    def __init__(self):
        self.options = [
            "Player vs Player",
            "Player vs AI (White)",
            "Player vs AI (Black)",
            "AI vs AI",
            "Quit"
        ]
        self.selected = 0

    def draw(self):
        screen.fill(BLACK)

        title = font.render("CHESS ENGINE", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        for i, option in enumerate(self.options):

            color = YELLOW if i == self.selected else WHITE

            text = font.render(option, True, color)

            screen.blit(
                text,
                (WIDTH//2 - text.get_width()//2, 250 + i * 80)
            )

        pygame.display.flip()

    def run(self):

        config = GameConfig()

        while True:

            self.draw()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)

                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)

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
