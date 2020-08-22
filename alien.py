import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """
    Class to represent a single alien object
    """
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        # Alien image load
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Place an alien in top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Correct horizontal alien location
        self.x = float(self.rect.x)

