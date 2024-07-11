#!/usr/bin/env python3

"""
Imports the game demo and executes the main function.
"""

import sys
import random
import pygame
from spaceship import Spaceship
from lasers import AlienLaser
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    NUM_OF_STARS,
    ALIEN_START_Y,
    ALIEN_GAP_Y,
    ALIEN_COLUMNS,
    MOTHERSHIP_MIN_INTERVAL,
    MOTHERSHIP_MAX_INTERVAL,
)
from aliens import Alien, Mothership
from shields import Obstacle
from menu import Menu
from collosions import collision_check


class Game:
    """Runs the game and inits"""

    def __init__(self):
        """initializing the main components for the game"""
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.stars = self.create_stars(NUM_OF_STARS)
        self.spaceship = Spaceship(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(self.spaceship)
        self.lasers_up_group = pygame.sprite.Group()
        self.aliens_group = pygame.sprite.Group()
        self.draw_aliens()
        self.shield = self.draw_shields()
        self.aliens_shoot_group = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)
        self.alien_direction = 1
        self.mothership_group = pygame.sprite.Group()
        self.score = 0
        self.lives = 3
        self.play_music()
        self.alien_shoot_timer = random.randint(20, 100)

    def create_stars(self, num_of_stars):
        """Creating stars that make the background look neat"""
        stars = []
        for _ in range(num_of_stars):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            stars.append((x, y))
        return stars

    def draw_stars(self):
        """Draws the stars onto the screen"""
        for star in self.stars:
            self.screen.set_at(star, (255, 255, 255))

    def draw_shields(self):
        """draws the shields for the player"""
        shields = []
        shield_positions = [
            (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 100),
            (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT - 100),
        ]

        for x, y in shield_positions:
            obstacle = Obstacle(x, y)
            shields.append(obstacle)

        return shields

    def draw_aliens(self):
        """Creates the aliens onto the screen"""
        alien_types = ["yellow"] + ["red"] * 2 + ["green"] * 2

        for row_index, alien_type in enumerate(alien_types):
            y = ALIEN_START_Y + row_index * ALIEN_GAP_Y

            for column_index in range(ALIEN_COLUMNS):
                x = 75 + column_index * 55
                alien = Alien(alien_type, x, y)
                self.aliens_group.add(alien)

    def move_and_shuffle_aliens(self):
        """Moves the aliens and shuffles them when needed"""
        self.aliens_group.update(self.alien_direction)
        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= SCREEN_WIDTH or alien.rect.left <= 0:
                self.alien_direction *= -1
                for alien in self.aliens_group.sprites():
                    alien.rect.y += 12
                break

    def alien_gun(self):
        """Aliens shoot more frequently when closer to the spaceship"""
        if self.aliens_group.sprites():
            lowest_aliens = {}
            for alien in self.aliens_group.sprites():
                if (
                    alien.rect.x not in lowest_aliens
                    or alien.rect.y > lowest_aliens[alien.rect.x].rect.y
                ):
                    lowest_aliens[alien.rect.x] = alien

            shooter = random.choice(list(lowest_aliens.values()))
            alien_laser = AlienLaser(shooter.rect.center, 6, SCREEN_HEIGHT)
            self.aliens_shoot_group.add(alien_laser)

    def spawn_mothership(self):
        """Spawns the mothership at the edge"""
        self.mothership_group.add(Mothership(SCREEN_WIDTH))

    def display_score_and_lives(self):
        """Displays the current score and lives on the screen"""
        score_surface = self.font.render(f"Score: {self.score}", True, (0, 255, 0))
        self.screen.blit(score_surface, (10, 10))
        lives_surface = self.font.render(f"Lives: {self.lives}", True, (0, 255, 0))
        lives_rect = lives_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(lives_surface, lives_rect)

    def play_music(self):
        """Play background music for the game"""
        try:
            pygame.mixer.music.load("Mixes/retro.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            print("Music loaded")
        except pygame.error as e:
            print(f"Unable to load music file: {e}")

    def run(self):
        """Function to hold the event loops and keep game running"""
        mothership = pygame.USEREVENT
        pygame.time.set_timer(
            mothership,
            random.randint(MOTHERSHIP_MIN_INTERVAL, MOTHERSHIP_MAX_INTERVAL),
        )
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == mothership:
                    self.spawn_mothership()

            self.spaceship_group.update()
            self.move_and_shuffle_aliens()
            self.mothership_group.update()
            self.aliens_shoot_group.update()
            self.score, self.lives = collision_check(
                self.spaceship_group,
                self.aliens_group,
                self.mothership_group,
                self.shield,
                self.aliens_shoot_group,
                self.score,
                self.lives,
                self.screen,
            )

            if self.alien_shoot_timer <= 0:
                self.alien_gun()
                self.alien_shoot_timer = random.randint(20, 100)
            else:
                self.alien_shoot_timer -= 1

            self.screen.fill((0, 0, 0))
            self.draw_stars()
            self.spaceship_group.draw(self.screen)
            self.spaceship_group.sprite.lasers_group.draw(self.screen)
            for obstacle in self.shield:
                obstacle.block_group.draw(self.screen)
            self.aliens_group.draw(self.screen)
            self.mothership_group.draw(self.screen)
            self.aliens_shoot_group.draw(self.screen)
            self.display_score_and_lives()

            pygame.display.update()
            self.clock.tick(60)


def main():
    """Holds the logic for main and menu"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = Menu(screen)
    menu.run()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
