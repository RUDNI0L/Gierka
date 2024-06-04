import os

import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK
from player import Player, Player2, Player3, Player4


class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        self.font_main = pygame.font.Font(None, 65)
        self.font_highlight = pygame.font.Font(None, 75)
        self.stage = "main"  # "main" lub "character"
        self.menu_items = ["Start", "Exit"]
        self.character_items = ["Rynerz", "Łucznik", "Mag", "Władca"]
        self.selected_item = 0
        self.background = pygame.image.load('zdjecia/background2.png').convert()
        desired_width, desired_height = self.screen.get_size()
        self.background = pygame.transform.scale(self.background, (desired_width, desired_height))
        pygame.mixer.init()
        pygame.mixer.music.load('muzyka/menu.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)


        # Load character images
        self.character_images = [
            pygame.transform.scale(pygame.image.load(os.path.join("zdjecia", "rycerz.png")), (64, 64)),
            pygame.transform.scale(pygame.image.load(os.path.join("zdjecia", "zombie.png")), (64, 64)),
            pygame.transform.scale(pygame.image.load(os.path.join("zdjecia", "rycerz.png")), (64, 64)),
            pygame.transform.scale(pygame.image.load(os.path.join("zdjecia", "rycerz.png")), (64, 64)),
        ]
    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, 0))

        if self.stage == "main":
            for idx, item in enumerate(self.menu_items):
                if idx == self.selected_item:
                    font = self.font_highlight
                    color = WHITE
                else:
                    font = self.font_main
                    color = (100, 100, 100)
                text = font.render(item, True, color)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + idx * 100))
                self.screen.blit(text, text_rect)
        elif self.stage == "character":
            spacing = WIDTH // (len(self.character_items) + 1)
            for idx, item in enumerate(self.character_items):
                color = WHITE if idx == self.selected_item else (100, 100, 100)
                text = self.font_main.render(item, True, color)
                text_rect = text.get_rect(center=(spacing * (idx + 1), HEIGHT // 2 - 50))
                self.screen.blit(text, text_rect)

                # Draw character image
                image = self.character_images[idx]
                image_rect = image.get_rect(center=(spacing * (idx + 1), HEIGHT // 2 + 50))
                self.screen.blit(image, image_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.game.running = False
            if event.type == pygame.QUIT:
                self.running = False
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if self.stage == "main":
                    if event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                    elif event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item == 0:  # Start
                            self.stage = "character"
                            self.selected_item = 0
                        elif self.selected_item == 1:  # Exit
                            self.running = False
                            self.game.running = False
                elif self.stage == "character":
                    if event.key == pygame.K_LEFT:
                        self.selected_item = (self.selected_item - 1) % len(self.character_items)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_item = (self.selected_item + 1) % len(self.character_items)
                    elif event.key == pygame.K_RETURN:
                        self.game.character = [Player, Player2, Player3, Player4][self.selected_item]
                        self.running = False
