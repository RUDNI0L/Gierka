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
        self.speed = speed
        self.last_attack_time = time.time()
        self.attack_delay = attack_delay

        # Ładowanie obrazków animacji ruchu
        self.walk_right_imgs = [pygame.image.load(f'{image_path}/right/right{x}.png').convert_alpha() for x in range(1, 8)]
        self.walk_left_imgs = [pygame.image.load(f'{image_path}/left/left{x}.png').convert_alpha() for x in range(1, 8)]

        self.direction = 'left'  # Początkowy kierunek animacji
        self.walk_index = 0  # Indeks aktualnie wyświetlanej klatki animacji
        self.image = self.walk_left_imgs[self.walk_index // 5]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        direction = pygame.math.Vector2(self.target.rect.center) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize()

        # Aktualizacja pozycji
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

        # Ustalanie kierunku animacji
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.direction = 'right'
            else:
                self.direction = 'left'

        # Aktualizacja animacji
        self.walk_index += 1
        if self.walk_index >= len(self.walk_right_imgs) * 5:
            self.walk_index = 0

        if self.direction == 'right':
            self.image = self.walk_right_imgs[self.walk_index // 5]
        elif self.direction == 'left':
            self.image = self.walk_left_imgs[self.walk_index // 5]

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

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
        super().__init__(x, y, max_hp=max_hp, damage=damage, image_path=os.path.join('zdjecia', 'goblin'), target=target)

class Skeleton(EnemyBase):
    def __init__(self, x, y, target, level):
        max_hp = 70 + level * 15
        damage = 15 + level * 3
        super().__init__(x, y, max_hp=max_hp, damage=damage, image_path=os.path.join('zdjecia', 'skeleton'), target=target)

class shadow(EnemyBase):
    def __init__(self, x, y, target, level):
        max_hp = 100 + level * 20
        damage = 20 + level * 4
        super().__init__(x, y, max_hp=max_hp, damage=damage, image_path=os.path.join('zdjecia', 'shadow'), target=target)

class boss(EnemyBase):
    def __init__(self, x, y, target, level):
        max_hp = 200 + level * 50
        damage = 30 + level * 10
        super().__init__(x, y, max_hp=max_hp, damage=damage, image_path=os.path.join('zdjecia', 'boss'), target=target)
