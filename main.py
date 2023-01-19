import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height, objects):
        pygame.init()
        self.objects = objects
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    v = 0
                if event.type == pygame.KEYDOWN:
                    print(11)
                    self.key_down(event)
            self.screen.fill((0, 0, 0))
            self.render()
            pygame.display.flip()

    def render(self):
        self.sprites = pygame.sprite.Group()
        for i in objects:
            self.sprites.add(i)
        self.sprites.draw(self.screen)

    def on_click(self, cell):
        v = 0

    def add_object(self, obj):
        self.objects.append(obj)

    def key_down(self, event):
        if pygame.K_SPACE == event.key:
            self.shoot()
            return
        elif pygame.K_LEFT == event.key:
            print(11)
            self.objects[0].new_move(-5, 0)

    def shoot(self):
        c = 0


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.is_enemy = True
        if self.is_enemy:
            self.image_origin = load_image("img\\tanchik.png")
        else:
            self.image_origin = load_image("img\\tanchik.png")
        self.image = self.image_origin
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.direction = 'top'

    def new_move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if x > 0:
            self.direction = 'right'
        elif x < 0:
            self.direction = 'left'
        elif y > 0:
            self.direction = 'down'
        elif y < 0:
            self.direction = 'top'


objects = []
objects.append(Tank((50, 50)))
objects.append(Tank((100, 100)))

board = Board(700, 700, objects)
