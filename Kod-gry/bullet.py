import pygame
import os
import math

# Initialize Pygame
pygame.init()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target=None, damage=10):
        super().__init__()
        image_path = os.path.join('zdjecia', 'zombie.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8
        self.target = target
        self.damage = damage

    def update(self):
        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                dx /= distance
                dy /= distance

                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            else:
                self.kill()
        else:
            self.rect.y -= self.speed
            if self.rect.bottom < 0:
                self.kill()
class OrbitingBullet(pygame.sprite.Sprite):
    def __init__(self, character, radius, angle_speed, damage=5000):
        super().__init__()
        image_path = os.path.join('zdjecia', 'zombie.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (20, 20))
        self.rect = self.image.get_rect()
        self.character = character
        self.radius = radius
        self.angle = 0
        self.angle_speed = angle_speed
        self.damage = damage

    def update(self):
        self.angle += self.angle_speed
        self.rect.centerx = self.character.rect.centerx + self.radius * math.cos(math.radians(self.angle))
        self.rect.centery = self.character.rect.centery + self.radius * math.sin(math.radians(self.angle))

class StraightShootingBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=10, damage=10):
        super().__init__()
        image_path = os.path.join('zdjecia', 'zombie.png')
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.damage = damage

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


