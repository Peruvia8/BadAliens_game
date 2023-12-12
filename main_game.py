# modules & functions
import sys
from time import sleep
import pygame

# classes
from settings import Settings
from game_stats import GameStats
from hero import Hero
from laser import Laser
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class Game:
    """Main class to control game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # start game in active state
        self.game_active = False
        
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        
        # make the play button
        self.play_button = Button(self, "Play")

        self.rect = self.screen.get_rect()
        pygame.display.set_caption("Bad Aliens")

        # create instance to store game statistics
        #   and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

# The call to hero() requires one argument: an instance 
# of AlienInvasion. The self argument here refers to the current instance of 
# AlienInvasion. This is the parameter that gives hero access to the game’s 
# resources, such as the screen object
        self.hero = Hero(self)
        self.lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        
        # Make an alien and keep adding till no more room
        # spacing between aliens is one alien width and one height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        # alien_width * 7 apomakrynei ta aliens apo ton typa
        current_x, current_y = alien_width * 7, alien_height
        while current_x < (self.settings.screen_width - alien_width):
            while current_y < (self.settings.screen_height - 2 * alien_height):
                self._create_alien(current_x, current_y)
                current_y += 2 * alien_height

            current_y = alien_height
            current_x += 2 * alien_width

    def _hero_hit(self):
        """Respond to the hero being hit by an alien."""
        if self.stats.heroes_left > 0:
            # Decrement heroes_left.
            self.stats.heroes_left -= 1

            # Get rid of any remaining bullets and aliens.
            self.lasers.empty()
            self.aliens.empty()

            # Create a new fleet and center the hero.
            self._create_fleet()
            self.hero.center_hero()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _create_alien(self, x_position, y_position):
        """Create alien and place in the row"""
        new_alien = Alien(self)
        new_alien.y = y_position
        new_alien.rect.y = y_position
        new_alien.rect.x = x_position
        self.aliens.add(new_alien)

    def run_game(self):
        """Start main game loop"""
        while True:
            self.checkevnts()
            if self.game_active:
                self.hero.update()
                self._update_lasers()    
                self._update_aliens()

            # draw most recent frame
            self._update_screen()
            self.clock.tick(30)

    def checkevnts(self):
        """Respond to key presses"""

        # watch for keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # self._check_keydown_events(self, event) --> wrong! self is
                # already included in the call
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start new game when play button is clicked"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # reset the game settings
            self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True

            # rid of remaining lasers and aliens
            self.lasers.empty()
            self.aliens.empty()

            # create new fleet
            self._create_fleet()
            self.hero.center_hero()

            # hide mouse cursor
            pygame.mouse.set_visible(False)

    def _update_aliens(self):
        """Check if at edge and update position of all aliens"""
        self._change_fleet_edges()
        self.aliens.update()

        # look for alien hero collisions
        if pygame.sprite.spritecollideany(self.hero, self.aliens):
            self._hero_hit()

        # look for aliens hitting bottom (left)
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the left of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                # Treat this the same as if the hero got hit.
                self._hero_hit()
                break # break because one alien enough for game over

    def _change_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
                

    def _check_keydown_events(self, event):
        if event.key == pygame.K_LEFT:
            self.hero.moving_up = True
            self.hero.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.hero.moving_down = True
            self.hero.moving_up = False
        elif event.key == pygame.K_SPACE:
            self._fire_laser()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.hero.moving_up = False
        elif event.key == pygame.K_RIGHT:
            self.hero.moving_down = False

    def _fire_laser(self):
        if len(self.lasers) < self.settings.lasers_allowed:
            new_laser = Laser(self)
            self.lasers.add(new_laser)

    def _update_lasers(self):
        self.lasers.update()
        # Get rid of lasers that have disappeared.
        for laser in self.lasers.copy():
            if laser.rect.left >= self.rect.right:
                self.lasers.remove(laser)
        self._check_laser_alien_collisions()

    def _check_laser_alien_collisions(self):
        # Check for any lasers that hit aliens.
        # If so, get rid of the laser and the alien.
        collisions = pygame.sprite.groupcollide(
            self.lasers, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
        if not self.aliens:
            # destroy existing lasers and create batch of aliens
            self.lasers.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_screen(self):
        """Update images on screen, flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        for laser in self.lasers.sprites():
            laser.draw_laser()
        self.hero.blitme()
        self.aliens.draw(self.screen)

        # draw score information
        self.sb.show_score()

        # draw play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()



if  __name__ == '__main__':
    # make game instance, run game
    ba = Game()
    ba.run_game()