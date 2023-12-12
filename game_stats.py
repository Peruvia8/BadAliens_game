class GameStats:
    """Track statistics for Alien Invasion."""
    
    def __init__(self, a_game):
        """Initialize statistics."""
        self.settings = a_game.settings
        self.reset_stats()
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.heroes_left = self.settings.hero_limit
        self.score = 0
        