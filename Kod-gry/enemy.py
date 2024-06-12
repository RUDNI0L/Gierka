import os
import time
import pygame

class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, damage, image_path, target, speed=3, attack_delay=1.0):
        super().__init__()
        self.max_hp = max_hp
        self.hp = max_hp
        self.damage = damage
        self.target = target
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_attack_time = time.time()
        self.attack_delay = attack_delay
        self.speed = speed

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def update(self):
        direction = pygame.math.Vector2(self.target.rect.center) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

    def can_attack(self):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_delay:
            self.last_attack_time = current_time
            return True
        return False

class Zombie(EnemyBase):
    def __init__(self, x, y, target, level):
        max_hp = 50 + level * 10
        damage = 10 + level * 2
        super().__init__(x, y, max_hp=max_hp, damage=damage, image_path=os.path.join('zdjecia', 'zombie.png'), target=target)

class Skeleton(EnemyBase):
    def __init__(self, x, y, target, level):
        max_hp = 30 + level * 8
        damage = 15 + level * 3
        super().__init__(x, y, max_hp=max_hp, damage=damage, image_path=os.path.join('zdjecia', 'rycerz.png'), target=target)

class shadow(EnemyBase):
    def __init__(self, x, y, target, level):
        max_hp = 30 + level * 6
        damage = 15 + level * 4
        super().__init__(x, y, max_hp=max_hp, damage=damage, image_path=os.path.join('zdjecia', 'rycerz.png'), target=target)

class boss(EnemyBase):
    def __init__(self, x, y, target, level):
        max_hp = 100 + level * 20
        damage = 20 + level * 5
        super().__init__(x, y, max_hp=max_hp, damage=damage, image_path=os.path.join('zdjecia', 'zombie.png'), target=target)
