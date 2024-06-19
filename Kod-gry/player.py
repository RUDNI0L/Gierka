import os

import pygame
from bullet import Bullet,OrbitingBullet,StraightShootingBullet
from settings import WIDTH,HEIGHT


class PlayerBase(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp, image_path):
        super().__init__()
        self.max_hp = max_hp
        self.hp = max_hp
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

        self.exp = 0
        self.level = 1
        self.exp_to_next_level = 100  # Initial XP needed for the next level

        self.bullet_damage = 10
        self.bullet_speed = 60

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        print(f"lvl:  {self.level}")
        self.on_level_up()

    def on_level_up(self):
        if self.level == 2:
            self.special_event_2()
        elif self.level == 3:
            self.special_event_3()
        elif self.level == 4:
            self.special_event_4()
        elif self.level == 5:
            self.special_event_5()
        elif self.level == 6:
            self.special_event_6()
        elif self.level == 7:
            self.special_event_7()
        elif self.level == 8:
            self.special_event_8()
        elif self.level == 9:
            self.special_event_9()
        elif self.level == 10:
            self.boss_fight()


    def special_event_2(self):
        self.bullet_damage = 50000
        pass

    def special_event_3(self): # Example: Change bullet speed and damage
        self.speed = 10
        self.bullet_damage = 20
        self.bullet_speed = 12
        print("3")

    def special_event_4(self):
        pass

    def special_event_5(self):
        pass

    def special_event_6(self):
        self.bullet_damage = 40
        self.bullet_speed = 15
        print("6")

    def special_event_7(self):
        pass

    def special_event_8(self):
        pass

    def special_event_9(self):
        self.bullet_damage = 40
        self.bullet_speed = 18
        print("9")

    def boss_fight(self):
        print("boss")

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
    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, max_hp=100, image_path='zdjecia/rycerz/right/right1.png')
        self.walk_right_imgs = [pygame.image.load(f'zdjecia/rycerz/right/right{x}.png').convert_alpha() for x in range(1, 9)]
        self.walk_left_imgs = [pygame.image.load(f'zdjecia/rycerz/left/left{x}.png').convert_alpha() for x in range(1, 9)]
        self.direction = 'right'  # Początkowy kierunek animacji
        self.walk_index = 0  # Indeks aktualnie wyświetlanej klatki animacji
        self.bullet_group = bullet_group
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = 500
        self.default_direction = "up"
        self.last_hit_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Wyświetlanie animacji
        if self.direction == 'right':
            self.image = self.walk_right_imgs[self.walk_index // 5]
        elif self.direction == 'left':
            self.image = self.walk_left_imgs[self.walk_index // 5]

        screen.blit(self.image, self.rect)

    def update(self):
        # Aktualizacja animacji na podstawie wciśniętych klawiszy
        keys = pygame.key.get_pressed()
        moved = False  # Flaga wskazująca, czy gracz się poruszył

        if keys[pygame.K_LEFT]:
            self.direction = 'left'
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'
            moved = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # Jeśli gracz się poruszył, zaktualizuj indeks animacji
        if moved:
            self.walk_index += 1
            if self.walk_index >= len(self.walk_right_imgs) * 5:
                self.walk_index = 0
        else:
            self.walk_index = 0  # Zatrzymaj animację gdy gracz stoi w miejscu

        super().update()  # Wywołanie metody update z klasy bazowej

    def shoot(self, direction=None):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.shoot_cooldown:
            return
        self.last_shot_time = current_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.last_direction = "up"
            self.last_pressed_key = pygame.K_UP
            self.default_direction = "up"
        elif keys[pygame.K_DOWN]:
            self.last_direction = "down"
            self.last_pressed_key = pygame.K_DOWN
            self.default_direction = "down"
        elif keys[pygame.K_LEFT]:
            self.last_direction = "left"
            self.last_pressed_key = pygame.K_LEFT
            self.default_direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.last_direction = "right"
            self.last_pressed_key = pygame.K_RIGHT
            self.default_direction = "right"
        direction = direction or self.default_direction

        if direction == "up":
            self.last_direction = "up"
            dx, dy = 0, -1
        elif direction == "down":
            self.last_direction = "down"
            dx, dy = 0, 1
        elif direction == "left":
            self.last_direction = "left"
            dx, dy = -1, 0
        elif direction == "right":
            self.last_direction = "right"
            dx, dy = 1, 0
        else:
            return

        bullet = StraightShootingBullet(self.rect.centerx, self.rect.centery, speed=self.bullet_speed, damage=self.bullet_damage)
        bullet.update = lambda: self.update_bullet(bullet, dx, dy)
        self.bullet_group.add(bullet)

    def update_bullet(self, bullet, dx, dy):
        bullet.rect.x += dx * bullet.speed
        bullet.rect.y += dy * bullet.speed
        if bullet.rect.right < 0 or bullet.rect.left > WIDTH or bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT:
            bullet.kill()

class Player2(PlayerBase):
    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, max_hp=100, image_path='zdjecia/lucznik/idle.png')
        self.walk_right_imgs = [pygame.image.load(f'zdjecia/lucznik/right/right{x}.png').convert_alpha() for x in
                                range(1, 9)]
        self.walk_left_imgs = [pygame.image.load(f'zdjecia/lucznik/left/left{x}.png').convert_alpha() for x in
                               range(1, 9)]
        self.direction = 'right'  # Początkowy kierunek animacji
        self.walk_index = 0  # Indeks aktualnie wyświetlanej klatki animacji
        self.bullet_group = bullet_group
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = 500
        self.default_direction = "up"
        self.last_hit_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Wyświetlanie animacji
        if self.direction == 'right':
            self.image = self.walk_right_imgs[self.walk_index // 5]
        elif self.direction == 'left':
            self.image = self.walk_left_imgs[self.walk_index // 5]

        screen.blit(self.image, self.rect)

    def update(self):
        # Aktualizacja animacji na podstawie wciśniętych klawiszy
        keys = pygame.key.get_pressed()
        moved = False  # Flaga wskazująca, czy gracz się poruszył

        if keys[pygame.K_LEFT]:
            self.direction = 'left'
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'
            moved = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # Jeśli gracz się poruszył, zaktualizuj indeks animacji
        if moved:
            self.walk_index += 1
            if self.walk_index >= len(self.walk_right_imgs) * 5:
                self.walk_index = 0
        else:
            self.walk_index = 0  # Zatrzymaj animację gdy gracz stoi w miejscu

        super().update()  # Wywołanie metody update z klasy bazowej

    def shoot(self, target):
        bullet = Bullet(self.rect.centerx, self.rect.centery, target=target, damage=self.bullet_damage, speed=self.bullet_speed)
        self.bullet_group.add(bullet)

class Player3(PlayerBase):
    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, max_hp=100, image_path='zdjecia/mag/right/right1.png')
        self.walk_right_imgs = [pygame.image.load(f'zdjecia/mag/right/right{x}.png').convert_alpha() for x in
                                range(1, 7)]
        self.walk_left_imgs = [pygame.image.load(f'zdjecia/mag/left/left{x}.png').convert_alpha() for x in
                               range(1, 7)]
        self.direction = 'right'  # Początkowy kierunek animacji
        self.walk_index = 0  # Indeks aktualnie wyświetlanej klatki animacji
        self.bullet_group = bullet_group
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = 500
        self.default_direction = "up"
        self.last_hit_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Wyświetlanie animacji
        if self.direction == 'right':
            self.image = self.walk_right_imgs[self.walk_index // 5]
        elif self.direction == 'left':
            self.image = self.walk_left_imgs[self.walk_index // 5]

        screen.blit(self.image, self.rect)

    def update(self):
        # Aktualizacja animacji na podstawie wciśniętych klawiszy
        keys = pygame.key.get_pressed()
        moved = False  # Flaga wskazująca, czy gracz się poruszył

        if keys[pygame.K_LEFT]:
            self.direction = 'left'
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'
            moved = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # Jeśli gracz się poruszył, zaktualizuj indeks animacji
        if moved:
            self.walk_index += 1
            if self.walk_index >= len(self.walk_right_imgs) * 5:
                self.walk_index = 0
        else:
            self.walk_index = 0  # Zatrzymaj animację gdy gracz stoi w miejscu

        super().update()  # Wywołanie metody update z klasy bazowej

    def create_orbiting_bullet(self):
        bullet = Orbitingbullet = OrbitingBullet(self, radius=100, angle_speed=5, damage=self.bullet_damage)
        self.bullet_group.add(bullet)

class Player4(PlayerBase):
    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, max_hp=100, image_path='zdjecia/rycerz/right/right1.png')
        self.walk_right_imgs = [pygame.image.load(f'zdjecia/rycerz/right/right{x}.png').convert_alpha() for x in
                                range(1, 9)]
        self.walk_left_imgs = [pygame.image.load(f'zdjecia/rycerz/left/left{x}.png').convert_alpha() for x in
                               range(1, 9)]
        self.direction = 'right'  # Początkowy kierunek animacji
        self.walk_index = 0  # Indeks aktualnie wyświetlanej klatki animacji
        self.bullet_group = bullet_group
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_cooldown = 500
        self.default_direction = "up"
        self.last_hit_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Wyświetlanie animacji
        if self.direction == 'right':
            self.image = self.walk_right_imgs[self.walk_index // 5]
        elif self.direction == 'left':
            self.image = self.walk_left_imgs[self.walk_index // 5]

        screen.blit(self.image, self.rect)

    def update(self):
        # Aktualizacja animacji na podstawie wciśniętych klawiszy
        keys = pygame.key.get_pressed()
        moved = False  # Flaga wskazująca, czy gracz się poruszył

        if keys[pygame.K_LEFT]:
            self.direction = 'left'
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'
            moved = True

        # Jeśli gracz się poruszył, zaktualizuj indeks animacji
        if moved:
            self.walk_index += 1
            if self.walk_index >= len(self.walk_right_imgs) * 5:
                self.walk_index = 0
        else:
            self.walk_index = 0  # Zatrzymaj animację gdy gracz stoi w miejscu

        super().update()  # Wywołanie metody update z klasy bazowej

    def shoot(self, target):
        bullet = Bullet(self.rect.centerx, self.rect.centery, target=target, damage=self.bullet_damage, speed=self.bullet_speed)
        self.bullet_group.add(bullet)