import pygame.sysfont


class Button:

    def __init__(self, ai_game, screen, message):

        self.screen = ai_game.screen
        self.screen_rect = self.screen_rect.get_rect()

        # size and button settings
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)  # none att uses default font + size

        # create button rect and center location
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # print message
        self._prep_message(message)

    def _prep_message(self, message):
        """
        Place text in generated button object and center
        """
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        # font.render method convert msg text into image
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        # display empty button with text
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
