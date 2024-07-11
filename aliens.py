"""Contains the alien class and mothership class"""

import random
import pygame


class Alien(pygame.sprite.Sprite):
    """Alien class that will hold all info to get them on screen"""

    def __init__(self, color, x, y):
        """Initializing the three types of alien classes"""
        super().__init__()
        self.color = color
        path = f"Sprites/{color}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        """Updates the direction of rectangle"""
        self.rect.x += direction

    def update_again(self, direction):
        """Updates the direction faster"""
        self.rect.x += direction * 2


class Mothership(pygame.sprite.Sprite):
    """Mothership that spawns in the top left or right"""

    def __init__(self, screen_width):
        """Inits the mothership and two spawn points it can come from"""
        super().__init__()
        self.screen_width = screen_width
        self.image = pygame.image.load("Sprites/extra.png")
        x = random.choice([0, self.screen_width - self.image.get_width()])

        if x == 0:
            self.speed = 3
        else:
            self.speed = -3

        self.rect = self.image.get_rect(topleft=(x, 40))

    def change_speed(self, new_speed):
        """Changes the speed of the mothership"""
        self.speed = new_speed

    def update(self):
        """Updates the aliens."""
        self.rect.x += self.speed
        if self.rect.right > self.screen_width:
            self.kill()
        elif self.rect.left < 0:
            self.kill()
