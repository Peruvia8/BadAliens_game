import pygame

class Hero():
    """A class to control hero"""

    def __init__(self, a_game):
        """Initialize hero and starting position"""
        self.screen = a_game.screen
        self.settings = a_game.settings
        self.screen_rect = a_game.screen.get_rect()

        # load hero image and get rekt
        self.image = pygame.image.load('assets//hero.png')
        self.rect = self.image.get_rect()

        # start each hero at midleft
        self.rect.midleft = self.screen_rect.midleft

        # store movement speed as float
        self.y = float(self.rect.y)

        # movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update hero location based on flag"""
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.hero_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.hero_speed

        # update rect object from self.y
        self.rect.y = self.y

    def blitme(self):
        """Draw hero at its current lokeisio"""
        self.screen.blit(self.image, self.rect)

    def center_hero(self):
        """Center the hero on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

