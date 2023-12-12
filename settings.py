class Settings:
    """A class to store game settings"""

    def __init__(self):
        """Initialize game's static settings"""
        # screen settings
        self.screen_width = 1100
        self.screen_height = 700
        self.bg_color = (100, 100, 120)

        # ship settings
        self.hero_limit = 3

        # alien settings
        self.fleet_drop_speed = 10
       
        # laser settings
        self.laser_width = 13
        self.laser_height = 8
        self.laser_color = (130, 40, 80)
        self.lasers_allowed = 5

        # how quickly game speeds up
        self.speedup_scale = 1.3
        # how quickly game points value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.hero_speed = 1.5
        self.laser_speed = 5.5
        self.alien_speed = 5.0

        # fleet_direction of 1 represents down; -1 represents up.
        self.fleet_direction = 1

        # scoring settings
        self.alien_points = 50
    
    def increase_speed(self):
        """Increase speed settings and point values."""
        self.hero_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
