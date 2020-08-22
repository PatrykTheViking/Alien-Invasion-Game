class Settings:
    """
    This class will maintain all game settings
    """
    def __init__(self):
        # screen settings
        self.screen_width = 1400
        self.screen_height = 900
        self.background_color = (128, 128, 128)

        # ship settings
        self.ship_speed = 2.5

        # bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
