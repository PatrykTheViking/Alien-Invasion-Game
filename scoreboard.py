import pygame.sysfont


class Scoreboard:
    """
    Class to represent actual player score
    """
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font set up for scoreboard
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # main set up
        self.prep_score()

    def prep_score(self):
        """
        Transform scoreboard into image object
        """
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.background_color)

        # display scoreboard at right top corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """
        Display score on the board
        """
        self.screen.blit(self.score_image, self.score_rect)
