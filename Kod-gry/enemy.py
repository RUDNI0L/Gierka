import pygame
from settings import *
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        self.rect.x += random.choice([-1, 1]) * self.speed
        self.rect.y += random.choice([-1, 1]) * self.speed