import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """
    This class is to set up and organize players Spaceship
    """
    def __init__(self, ai_game):
        super().__init__()
        # spaceship init and it's start location
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Loads up spaceship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Location of the image
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Spaceship position update
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        """
        Center the ship after being hit by alien object
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """
        Spaceship displayed on proper location
        """
        self.screen.blit(self.image, self.rect)
