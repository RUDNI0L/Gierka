import os
import pygame
from settings import *
import random
from player import Player, Player2, Player3, Player4

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        image_path = os.path.join('zdjecia', 'zombie.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.target = target

    def update(self):
        direction = pygame.Vector2(self.target.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        self.rect.move_ip(direction)