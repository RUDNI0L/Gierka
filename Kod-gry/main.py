import pygame
import sys
import random
from settings import WIDTH, HEIGHT, FPS, BLACK
from player import Player, Player2, Player3, Player4
from enemy import Zombie, Skeleton
from menu import Menu
from bullet import Bullet

SHOOT_EVENT = pygame.USEREVENT + 1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vampire Survivors Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.character = Player

        self.menu = Menu(self)
        self.menu.run()

        pygame.mixer.init()

        self.music_files = ['muzyka/muzyka1.mp3', 'muzyka/muzyka2.mp3', 'muzyka/muzyka3.mp3']
        pygame.mixer.music.set_volume(0.01)
        self.play_random_music()

        self.background = pygame.image.load('zdjecia/background.jpg').convert()

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
        self.player = self.character(WIDTH // 2, HEIGHT // 2)
        self.all_sprites.add(self.player)
        for _ in range(1):
            enemy = self.spawn_enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        pygame.time.set_timer(SHOOT_EVENT, 1000)

    def spawn_enemy(self):
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
        return Zombie(x, y, self.player)

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
                if self.enemies:
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, target=random.choice(self.enemies.sprites()))
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)

    def update(self):
        self.all_sprites.update()

        # kolizja pocisk-wrog
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for hit in hits:
                hit.take_damage(bullet.damage)
                bullet.kill()

        # kolizja
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            if enemy.can_attack():
                self.player.take_damage(enemy.damage)

        if self.player.hp <= 0:
            self.running = False

    def draw(self):
        for x in range(0, WIDTH, self.background.get_width()):
            for y in range(0, HEIGHT, self.background.get_height()):
                self.screen.blit(self.background, (x, y))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    if game.running:
        game.run()
    game.quit()
