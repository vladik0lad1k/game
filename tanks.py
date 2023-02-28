import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.timeout = 50
        self.time = 0

    def run(self):
        self.running = True
        self.is_win = False
        self.is_pause = False
        while self.running:
            self.time += self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_win = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    v = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_pause = not self.is_pause
                        if self.is_pause:
                            self.pause = Pause((350, 350))
                            self.add_object(self.pause)
                        else:
                            self.pause.die()
            if not self.is_pause:
                self.actions()
            self.screen.fill((0, 0, 0))
            self.render()
            pygame.display.flip()
        pygame.display.quit()
        return self.is_win

    def set_objects(self, objects):
        self.objects = objects
        for i in self.objects:
            if hasattr(i, 'set_board'):
                i.set_board(self)

    def render(self):
        self.sprites = pygame.sprite.Group()
        for i in self.objects:
            self.sprites.add(i)
        self.sprites.draw(self.screen)

    def actions(self):
        count_enemies = 0
        for i in self.objects:
            if hasattr(i, 'is_enemy'):
                if i.is_enemy:
                    count_enemies += 1
        if count_enemies == 0:
            self.is_win = True
            self.running = False
            return

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

    def set_form(self, form):
        self.form = form

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
        if obj in self.objects:
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
            self.board.running = False

        if xm < 10 or ym < 10:
            if xm < 10:
                self.new_move(0, self.speed * (1 if y > 0 else -1))
            if ym < 10:
                self.new_move(self.speed * (1 if x > 0 else -1), 0)
            if xm < self.width // 2 or ym < self.height // 2:
                self.shoot()
        else:
            if xm >= ym:
                self.new_move(0, self.speed * (1 if y > 0 else -1))
            elif xm < ym:
                self.new_move(self.speed * (1 if x > 0 else -1), 0)
        objects = self.board.objects
        for i in objects:
            if not hasattr(i, 'is_enemy'):
                xi = abs(self.pos.x - i.pos.x)
                yi = abs(self.pos.y - i.pos.y)
                if (xi ** 2 + yi ** 2) ** 0.5 < 100:
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
        char = self.board.get_char()
        if self is char:
            self.board.running = False
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

        self.speed = 20

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
            if not hasattr(i, 'is_enemy'):
                continue
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


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, is_strong=False):
        super().__init__()
        self.width = 50
        self.height = 50
        self.is_strong = is_strong
        if self.is_strong:
            self.image_origin = load_image("wall_chb.jpg")
        else:
            self.image_origin = load_image("wall.jpg")
        self.image = self.image_origin
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.width // 2
        self.rect.y = pos[1] - self.height // 2

        self.pos = Position(pos)

    def set_board(self, board):
        self.board = board

    def set_pos_x(self, x):
        self.pos.set_x(x)
        self.rect.x = x - self.width // 2

    def set_pos_y(self, y):
        self.pos.set_y(y)
        self.rect.y = y - self.height // 2

    def auto_action(self):
        objects = self.board.objects
        for i in objects:
            if i is self:
                continue
            x = abs(self.pos.x - i.pos.x)
            y = abs(self.pos.y - i.pos.y)
            if (x ** 2 + y ** 2) ** 0.5 < 25:
                i.die()
                self.die()
                break

    def die(self):
        if not self.is_strong:
            self.board.remove(self)


