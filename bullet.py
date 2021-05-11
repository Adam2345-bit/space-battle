import pygame
from pygame.sprite import Sprite
 
class Bullet(Sprite):
    """A class to manage bullets fired from the rocket"""

    def __init__(self, sb_game):
        """Create a bullet object at the rocket's current position."""
        super().__init__()
        self.screen = sb_game.screen
        self.settings = sb_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = sb_game.rocket.rect.midtop
        
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)