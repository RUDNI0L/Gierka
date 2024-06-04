import pygame
import sys
import random
from settings import WIDTH, HEIGHT, FPS, BLACK
from player import Player, Player2, Player3, Player4
from enemy import Enemy
from menu import Menu

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

        # Inicjalizacja Pygame Mixer i załadowanie muzyki
        pygame.mixer.init()
        pygame.mixer.music.load('muzyka/muzyka1.mp3')
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)

        if self.running:
            self.new_game()

    def new_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = self.character(WIDTH // 2, HEIGHT // 2)
        self.all_sprites.add(self.player)

        for _ in range(10):
            enemy = Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()

        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
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