import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('projectiles')

WHITE = (255,255,255)

G = 1500 # scaled gravitational constant

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

    def draw(self, screen, camera_offset, zoom):
        screen_pos = self.pos * zoom + camera_offset
        pygame.draw.circle(
            screen,
            self.color,
            (int(screen_pos.x), int(screen_pos.y)),
            max(1, int(self.radius * zoom))  # radius scales too
        )

def apply_gravity(a, b):

    r_vec = b.pos - a.pos # vector distance
    distance = r_vec.length() # absolute distance (scaled)

    # prevent division by zero
    if distance < 5:
        distance = 5

    r_hat = r_vec.normalize() # unit vector

    force_mag = G * a.mass * b.mass / distance**2

    force = r_hat * force_mag

    a.apply_force(force)
    b.apply_force(-force) # newton's third law


# camera movement/zoom
camera_offset = pygame.Vector2(0, 0)
dragging = False
last_mouse_pos = pygame.Vector2(0, 0)

zoom = 1  # 1.0 = 100%, <1 = zoom out, >1 = zoom in
ZOOM_STEP = 0.1  # amount to zoom per scroll


ball1 = Ball(
    x=100,
    y=500,
    vx=150,
    vy=50,
    mass=5.5e4,
    radius=50,
    color=(255, 50, 50)
)

ball2 = Ball(
    x=700,
    y=100,
    vx=-150,
    vy=-50,
    mass=5e4,
    radius=50,
    color=(0, 0, 255)
)


running = True
while running:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                dragging = True
                last_mouse_pos = pygame.Vector2(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = pygame.Vector2(event.pos)
                delta = mouse_pos - last_mouse_pos
                camera_offset += delta  # move camera by mouse movement
                last_mouse_pos = mouse_pos

        if event.type == pygame.MOUSEWHEEL:
            # zoom relative to mouse position
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            world_pos_before = (mouse - camera_offset) / zoom

            # update zoom factor
            if event.y > 0:  # scroll up
                zoom *= 1 + ZOOM_STEP
            else: # scroll down
                zoom /= 1 + ZOOM_STEP

            # adjust camera_offset so zoom is centered on mouse
            camera_offset = mouse - world_pos_before * zoom

    # physics updates
    apply_gravity(ball1, ball2)

    ball1.update(dt)
    ball2.update(dt)
    #ball1.collide_walls()

    # visual updates
    screen.fill(WHITE)

    ball1.draw(screen, camera_offset, zoom)
    ball2.draw(screen, camera_offset, zoom)

    pygame.display.flip()

pygame.quit()