"""File that holds Spaceship"""

import sys
import pygame
from lasers import Laser
from menu import Menu


class Spaceship(pygame.sprite.Sprite):
    """Spaceship that holds logic"""

    def __init__(self, screen_width, screen_height):
        """Creates the spaceship and the spawn point"""
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 4
        self.image = pygame.image.load("Sprites/ship.png")
        self.rect = self.image.get_rect(
            midbottom=(self.screen_width / 2, self.screen_height)
        )
        self.lasers_group = pygame.sprite.Group()
        self.cooldown = {"fire": True, "shoot_time": 0, "shoot_delay": 500}

    def update(self):
        """Calls on the two functions to update continuously"""
        self.handle_controls()
        self.lasers_group.update()
        self.reload_gun()

    def handle_controls(self):
        """Controls the player movement"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and self.cooldown["fire"]:
            self.cooldown["fire"] = False
            laser = Laser(self.rect.center, 5, self.screen_height)
            self.lasers_group.add(laser)
            self.cooldown["shoot_time"] = pygame.time.get_ticks()
        if keys[pygame.K_q]:
            sys.exit()

        self.rect.right = min(self.rect.right, self.screen_width)
        self.rect.left = max(self.rect.left, 0)

    def reload_gun(self):
        """Limits the amount of fire the gun can have"""
        if not self.cooldown["fire"]:
            current_time = pygame.time.get_ticks()
            if (
                current_time - self.cooldown["shoot_time"]
                >= self.cooldown["shoot_delay"]
            ):
                self.cooldown["fire"] = True
