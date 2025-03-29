import pygame
from pygame.sprite import Sprite
class Ship(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def move_right(self):
        if self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            self.rect.x = self.x

    def move_left(self):
        if self.rect.left > 0:
            self.x -= self.settings.ship_speed
            self.rect.x = self.x
            
    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
