import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """
    Class to represent a single alien object
    """
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Alien image load
        self.image = pygame.image.load('images/alien1.png')
        self.rect = self.image.get_rect()

        # Place an alien in top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Correct horizontal alien location
        self.x = float(self.rect.x)

    def check_edges(self):
        """
        The function returns true if alien reaches the edge of the screen
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """
        Move alien from left to right edge
        """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
