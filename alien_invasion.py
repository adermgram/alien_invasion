import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from  game_stats import  GameStats
from button import Button
from scoreboard import Scoreboard
        
class AlienInvasion:
    """Overall class to handle game assets and behaviour. """
    def __init__(self):
        "Initialize the game, and create game resources."
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")


        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
    
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")
        

    def _create_fleet(self):
        """make the fleet of aliens """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)


        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)




    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.ship.move_left()
        if keys[pygame.K_RIGHT]:
            self.ship.move_right()
            
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if button_clicked and not self.stats.game_active:
            #Reset the game statistics.
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.settings.initialize_dynamic_settings()

            self.aliens.empty()
            self.bullets.empty()
            
            self._create_fleet()
            self.ship.center_ship
                   
    def _ship_hit(self):
        """ Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            

            #Decrement ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of any remaining aliens  and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group. """
        if len(self.bullets) <self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)




    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen) 
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()


        pygame.display.flip()


    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        
    
    def _check_bullet_alien_collisions(self):
 
        #Check for any bullet that hits aliens and get rid of both the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet() 

            self.settings.increase_speed()

            #Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def run_game(self):
        """Start the main loop of the game."""

        while True:
            self._check_events()
            
            if self.stats.game_active:
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        
        #look for alien-ship collison.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        #look for aliens hitting the buttom of the screen.
        self._check_aliens_bottom()
        
            

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():

            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction. """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
            



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    
