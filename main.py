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
        c = 0

    def get_char(self):
        return self.objects[0]


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, is_enemy=True):
        super().__init__()
        self.is_enemy = is_enemy
        if self.is_enemy:
            self.image_origin = load_image("enemy.jpg")
        else:
            self.image_origin = load_image("character.jpg")
        self.image = self.image_origin
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.width = 50
        self.height = 50

        self.speed = 5

        self.direction = 'top'

    def set_board(self, board):
        self.board = board

    def new_move(self, x, y):
        if self.width // 2 <= self.rect.x + x + self.width // 2 <= self.board.width - self.width // 2:
            self.rect.x += x
        if self.height // 2 <= self.rect.y + y + self.height // 2 <= self.board.height - self.height // 2:
            self.rect.y += y
        if x > 0:
            self.direction = 'right'
        elif x < 0:
            self.direction = 'left'
        elif y > 0:
            self.direction = 'top'
        elif y < 0:
            self.direction = 'down'
        self.change_direction()

    def auto_action(self):
        if not self.is_enemy:
            return
        char = self.board.get_char()
        x = char.rect.x - self.rect.x
        y = char.rect.y - self.rect.y
        xm = abs(x)
        ym = abs(y)
        if xm > ym:
            self.new_move(0, self.speed * (1 if x > 0 else -1))
        else:
            self.new_move(self.speed * (1 if y > 0 else -1), 0)

    def change_direction(self):
        d = 0
        if self.direction == 'left':
            d = -90
        elif self.direction == 'right':
            d = 90
        elif self.direction == 'down':
            d = 180
        self.image = pygame.transform.rotate(self.image_origin, d)


objects = []
objects.append(Tank((50, 50), is_enemy=False))
objects.append(Tank((100, 100)))
objects.append(Tank((300, 570)))

board = Board(700, 700)
board.set_objects(objects)
board.run()
