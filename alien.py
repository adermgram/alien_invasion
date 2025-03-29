import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    """A class to represent a single alien in a fleet. """
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen


        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()


        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.settings = ai_game.settings
        
    def update(self):
        """Move the alien to the left or right. """
        
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)

        self.rect.x = self.x

        

    def check_edges(self):
        """Return True if alien is at edge of the screen."""

        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True

            
