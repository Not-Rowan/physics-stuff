import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
PIXELS_PER_METER = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('projectiles')

WHITE = (255,255,255)

g = 9.81 * PIXELS_PER_METER

class Ball:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)

        self.force = pygame.Vector2(0, 0)
        self.mass = mass

        self.radius = radius
        self.color = color

    def collide_walls(self):
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.vel.x *= -0.9

        if self.pos.x + self.radius > WIDTH:
            self.pos.x = WIDTH - self.radius
            self.vel.x *= -0.9

        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.vel.y *= -0.9

        if self.pos.y + self.radius > HEIGHT:
            self.pos.y = HEIGHT - self.radius
            self.vel.y *= -0.9

    def apply_force(self, force):
        self.force += force
    
    def update(self, dt):
        acc = self.force / self.mass

        self.vel += acc * dt
        self.pos += self.vel * dt

        self.force = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

ball = Ball(
    x=200,
    y=500,
    vx=300,
    vy=-900,
    mass=1,
    radius=20,
    color=(255, 50, 50)
)


running = True
while running:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # physics updates
    gravity = pygame.Vector2(0, g * ball.mass)
    ball.apply_force(gravity)

    drag = -0.2 * ball.vel
    ball.apply_force(drag)

    ball.update(dt)
    ball.collide_walls()

    # visual updates
    screen.fill(WHITE)

    ball.draw(screen)

    pygame.display.flip()

pygame.quit()