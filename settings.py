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
        self.ship_limit = 1

        # bullet settings
        self.bullet_width = 300  # TODO change after testing
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        self.fleet_drop_speed = 40

        self.speedup_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        Settings init that change during the game
        """
        self.ship_speed = 2.5
        self.bullet_speed = 1.5
        self.alien_speed = 3.0
        self.fleet_direction = 1

    def increase_speed(self):
        """
        Speed up setting change
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale


