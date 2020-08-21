import pygame


class Ship:
    """
    This class is to set up and organize players Spaceship
    """
    def __init__(self, ai_game):
        # spaceship init and it's start location
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Loads up spaceship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Location of the image
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """
        Spaceship display on proper location
        """
        self.screen.blit(self.image, self.rect)
