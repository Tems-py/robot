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
    (100, 0, 100, 500, (200, 20, 0)),
    (100, 650, 100, 70, (200, 20, 0)),
    (500, 100, 290, 100, (200, 20, 0)),
    (600, 900, 1000, 700, (200, 20, 0)),
]



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
        self.rotation = math.pi

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
                if x > WIDTH or y > HEIGHT or x < 0 or y < 0 or not r.check_collisions(x, y):
                    ll = False
                    break
            if not ll:
                break
            distance = math.sqrt((self.x - x) * (self.x - x) + (self.y - y) * (self.y - y))
            if distance > 200:
                pygame.draw.line(screen, (20, 20, 250), (self.x, self.y), (x, y), 2)
                return -1
        x, y = round(x), round(y)
        pygame.draw.line(screen, (20, 20, 250), (self.x, self.y), (x, y), 2)
        distance = math.sqrt((self.x - x) * (self.x - x) + (self.y - y) * (self.y - y))
        pygame.draw.circle(screen, (50, 250, 50), (x, y), 5, 0)
        return distance

    def rotate(self, value):
        self.rotation += math.pi * value * 2

    def move(self, value):
        self.x += math.cos(self.rotation) * value
        self.y += math.sin(self.rotation) * value


robot = Robot()

for w in walls:
    obj = Object(*w)
    objects.append(obj)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        robot.rotate(-0.04)
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        robot.rotate(0.04)
    if pygame.key.get_pressed()[pygame.K_UP]:
        robot.move(5)

    if pygame.key.get_pressed()[pygame.K_k]:
        print(robot.hypersonic())

    screen.fill((230, 230, 230))

    font = pygame.font.SysFont('Garamond', 30)
    textsurface = font.render(f'X: {robot.x}', False, (200, 200, 200))
    screen.blit(textsurface, (20, HEIGHT - 35))

    textsurface = font.render(f'Y: {robot.y}', False, (200, 200, 200))
    screen.blit(textsurface, (20, HEIGHT - 55))

    textsurface = font.render(f'R: {robot.rotation}', False, (200, 200, 200))
    screen.blit(textsurface, (20, HEIGHT - 75))

    textsurface = font.render(f'D: {robot.hypersonic()}', False, (200, 200, 200))
    screen.blit(textsurface, (20, HEIGHT - 95))

    robot.update()
    for r in objects:
        r.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(20)

pygame.quit()
