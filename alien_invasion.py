import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """A class to represent Alien Invasion Game
    Args:
        settings : represent Settings class object
        screen : screen display mode
        stats : Game stats class object
        score_board: Scoreboard class object
        ship : Ship class object
        bullets : A container class to hold and manage multiple Bullet objects
        aliens : A container class to hold and manage multiple Alien objects
        single_player : Create a Button object at the start of the game
    """
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        self.stats = GameStats(self)
        self.score_board = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._check_music()
        self._create_fleet()
        self.single_player = Button(self, self.screen, "Single Player")

    def run_game(self):
        """ Run main loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self._check_events()
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    @staticmethod
    def _check_music():
        """Play music while game starts, endless loop"""
        pygame.mixer.init()
        pygame.mixer.music.load('music/background.wav')
        pygame.mixer.music.play(-1)

    def _check_events(self):
        """React on events during the game. Check for proper system react when player want to quit the game,
        press up/down button and get mouse cursor position"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Check if mouse cursor collided with button object and clicked. If so start new game,
        initialize initial settings and reset stats. Prepare score board,
        create new alien fleet and center players ship.
        Mouse cursor set not to be visible during the game"""
        button_clicked = self.single_player.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.score_board.prep_score()
            self.score_board.prep_level()
            self.score_board.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            # hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_event(self, event):
        """Function react on pressing a keyboard key and let the spaceship move
        left or right, fire a bullet or exit the game"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Control ship left or right movement when button released"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Control number of bullets allowed for player, if any create new Bullet object,
        add it to bullets Group. Release the sound of bullet when used"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            bullet_sound = pygame.mixer.Sound('music/laser.wav')
            bullet_sound.set_volume(0.3)
            bullet_sound.play()

    def _update_bullets(self):
        """Update bullets location on the screen and deletes bullets that went over the screen to save memory"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """React on collision between alien and bullet objects. Destroy both if so.
        Update score points when collided and release explosion sound.
        If all aliens get destroyed by player, function remove existing bullet objects,
        prepare new level with updated scoreboard and increased speed"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                collision_sound = pygame.mixer.Sound('music/explosion.wav')
                collision_sound.set_volume(0.3)
                collision_sound.play()
            self.score_board.prep_score()
            self.score_board.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.score_board.prep_level()

    def _create_fleet(self):
        """Create alien object and count number of aliens to fit in one row leaving a 1 alien width
        space on each side. Calculate the numbers of rows dependable of alien object size.
        Finally, create full alien objects fleet"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create alien object and adds it to alien Group"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Check if the edge of screen is reached and change fleet direction"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Change fleet direction and move one level down if so"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Update alien objects location. Check for alien and player ship objets collision or
        if alien fleet reached the bottom of the screen for player to loose live or game"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _ship_hit(self):
        """Update player lives when reached by alien objets fleet. Reset level if player still have any lives
         left or game over when none. Game pauses for one second to get ready when live lost.
          Mouse cursor set visible for player to start new game"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.score_board.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any alien object reached bottom of the screen and reset fleet if so"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):

        self.screen.blit(self.settings.background_image, [0, 0])
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.score_board.show_score()

        if not self.stats.game_active:
            self.single_player.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
