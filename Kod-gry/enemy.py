import os

import pygame
from settings import *
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image_path = os.path.join('zdjecia', 'zombie.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 50))  # Zmień wymiary zgodnie z potrzebą
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        self.rect.x += random.choice([-1, 1]) * self.speed
        self.rect.y += random.choice([-1, 1]) * self.speed