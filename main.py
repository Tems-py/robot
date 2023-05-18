import math

import pygame

WIDTH, HEIGHT = 1280, 720

# pygame setup
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Robot co skanuje pokój Pana Piotra Matei')
clock = pygame.time.Clock()
running = True

objects = []

walls = [
    # (x, y, width, height, (r, g, b)),
    (200, 0, 199, 500, (200, 20, 0)),
    (200, 650, 199, 70, (200, 20, 0)),
    (700, 400, 199, 100, (200, 20, 0)),
]


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.states = [[0 for _ in range(width)] for _ in range(height)]

    def draw(self):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i, x in enumerate(self.states):
            for j, y in enumerate(x):
                color = (60, 60, 60, 80)
                if y == 1:
                    color = (50, 100, 250, 80)
                pygame.draw.circle(surface, color, (WIDTH - i * 20 - 20, HEIGHT - j * 20 - 20), 8, 0)

        screen.blit(surface, (0, 0))

    def set_on(self, x, y):
        print(x, y)
        x = self.height - x
        y = self.width - y
        self.states[x][y] = 1


class Object:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def check_collisions(self, x, y):
        if self.x < x < self.x + self.width:
            if self.y < y < self.y + self.height:
                return False
        return True

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.rect.Rect(self.x, self.y, self.width, self.height))


class Robot:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.imaginary_x = 50
        self.imaginary_y = 50
        self.rotation = 1 / 2 * math.pi

    def draw(self):
        # screen.blit(pygame.transform.scale(self.image, (50, 50)), (self.x, self.y))
        pygame.draw.circle(screen, (50, 50, 50), (self.x, self.y), 20, 0)

    def update(self):
        self.hypersonic()
        self.draw()

    def hypersonic(self):
        x, y = self.x, self.y
        ll = True
        while ll:
            x += math.cos(self.rotation)
            y += math.sin(self.rotation)
            for r in objects:
                # x > WIDTH or y > HEIGHT or x < 0 or y < 0 or
                if not r.check_collisions(x, y):
                    ll = False
                    break
            if not ll:
                break
            distance = math.sqrt((self.x - x) * (self.x - x) + (self.y - y) * (self.y - y))
            if distance > 200:
                pygame.draw.line(screen, (20, 20, 250), (self.x, self.y), (x, y), 2)
                return -1, -1, -1
        x, y = round(x), round(y)
        pygame.draw.line(screen, (20, 20, 250), (self.x, self.y), (x, y), 2)
        distance = math.sqrt((self.x - x) * (self.x - x) + (self.y - y) * (self.y - y))
        pygame.draw.circle(screen, (50, 250, 50), (x, y), 5, 0)
        return distance, x, y

    def rotate(self, value):
        self.rotation += math.pi * value * 2

    def move(self, value):
        self.x += math.cos(self.rotation) * value
        self.y += math.sin(self.rotation) * value


robot = Robot()
display = Display(8, 16)

for w in walls:
    obj = Object(*w)
    objects.append(obj)

scanned_points = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        robot.rotate(-0.01)
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        robot.rotate(0.01)
    if pygame.key.get_pressed()[pygame.K_UP]:
        robot.move(5)

    screen.fill((230, 230, 230))

    font = pygame.font.SysFont('Garamond', 30)
    textsurface = font.render(f'X: {robot.x}', False, (200, 200, 200))
    screen.blit(textsurface, (20, HEIGHT - 35))

    textsurface = font.render(f'Y: {robot.y}', False, (200, 200, 200))
    screen.blit(textsurface, (20, HEIGHT - 55))

    textsurface = font.render(f'R: {robot.rotation}', False, (200, 200, 200))
    screen.blit(textsurface, (20, HEIGHT - 75))

    distance = robot.hypersonic()
    textsurface = font.render(f'D: {distance}', False, (200, 200, 200))
    screen.blit(textsurface, (20, HEIGHT - 95))

    textsurface = font.render(f'M_X: {display.x}', False, (200, 200, 200))
    screen.blit(textsurface, (WIDTH - display.height * 20, HEIGHT - display.width * 20 - 40))

    textsurface = font.render(f'M_Y: {display.y}', False, (200, 200, 200))
    screen.blit(textsurface, (WIDTH - display.height * 15, HEIGHT - display.width * 20 - 40))

    robot.update()
    for r in objects:
        r.draw()

    if distance[0] != -1:
        if (distance[1], distance[2]) not in scanned_points:
            scanned_points.append((round(distance[1] / (WIDTH / 16)), round(distance[2] / (HEIGHT / 8))))

    for p in scanned_points:
        display.set_on(p[0] + 1, p[1] + 1)

    display.draw()

    for i in range(16):
        pygame.draw.line(screen, (0, 0, 0), (i * (WIDTH / 16), 0), (i * (WIDTH / 16), HEIGHT))

    for i in range(8):
        pygame.draw.line(screen, (0, 0, 0), (0, i * HEIGHT / 8), (WIDTH, i * HEIGHT / 8))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(20)

pygame.quit()
