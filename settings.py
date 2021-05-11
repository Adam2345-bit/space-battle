class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (12, 20, 69)

        # Ship settings
        self.rocket_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,255,255)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 5

        # How quickly the game speeds up
        self.speedup_scale = 1.3
        # How quickly the spaceship point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.rocket_speed = 0.6
        self.bullet_speed = 2.0
        self.spaceship_speed = 0.1

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.spaceship_points = 50

    def increase_speed(self):
        """Increase speed settings and spaceship point values."""
        self.rocket_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.spaceship_speed *= self.speedup_scale

        self.spaceship_points = int(self.spaceship_points * self.score_scale)