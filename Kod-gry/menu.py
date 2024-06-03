import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK
from player import Player, Player2, Player3, Player4

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        self.font = pygame.font.Font(None, 74)
        self.stage = "main"  # "main" lub "character"
        self.menu_items = ["Start", "Exit"]
        self.character_items = ["Character 1", "Character 2", "Character 3", "Character 4"]
        self.selected_item = 0

    def draw(self):
        self.screen.fill(BLACK)
        if self.stage == "main":
            for idx, item in enumerate(self.menu_items):
                color = WHITE if idx == self.selected_item else (100, 100, 100)
                text = self.font.render(item, True, color)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + idx * 100))
                self.screen.blit(text, text_rect)
        elif self.stage == "character":
            for idx, item in enumerate(self.character_items):
                color = WHITE if idx == self.selected_item else (100, 100, 100)
                text = self.font.render(item, True, color)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + idx * 100))
                self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    if self.stage == "main":
                        if self.selected_item == 0:  # Start
                            self.stage = "character"
                            self.selected_item = 0
                            self.menu_items = self.character_items
                        elif self.selected_item == 1:  # Exit
                            self.running = False
                            self.game.running = False
                    elif self.stage == "character":
                        self.game.character = [Player, Player2, Player3, Player4][self.selected_item]
                        self.running = False
