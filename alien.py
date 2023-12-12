import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, a_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = a_game.screen
        self.settings = a_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('assets/bad.png')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Start each new alien near the top right of the screen.
        self.rect.y = self.screen_rect.top
        self.rect.right = self.screen_rect.right
        #self.rect.midtop = 100

        # Store the alien's exact horizontal position.
        self.y = float(self.rect.y)

    def update(self):
        """Move alien down or up """
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        return(self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0)
    
    