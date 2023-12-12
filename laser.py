import pygame
from pygame.sprite import Sprite

class Laser(Sprite):
    """A class to manage lasers fired from the ship."""
 
    def __init__(self, a_game):
        """Create a laser object at the ship's current position."""
        super().__init__()
        self.screen = a_game.screen
        self.settings = a_game.settings
        self.color = self.settings.laser_color

        # Create a laser rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.laser_width,
        self.settings.laser_height)
        self.rect.midleft = a_game.hero.rect.midright
        # patenta gia na kentrarei to laser sto oplo
        self.rect.y = self.rect.y + 5

        # Store the laser's position as a float.
        self.x = float(self.rect.x)

    def update(self):
        """Move the laser cross the screen."""
        # Update the exact position of the laser.
        self.x += self.settings.laser_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_laser(self):
        """Draw the laser to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)