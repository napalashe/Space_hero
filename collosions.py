"""Collosion check function and game over function"""

import sys
import pygame
from menu import Menu
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.mixer.init()
alien_death_sound = pygame.mixer.Sound("Mixes/laserthing.wav")
alien_death_sound.set_volume(0.5)
ship_hit_shound = pygame.mixer.Sound("Mixes/boom1.wav")
ship_hit_shound.set_volume(0.4)


def collision_check(
    spaceship_group,
    aliens_group,
    mothership_group,
    shield,
    aliens_shoot_group,
    score,
    lives,
    screen,
):
    """Game logic to check if collisions have been met"""
    if spaceship_group.sprite.lasers_group:
        for throw_sprite in spaceship_group.sprite.lasers_group:
            if pygame.sprite.spritecollide(throw_sprite, aliens_group, True):
                throw_sprite.kill()
                score += 10
                alien_death_sound.play()
            if pygame.sprite.spritecollide(throw_sprite, mothership_group, True):
                throw_sprite.kill()
            if len(aliens_group) == 0:
                game_over(screen)
                lives = 3
                score = 0
            for obstacle in shield:
                if pygame.sprite.spritecollide(
                    throw_sprite, obstacle.block_group, True
                ):
                    throw_sprite.kill()

    if aliens_shoot_group:
        for throw_sprite in aliens_shoot_group:
            if pygame.sprite.spritecollide(throw_sprite, spaceship_group, False):
                throw_sprite.kill()
                lives -= 1
                ship_hit_shound.play()
                if lives == 0:
                    game_over(screen)
                    lives = 3
                    score = 0
            for obstacle in shield:
                if pygame.sprite.spritecollide(
                    throw_sprite, obstacle.block_group, True
                ):
                    throw_sprite.kill()

    if aliens_group:
        for throw_sprite in aliens_group:
            for obstacle in shield:
                pygame.sprite.spritecollide(throw_sprite, obstacle.block_group, True)
        if pygame.sprite.spritecollide(throw_sprite, spaceship_group, False):
            game_over(screen)
    return score, lives

# def show_score(self):
#     for score in self.score:
#         pygame.

def game_over(screen):
    """Function to handle game over and restart to main menu"""
    game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = Menu(game_screen)
    menu.run()
