"""Classes that hold both the laser and alien laser"""

import pygame


class Laser(pygame.sprite.Sprite):
    """Laser class that sets up laser that moves"""

    def __init__(self, pos, speed, screen_height):
        """Creates the laser and chooses where to begin and fire"""
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill((245, 17, 17))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.screen_height = screen_height
        self.shoot_sound = pygame.mixer.Sound("Mixes/laser.mp3")
        self.shoot_sound.set_volume(0.2)
        self.shoot_sound.play()

    def update(self):
        """Updates the moving laser"""
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 10 or self.rect.y < 0:
            self.kill()


class AlienLaser(pygame.sprite.Sprite):
    """Creates the alien laser that will be used"""

    def __init__(self, position, speed, screen_height):
        """initializes the alien lasers"""
        super().__init__()
        self.image = pygame.Surface((8, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.screen_height = screen_height
        self.shoot_sound = pygame.mixer.Sound("Mixes/laserfire01.ogg")
        self.shoot_sound.set_volume(0.4)
        self.shoot_sound.play()

    def update(self):
        """updates the screen with alien laser"""
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > self.screen_height:
            self.kill()
