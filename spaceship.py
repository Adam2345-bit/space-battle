import pygame
from pygame.sprite import Sprite
 
class SpaceShip(Sprite):
    """A class to represent a single spaceship in the fleet."""

    def __init__(self, ai_game):
        """Initialize the spaceship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the spaceship image and set its rect attribute.
        self.image = pygame.image.load('images/spaceship.bmp')
        self.rect = self.image.get_rect()

        # Start each new spaceship near the top left corner of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the spaceship's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if spaceship is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the spaceship right or left."""
        self.x += (self.settings.spaceship_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x