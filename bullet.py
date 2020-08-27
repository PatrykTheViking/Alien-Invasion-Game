import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """This class create and represent bullet object at current spaceship location"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Update bullet location"""
        self.y -= self.settings.bullet_speed

        self.rect.y = self.y

    def draw_bullet(self):
        """Display bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


