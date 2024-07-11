"""Menu screen that starts when the game is booted up"""

import sys
import random
import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    NUM_OF_STARS,
    WHITE,
    BLACK,
    GREEN,
    FPS,
    RED,
)


class Menu:
    """Menu class that boots when game is launched"""

    def __init__(self, display_screen):
        """Initialize the menu components"""
        self.screen = display_screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.match_font("arial", 74)
        self.stars = self.create_stars(NUM_OF_STARS)
        pygame.mixer.init()
        self.play_music()

    def create_stars(self, num_of_stars):
        """Creating stars that make the background look neat"""
        stars = []
        for _ in range(num_of_stars):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            stars.append((x, y))
        return stars

    def draw_stars(self):
        """Draws stars to the main menu screen"""
        for star in self.stars:
            self.screen.set_at(star, WHITE)

    def display_text(self, text, size, color, position):
        """Display text on the screen"""
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def play_music(self):
        """Play background music for the menu"""
        try:
            pygame.mixer.music.load("Mixes/game_music.wav")
            pygame.mixer.music.play(-1)
            print("Music loaded and playing.")
        except pygame.error as e:
            print(f"Unable to load music file: {e}")

    def run(self):
        """Run the menu loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        return

            self.screen.fill(BLACK)
            self.draw_stars()
            self.display_text(
                "Space Invaders",
                74,
                GREEN,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50),
            )
            self.display_text(
                "------------------------",
                74,
                GREEN,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 21),
            )
            self.display_text(
                "Press Enter to Start",
                36,
                GREEN,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50),
            )
            self.display_text(
                "Press q to exit",
                36,
                RED,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300),
            )
            self.display_text(
                "Created By: Christopher Mireles!",
                36,
                GREEN,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 300),
            )

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = Menu(game_screen)
    menu.run()
