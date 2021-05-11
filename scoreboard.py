import pygame.font
from pygame.sprite import Group
 
from rocket import Rocket

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, sb_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = sb_game
        self.screen = sb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sb_game.settings
        self.stats = sb_game.stats
        
        # Font settings for scoring information.
        self.text_color = ((255,255,255))
        self.font = pygame.font.SysFont("Times New Roman", 48)

        # Prepare the initial score images.
        self.set_score()
        self.set_high_score()
        self.set_level()
        self.set_rockets()

    def set_score(self):
        """Turn the score into a rendered image."""

        # Round the score to the nearest 10
        rounded_score = round(self.stats.score, -1)

        # Insert commas into numbers when converting number to a string
        score_str = "{:,}".format(rounded_score)

        # Create score's image
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def set_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
            
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def set_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)
    
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def set_rockets(self):
        """Show how many rockets are left."""
        self.rockets = Group()
        for rocket_number in range(self.stats.rockets_left):
            rocket = Rocket(self.ai_game)
            rocket.rect.x = 10 + rocket_number * rocket.rect.width
            rocket.rect.y = 10
            self.rockets.add(rocket)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.set_high_score()

    def show_score(self):
        """Draw scores, level, and rockets to the screen."""

        # Draws images of total score, highest score
        # and levels on screen at the location of respective rect's
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        self.rockets.draw(self.screen)