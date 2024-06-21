import os

import pygame
import sys
import random
import time
from settings import WIDTH, HEIGHT, FPS, BLACK, WHITE
from player import Player, Player2, Player3
from enemy import Zombie, Skeleton, shadow, boss
from menu import Menu
from bullet import Bullet, OrbitingBullet, StraightShootingBullet
import math

SHOOT_EVENT = pygame.USEREVENT + 1

class Experience(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0  # Można usunąć, ponieważ nie będziemy używać prędkości
        self.player = player  # Przechowujemy obiekt player

    def update(self):
        if self.rect.colliderect(self.player.rect):
            if self.player.level < 9:
                self.player.gain_exp(10)
                self.kill()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vampire Survivors Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.character = None  # Możesz ustawić domyślną postać tutaj

        self.menu = Menu(self)
        self.menu.run()

        pygame.mixer.init()

        self.music_files = ['muzyka/muzyka1.mp3', 'muzyka/muzyka2.mp3', 'muzyka/muzyka3.mp3']
        pygame.mixer.music.set_volume(0.01)
        self.play_random_music()

        self.background = pygame.image.load('zdjecia/background.png').convert()

        self.last_enemy_increase_time = time.time()
        self.enemy_spawn_interval = 60  # co ile sekund zwiększać liczbę wrogów
        self.enemy_increase_interval = 10  # co ile sekund spawnić wrogów
        self.enemy_increase_amount = 5  # o ile zwiększyć liczbę wrogów

        self.start_time = time.time()

        if self.running:
            self.new_game()

    def play_random_music(self):
        try:
            selected_music = random.choice(self.music_files)
            pygame.mixer.music.load(selected_music)
            pygame.mixer.music.play(-1)
            print(f"Playing: {selected_music}")
        except pygame.error as e:
            print(f"Could not load music: {e}")

    def new_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.exp = pygame.sprite.Group()

        # Inicjalizacja gracza z grupą pocisków
        self.player = self.character(WIDTH // 2, HEIGHT // 2, self.bullets)
        self.all_sprites.add(self.player)

        for _ in range(10):
            enemy = self.spawn_enemy(Zombie)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        pygame.time.set_timer(SHOOT_EVENT, 1000)

    def spawn_enemy(self, enemy_type):
        spawn_position = random.choice(['top', 'bottom', 'left', 'right'])
        if spawn_position == 'top':
            x = random.randint(-50, WIDTH + 50)
            y = -50
        elif spawn_position == 'bottom':
            x = random.randint(-50, WIDTH + 50)
            y = HEIGHT + 50
        elif spawn_position == 'left':
            x = -50
            y = random.randint(-50, HEIGHT + 50)
        elif spawn_position == 'right':
            x = WIDTH + 50
            y = random.randint(-50, HEIGHT + 50)
        return enemy_type(x, y, self.player, self.player.level)

    def update_spawn_rate_based_on_level(self):
        if self.player.level == 1:
            self.enemy_increase_interval = 4
        elif self.player.level == 2:
            self.enemy_increase_interval = 5
        elif self.player.level == 3:
            self.enemy_increase_interval = 2
        elif self.player.level == 4:
            self.enemy_increase_interval = 3
        elif self.player.level >= 5:
            self.enemy_increase_interval = 2

    def increase_enemies(self):
        current_time = time.time()
        if current_time - self.last_enemy_increase_time >= self.enemy_increase_interval:
            self.last_enemy_increase_time = current_time

            # respienie sie mobow od poziomu
            max_enemies = self.player.level * 10

            if len(self.enemies) < max_enemies:
                additional_enemies = min(self.enemy_increase_amount, max_enemies - len(self.enemies))
                for _ in range(additional_enemies):
                    enemy = self.spawn_enemy(Zombie)
                    self.all_sprites.add(enemy)
                    self.enemies.add(enemy)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        # Show game over screen
        self.game_over_screen()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == SHOOT_EVENT:
                if isinstance(self.player, Player3):
                    self.player.create_orbiting_bullet()
                elif isinstance(self.player, Player2):
                    if self.enemies:
                        target = random.choice(self.enemies.sprites())
                        self.player.shoot(target)
        keys = pygame.key.get_pressed()
        if isinstance(self.player, Player):
            if keys[pygame.K_UP]:
                self.player.shoot("up")
            elif keys[pygame.K_DOWN]:
                self.player.shoot("down")
            elif keys[pygame.K_LEFT]:
                self.player.shoot("left")
            elif keys[pygame.K_RIGHT]:
                self.player.shoot("right")
            else:
                self.player.shoot()

    def update(self):
        self.all_sprites.update()
        self.bullets.update()

        # kolizja pocisk-wrog
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for hit in hits:
                hit.take_damage(bullet.damage)
                bullet.kill()
                if self.player.level < 9:
                    if hit.hp <= 0:  # jak wrog zabity
                        exp_orb = Experience(hit.rect.centerx, hit.rect.centery, self.player)
                        self.all_sprites.add(exp_orb)
                        self.exp.add(exp_orb)
                        hit.kill()
                else:  # jeśli poziom >= 9
                    if hit.hp <= 0:
                        hit.kill()
                        if isinstance(hit, boss):
                            if self.player.level == 9:
                                self.player.level = 10
                                self.spawn_boss(scale=3)  # Duży boss
                            elif self.player.level == 10:
                                self.running = False  # Zamiast self.quit() ustawiamy self.running na False, żeby wywołać ekran końcowy

        # kolizja gracz-wrog
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            if enemy.can_attack():
                self.player.take_damage(enemy.damage)

        if self.player.hp <= 0:
            self.running = False

        self.check_player_level()  # Sprawdź poziom gracza po każdej aktualizacji
        self.update_spawn_rate_based_on_level()
        if self.player.level < 9:
            self.increase_enemies()

    def is_boss_alive(self):
        return any(isinstance(enemy, boss) for enemy in self.enemies)

    def check_player_level(self):
        if self.player.level == 3:
            self.spawn_special_enemies(level=3)
        elif self.player.level == 6:
            self.spawn_special_enemies(level=6)
        elif self.player.level == 9:
            if len(self.enemies) == 0:  # Sprawdź, czy wszystkie wrogie jednostki zostały zabite
                self.spawn_boss(scale=1)  # Mały boss
                self.enemy_increase_interval = float('inf')  # Zatrzymaj respawn zwykłych wrogów

        elif self.player.level == 10:
            if len(self.enemies) == 0:  # Sprawdź, czy wszystkie wrogie jednostki zostały zabite
                self.spawn_boss(scale=2.5)  # Duży boss
                self.enemy_increase_interval = float('inf')  # Zatrzymaj respawn zwykłych wrogów

    def spawn_boss(self, scale=1.0):
        if not any(isinstance(enemy, boss) for enemy in self.enemies):
            boss_enemy = boss(WIDTH // 2, HEIGHT // 2, self.player, self.player.level, scale=scale)
            self.all_sprites.add(boss_enemy)
            self.enemies.add(boss_enemy)

    def spawn_special_enemies(self, level):
        max_special_enemies = self.player.level * 15  # dostosowaniue
        current_special_enemies = len([enemy for enemy in self.enemies if isinstance(enemy, (Skeleton, shadow, boss))])

        if level == 3 and current_special_enemies < max_special_enemies:
            additional_special_enemies = min(5, max_special_enemies - current_special_enemies)
            for _ in range(additional_special_enemies):
                enemy = self.spawn_enemy(Skeleton)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
        elif level == 6 and current_special_enemies < max_special_enemies:
            additional_special_enemies = min(5, max_special_enemies - current_special_enemies)
            for _ in range(additional_special_enemies):
                enemy = self.spawn_enemy(shadow)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def draw_time(self):
        elapsed_time = int(time.time() - self.start_time)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
        self.screen.blit(text, (WIDTH - 150, HEIGHT - 50))

    def draw_boss_hp_bar(self, hp, max_hp, x, y, width, height):
        ratio = hp / max_hp
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, width, height))
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, width * ratio, height))

    def draw_xp(self):
        font = pygame.font.Font(None, 36)
        xp_text = font.render(f"XP: {self.player.exp}/{self.player.exp_to_next_level}", True, (255, 255, 255))
        level_text = font.render(f"Level: {self.player.level}", True, (255, 255, 255))
        self.screen.blit(xp_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

    def draw(self):
        for x in range(0, WIDTH, self.background.get_width()):
            for y in range(0, HEIGHT, self.background.get_height()):
                self.screen.blit(self.background, (x, y))
        self.player.draw(self.screen)  # Rysowanie animacji dla gracza 1
        self.all_sprites.draw(self.screen)
        self.bullets.draw(self.screen)
        self.exp.draw(self.screen)  # Dodajemy rysowanie obiektów doświadczenia
        self.draw_time()
        self.draw_xp()
        self.draw_hp_bar(self.player.hp, self.player.max_hp, 10, 80, 200, 20)

        # sprawdza czy bos jest i pasek robi
        boss_enemy = next((enemy for enemy in self.enemies if isinstance(enemy, boss)), None)
        if boss_enemy:
            self.draw_boss_hp_bar(boss_enemy.hp, boss_enemy.max_hp, WIDTH // 2 - 150, 10, 300, 20)

        pygame.display.flip()

    def draw_hp_bar(self, hp, max_hp, x, y, width, height):
        ratio = hp / max_hp
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, width, height))
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, width * ratio, height))

    def game_over_screen(self):
        elapsed_time = int(time.time() - self.start_time)
        font_main = pygame.font.Font(None, 65)
        font_highlight = pygame.font.Font(None, 75)
        menu_items = ["Play Again", "Exit"]
        selected_item = 0

        in_game_over_screen = True
        while in_game_over_screen:
            self.screen.fill(BLACK)
            self.display_text('GAME OVER', font_main, WHITE, self.screen, WIDTH // 2 - 100, HEIGHT // 4)
            self.display_text(f'Time: {elapsed_time} seconds', font_main, WHITE, self.screen, WIDTH // 2 - 150,
                              HEIGHT // 3)

            for idx, item in enumerate(menu_items):
                if idx == selected_item:
                    text = font_highlight.render(item, True, WHITE)
                else:
                    text = font_main.render(item, True, WHITE)
                self.screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 + idx * 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_item = (selected_item - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        if selected_item == 0:  # Play Again
                            in_game_over_screen = False  # Przerwij pętlę game_over_screen
                            self.reset_game()  # Wywołaj funkcję reset_game
                        elif selected_item == 1:  # Exit
                            self.running = False
                            pygame.quit()
                            sys.exit()

    def reset_game(self):
        print("Resetting game")  # Debugging message
        self.character = None
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.exp.empty()
        self.start_time = time.time()
        self.menu.run()
        if self.character is not None:
            self.new_game()
            self.run()  # Uruchom ponownie grę
        else:
            print("Character not selected, returning to menu")  # Debugging message

    def quit(self):
        pygame.quit()
        sys.exit()

    @staticmethod
    def display_text(text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

if __name__ == "__main__":
    game = Game()
    if game.running:
        game.run()
    game.quit()

