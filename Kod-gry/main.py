import pygame
import sys
import random
import time
from settings import WIDTH, HEIGHT, FPS, BLACK
from player import Player, Player2, Player3, Player4
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
            self.player.gain_exp(10)
            self.kill()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vampire Survivors Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.character = Player  # Możesz ustawić domyślną postać tutaj

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
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        self.quit()

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
                elif isinstance(self.player, Player4):
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
                if hit.hp <= 0:  # jak wrog zabity
                    exp_orb = Experience(hit.rect.centerx, hit.rect.centery, self.player)
                    self.all_sprites.add(exp_orb)
                    self.exp.add(exp_orb)
                    hit.kill()

        # kolizja gracz-wrog
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            if enemy.can_attack():
                self.player.take_damage(enemy.damage)

        if self.player.hp <= 0:
            self.running = False

        self.check_player_level()
        self.update_spawn_rate_based_on_level()
        self.increase_enemies()

    def check_player_level(self):
        if self.player.level == 3:
            self.spawn_special_enemies(level=3)
        elif self.player.level == 6:
            self.spawn_special_enemies(level=6)
        elif self.player.level == 9:
            self.spawn_special_enemies(level=9)
        elif self.player.level == 10:
            self.spawn_boss()

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
        elif level == 9 and current_special_enemies < max_special_enemies:
            additional_special_enemies = min(5, max_special_enemies - current_special_enemies)
            for _ in range(additional_special_enemies):
                enemy = self.spawn_enemy(boss)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def spawn_boss(self):
        if not any(isinstance(enemy, Boss) for enemy in self.enemies):
            boss_enemy = self.spawn_enemy(Boss)
            self.all_sprites.add(boss_enemy)
            self.enemies.add(boss_enemy)

    def set_enemy_increase_interval(self, interval):
        self.enemy_increase_interval = interval

    def draw_time(self):
        elapsed_time = int(time.time() - self.start_time)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
        self.screen.blit(text, (WIDTH - 150, HEIGHT - 50))

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
        pygame.display.flip()

    def draw_hp_bar(self, hp, max_hp, x, y, width, height):
        ratio = hp / max_hp
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, width, height))
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, width * ratio, height))

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    if game.running:
        game.run()
    game.quit()

