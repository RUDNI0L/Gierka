import pygame
import sys
import random
from settings import WIDTH, HEIGHT, FPS, BLACK  # Importowanie stałych z pliku settings
from player import Player
from enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Poprawka na set_mode
        pygame.display.set_caption("Vampire Survivors Clone")
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.all_sprites.add(self.player)

        for _ in range(10):
            enemy = Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            self.all_sprites.add(enemy)  # Poprawka na all_sprites
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
        self.all_sprites.update()  # Poprawka na all_sprites

        # Sprawdzanie kolizji między graczem a przeciwnikami
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.running = False  # Zatrzymanie gry po kolizji

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)  # Poprawka na all_sprites
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
    game.quit()