class Pause(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.width = 170
        self.height = 60
        self.image_origin = load_image("pause.png")
        self.image = self.image_origin
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.width // 2
        self.rect.y = pos[1] - self.height // 2

        self.pos = Position(pos)

    def set_board(self, board):
        self.board = board

    def set_pos_x(self, x):
        self.pos.set_x(x)
        self.rect.x = x - self.width // 2

    def set_pos_y(self, y):
        self.pos.set_y(y)
        self.rect.y = y - self.height // 2

    def die(self):
        self.board.remove(self)


def start_level_1(form):
    objects = []
    objects.append(Tank((50, 620), is_enemy=False))
    objects.append(Tank((620, 50)))

    objects.append(Wall((150, 0)))
    objects.append(Wall((150, 50)))
    objects.append(Wall((150, 100)))
    objects.append(Wall((150, 150)))
    objects.append(Wall((150, 200)))
    objects.append(Wall((150, 250)))
    objects.append(Wall((150, 300)))
    objects.append(Wall((200, 300)))
    objects.append(Wall((250, 300)))
    objects.append(Wall((300, 300)))
    objects.append(Wall((350, 300)))

    objects.append(Wall((450, 675)))
    objects.append(Wall((450, 625)))
    objects.append(Wall((450, 575)))
    objects.append(Wall((450, 525)))
    objects.append(Wall((450, 475)))

    objects.append(Wall((375, 410)))
    objects.append(Wall((425, 410)))
    objects.append(Wall((375, 460)))
    objects.append(Wall((375, 360)))
    objects.append(Wall((325, 410)))

    objects.append(Wall((200, 550), is_strong=True))
    objects.append(Wall((250, 550), is_strong=True))
    objects.append(Wall((200, 600), is_strong=True))
    objects.append(Wall((200, 500), is_strong=True))
    objects.append(Wall((150, 550), is_strong=True))

    board = Board(700, 700)
    board.set_objects(objects)
    board.set_form(form)
    return board.run()


def start_level_2(form):
    objects = []
    objects.append(Tank((50, 620), is_enemy=False))
    objects.append(Tank((620, 50)))

    objects.append(Wall((350, 350), is_strong=True))
    objects.append(Wall((350, 400), is_strong=True))
    objects.append(Wall((400, 350), is_strong=True))
    objects.append(Wall((350, 300), is_strong=True))
    objects.append(Wall((300, 350), is_strong=True))

    board = Board(700, 700)
    board.set_objects(objects)
    board.set_form(form)
    return board.run()


def start_level_3(form):
    objects = []
    objects.append(Tank((50, 620), is_enemy=False))
    objects.append(Tank((620, 50)))
    objects.append(Tank((350, 50)))

    objects.append(Wall((50, 50)))
    objects.append(Wall((100, 100)))
    objects.append(Wall((150, 150)))
    objects.append(Wall((200, 200)))
    objects.append(Wall((250, 250)))
    objects.append(Wall((300, 250), is_strong=True))
    objects.append(Wall((300, 300)))
    objects.append(Wall((350, 300), is_strong=True))
    objects.append(Wall((350, 350)))
    objects.append(Wall((400, 350), is_strong=True))
    objects.append(Wall((350, 350)))
    objects.append(Wall((400, 400)))
    objects.append(Wall((450, 450)))
    objects.append(Wall((500, 500)))
    objects.append(Wall((550, 550)))
    objects.append(Wall((600, 600)))
    objects.append(Wall((650, 650)))

    board = Board(700, 700)
    board.set_objects(objects)
    board.set_form(form)
    return board.run()

def start_level_4(form):
    objects = []
    objects.append(Tank((50, 620), is_enemy=False))
    objects.append(Tank((620, 50)))
    objects.append(Tank((120, 50)))

    objects.append(Wall((250, 0)))
    objects.append(Wall((250, 50)))
    objects.append(Wall((250, 100)))
    objects.append(Wall((250, 150)))
    objects.append(Wall((250, 200)))
    objects.append(Wall((250, 250)))
    objects.append(Wall((250, 300)))
    objects.append(Wall((200, 300)))
    objects.append(Wall((150, 300)))
    objects.append(Wall((100, 300)))
    objects.append(Wall((50, 300)))
    objects.append(Wall((0, 300)))
    objects.append(Wall((250, 350)))
    objects.append(Wall((250, 400)))
    objects.append(Wall((250, 450)))
    objects.append(Wall((300, 450)))
    objects.append(Wall((350, 450)))
    objects.append(Wall((400, 450)))
    objects.append(Wall((400, 500)))
    objects.append(Wall((400, 550)))
    objects.append(Wall((450, 550)))
    objects.append(Wall((500, 550)))
    objects.append(Wall((550, 550)))
    objects.append(Wall((600, 550)))
    objects.append(Wall((650, 550)))
    objects.append(Wall((700, 550)))
    objects.append(Wall((400, 600)))
    objects.append(Wall((400, 650)))
    objects.append(Wall((400, 700)))


    board = Board(700, 700)
    board.set_objects(objects)
    board.set_form(form)
    return board.run()

def start_level_5(form):
    objects = []
    objects.append(Tank((350, 550), is_enemy=False))
    objects.append(Tank((50, 650)))
    objects.append(Tank((600, 65)))
    objects.append(Tank((600, 650)))

    objects.append(Wall((350, 200)))
    objects.append(Wall((350, 250), is_strong=True))
    objects.append(Wall((400, 250)))
    objects.append(Wall((300, 250)))
    objects.append(Wall((350, 300)))

    objects.append(Wall((500, 400)))
    objects.append(Wall((500, 450), is_strong=True))
    objects.append(Wall((550, 450)))
    objects.append(Wall((450, 450)))
    objects.append(Wall((500, 500)))

    objects.append(Wall((225, 400)))
    objects.append(Wall((225, 450), is_strong=True))
    objects.append(Wall((275, 450)))
    objects.append(Wall((175, 450)))
    objects.append(Wall((225, 500)))



    board = Board(700, 700)
    board.set_objects(objects)
    board.set_form(form)
    return board.run()


pygame.init()
