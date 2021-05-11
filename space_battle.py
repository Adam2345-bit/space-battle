import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from play_button import PlayButton
from rocket import Rocket
from bullet import Bullet
from spaceship import SpaceShip

class SpaceBattle:
    """Main class that manages game's assets"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        # Get game's settings
        self.settings = Settings()

        # Create a main display
        self.screen = pygame.display.set_mode((1200, 800))

        # Set a main display's name
        pygame.display.set_caption("Space Battle")

        # Create an instance to store game statistics
        self.stats = GameStats(self)

        # Create a scoreboard
        self.scoreboard = Scoreboard(self)

        # Create a rocket
        self.rocket = Rocket(self)

        # Create a list of bullets
        self.bullets = pygame.sprite.Group()

        # Create a fleet of spaceships
        self.spaceships = pygame.sprite.Group()
        self._create_fleet()

        # Make the Start button.
        self.start_button = PlayButton(self, "Start")

    def run_game(self):
        """Start game's main loop."""
        while True:
            # Monitors key presses and releases
            self._check_key_mouse_events()

            # Updates positions of game's moving elements
            self._update_positions()

            # Flipping the main screen
            self._update_screen()

    def _update_positions(self):
        """Update the position of a rocket, bullets, and spaceships."""
        if self.stats.game_active:
            self.rocket.update()
            self._update_bullets()
            self._update_spaceships()

    def _check_key_mouse_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._press_play_button(mouse_pos)

    def _press_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""

        # Returns true if the point of a mouse click overlaps
        # with the start button
        button_clicked = self.start_button.rect.collidepoint(mouse_pos)

        # If the button is clicked and the game has not started yet,
        # it means player starts a new game. So, reset the game.
        if button_clicked and not self.stats.game_active:
            self._reset_dynamic_settings()
            self._reset_games_stats()

            # Get rid of any remaining spaceships
            self.spaceships.empty()

            # Get rid of any remaining bullets
            self.bullets.empty()
            
            # Create a new fleet
            self._create_fleet()

            # Center the rocket
            self.rocket.center_rocket()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _reset_games_stats(self):
        """Reset the game statistics."""
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.set_score()
        self.scoreboard.set_level()
        self.scoreboard.set_rockets()

    def _reset_dynamic_settings(self):
        """Reset the game's dynamic settings."""
        self.settings.initialize_dynamic_settings()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.rocket.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.rocket.moving_left = True
        elif event.key == pygame.K_UP:
            self.rocket.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.rocket.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.rocket.moving_left = False
        elif event.key == pygame.K_UP:
            self.rocket.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = False

    def _fire_bullet(self):
        """
        If the number of current bullets on the screen
        is less than number of bullets allowed to be fired, then
        create a new bullet and add it to the bullets group.
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        self._clean_off_screen_bullets()

        self._check_bullet_spaceship_collisions()

    def _clean_off_screen_bullets(self):
        """Get rid of bullets that are off screen."""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_spaceship_collisions(self):
        """Respond to bullet-spaceship collisions."""

        # Returns dictionary containing bullets (key) and spaceships (values) that
        # were hit
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.spaceships, True, True)

        self._update_total_score(collisions)

        self._increase_difficulty()

    def _increase_difficulty(self):
        """
        If there are no more spaceships on the screen, the
        increase the difficulty of the game
        """
        if not self.spaceships:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.scoreboard.set_level()

    def _update_total_score(self, collisions):
        """Update the total score on the game's screen"""
        # If collision dictionary exists, then add spaceships' total value to
        # a score.
        if collisions:
            for spaceships in collisions.values():
                self.stats.score += self.settings.spaceship_points * len(spaceships)

            # Create new image of updated total score
            self.scoreboard.set_score()
            self.scoreboard.check_high_score()

    def _update_spaceships(self):
        """
        Check if the fleet is at an border of a screen,
          then update the positions of spaceships' fleet.
        """
        self._check_fleet_edges()
        self.spaceships.update()

        # If the rocket touches an spaceship, then rocket is hit
        if pygame.sprite.spritecollideany(self.rocket, self.spaceships):
            self._rocket_hit()

        self._check_spaceships_bottom()

    def _check_spaceships_bottom(self):
        """Check if any spaceships have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for spaceship in self.spaceships.sprites():
            if spaceship.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the rocket got hit.
                self._rocket_hit()
                break

    def _rocket_hit(self):
        """Respond to the rocket being hit by an spaceship."""
        if self.stats.rockets_left > 0:
            # Decrement rockets_left, and update scoreboard.
            self.stats.rockets_left -= 1
            self.scoreboard.set_rockets()
            
            # Get rid of any remaining spaceships and bullets.
            self.spaceships.empty()
            self.bullets.empty()
            
            # Create a new fleet and center the rocket.
            self._create_fleet()
            self.rocket.center_rocket()
            
            # Pause a game to let player see what happened
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of spaceships."""

        # Create an spaceship and find the number of spaceships in a row.
        # Spacing between each spaceship is equal to one spaceship width.
        spaceship = SpaceShip(self)
        spaceship_width, spaceship_height = spaceship.rect.size

        # Calculate the number of spaceships in a row
        # (2 * spaceship_width) creates margins on either side of a screen
        available_space_x = self.settings.screen_width - (2 * spaceship_width)
        number_spaceships_x = available_space_x // (2 * spaceship_width)
        
        # Determine the number of rows of spaceships that fit on the screen.
        rocket_height = self.rocket.rect.height
        available_space_y = (self.settings.screen_height -
                                (18 * spaceship_height) - rocket_height)
        number_rows = available_space_y // (2 * spaceship_height)
        
        # Create the full fleet of spaceships.
        for row_number in range(number_rows):
            for spaceship_number in range(number_spaceships_x):
                self._create_spaceship(spaceship_number, row_number)

    def _create_spaceship(self, spaceship_number, row_number):
        """Create an spaceship and place it in the row."""
        spaceship = SpaceShip(self)
        spaceship_width, spaceship_height = spaceship.rect.size
        spaceship.x = spaceship_width + 2 * spaceship_width * spaceship_number
        spaceship.rect.x = spaceship.x
        spaceship.rect.y = 3.5 * spaceship.rect.height + 2 * spaceship.rect.height * row_number
        self.spaceships.add(spaceship)

    def _check_fleet_edges(self):
        """
        If any spaceship touches screen's edges,
        then change the direction of a fleet.
        """
        for spaceship in self.spaceships.sprites():
            if spaceship.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for spaceship in self.spaceships.sprites():
            spaceship.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        # Draw a rocket
        self.rocket.blitme()

        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw spaceships
        self.spaceships.draw(self.screen)

        # Draw the score information.
        self.scoreboard.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.start_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = SpaceBattle()
    ai.run_game()