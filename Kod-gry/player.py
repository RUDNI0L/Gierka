import os
import pygame

class PlayerBase(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, image_path):
        super().__init__()
        self.max_hp = max_hp
        self.hp = max_hp
        self.damage = damage
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def heal(self, healing):
        self.hp += healing
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class Player(PlayerBase):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=100, damage=10, image_path=os.path.join('zdjecia', 'rycerz.png'))

class Player2(PlayerBase):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=80, damage=10, image_path=os.path.join('zdjecia', 'lucznik.png'))

class Player3(PlayerBase):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=120, damage=10, image_path=os.path.join('zdjecia', 'mag.png'))

class Player4(PlayerBase):
    def __init__(self, x, y):
        super().__init__(x, y, max_hp=150, damage=10, image_path=os.path.join('zdjecia', 'wladca.png'))
