import random

import pygame
import os
import sys
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.timeout = 50
        self.time = 0

    def run(self):
        running = True
        while running:
            self.time += self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    v = 0
            self.actions()
            self.screen.fill((0, 0, 0))
            self.render()
            pygame.display.flip()

    def set_objects(self, objects):
        self.objects = objects
        for i in self.objects:
            if hasattr(i, 'set_board'):
                i.set_board(self)

    def render(self):
        self.sprites = pygame.sprite.Group()
        for i in objects:
            self.sprites.add(i)
        self.sprites.draw(self.screen)

    def actions(self):
        for i in self.objects:
            if hasattr(i, 'add_shoot_ready'):
                i.add_shoot_ready()
        if self.time > self.timeout:
            self.time = 0
        else:
            return
        keys = pygame.key.get_pressed()
        self.key_down(keys)
        for i in self.objects:
            if hasattr(i, 'auto_action'):
                i.auto_action()

    def on_click(self, cell):
        v = 0

    def add_object(self, obj):
        self.objects.append(obj)
        obj.set_board(self)

    def key_down(self, keys):
        if keys[pygame.K_SPACE]:
            self.shoot()
            return
        elif keys[pygame.K_LEFT]:
            self.objects[0].new_move(-self.objects[0].speed, 0)
        elif keys[pygame.K_RIGHT]:
            self.objects[0].new_move(self.objects[0].speed, 0)
        elif keys[pygame.K_UP]:
            self.objects[0].new_move(0, -self.objects[0].speed)
        elif keys[pygame.K_DOWN]:
            self.objects[0].new_move(0, self.objects[0].speed)


    def shoot(self):
        self.objects[0].shoot()

    def get_char(self):
        return self.objects[0]

    def remove(self, obj):
        # index = self.objects.index(obj)
        self.objects.remove(obj)


class Position:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def add_x(self, x):
        self.x += x

    def add_y(self, y):
        self.y += y


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, is_enemy=True):
        super().__init__()
        self.width = 50
        self.height = 50
        self.is_enemy = is_enemy
        if self.is_enemy:
            self.image_origin = load_image("enemy.jpg")
        else:
            self.image_origin = load_image("character.jpg")
        self.image = self.image_origin
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.width // 2
        self.rect.y = pos[1] - self.height // 2

        self.pos = Position(pos)

        self.speed = 5
        self.time_to_shoot = 1500
        self.shoot_ready = 0

        self.direction = 'top'

    def set_board(self, board):
        self.board = board

    def set_pos_x(self, x):
        self.pos.set_x(x)
        self.rect.x = x - self.width // 2

    def set_pos_y(self, y):
        self.pos.set_y(y)
        self.rect.y = y - self.height // 2

    def new_move(self, x, y):
        if self.width // 2 <= self.pos.x + x <= self.board.width - self.width // 2:
            self.set_pos_x(self.pos.x + x)
        if self.height // 2 <= self.pos.y + y <= self.board.height - self.height // 2:
            self.set_pos_y(self.pos.y + y)
        if x > 0:
            self.direction = 'left'
        elif x < 0:
            self.direction = 'right'
        elif y > 0:
            self.direction = 'down'
        elif y < 0:
            self.direction = 'top'
        self.change_direction()

    def auto_action(self):
        if not self.is_enemy:
            return
        char = self.board.get_char()
        x = char.pos.x - self.pos.x
        y = char.pos.y - self.pos.y

        xm = abs(x)
        ym = abs(y)

        if (xm ** 2 + ym ** 2) ** 0.5 < 45:
            pygame.quit()
        # if xm > ym:
        #     self.new_move(0, self.speed * (1 if x > 0 else -1))
        # elif xm < ym:
        #     self.new_move(self.speed * (1 if y > 0 else -1), 0)
        if xm < self.width // 2 or ym < self.height // 2:
            self.shoot()

    def shoot(self):
        if self.shoot_ready < self.time_to_shoot:
            return
        self.shoot_ready = 0
        bul = Bullet((self.pos.x, self.pos.y), self.direction, self.is_enemy)
        self.board.add_object(bul)

    def add_shoot_ready(self):
        self.shoot_ready += 1

    def die(self):
        self.board.remove(self)

    def change_direction(self):
        d = 0
        if self.direction == 'left':
            d = -90
        elif self.direction == 'right':
            d = 90
        elif self.direction == 'down':
            d = 180
        self.image = pygame.transform.rotate(self.image_origin, d)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, dir, is_enemy=True):
        super().__init__()
        self.width = 20
        self.height = 20
        self.is_enemy = is_enemy
        if self.is_enemy:
            self.image_origin = load_image("bullet.png")
        else:
            self.image_origin = load_image("bullet.png")
        self.image = self.image_origin
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.width // 2
        self.rect.y = pos[1] - self.height // 2

        self.pos = Position(pos)

        self.direction = dir

        self.speed = 30

    def set_board(self, board):
        self.board = board

    def set_pos_x(self, x):
        self.pos.set_x(x)
        self.rect.x = x - self.width // 2

    def set_pos_y(self, y):
        self.pos.set_y(y)
        self.rect.y = y - self.height // 2

    def auto_action(self):
        if self.direction == 'top':
            self.set_pos_y(self.pos.y - self.speed)
        elif self.direction == 'down':
            self.set_pos_y(self.pos.y + self.speed)
        elif self.direction == 'left':
            self.set_pos_x(self.pos.x + self.speed)
        elif self.direction == 'right':
            self.set_pos_x(self.pos.x - self.speed)

        objects = self.board.objects
        for i in objects:
            if self.is_enemy != i.is_enemy:
                x = abs(self.pos.x - i.pos.x)
                y = abs(self.pos.y - i.pos.y)
                if (x ** 2 + y ** 2) ** 0.5 < 25:
                    i.die()
                    self.die()
                    break
        if self.pos.x < 0 or self.pos.x > self.board.width or self.pos.y < 0 or self.pos.y > self.board.height:
            self.die()

    def die(self):
        self.board.remove(self)







objects = []
objects.append(Tank((50, 50), is_enemy=False))
objects.append(Tank((100, 100)))
objects.append(Tank((300, 570)))

board = Board(700, 700)
board.set_objects(objects)
board.run()
