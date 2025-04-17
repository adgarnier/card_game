import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Game: Build a Solar System')

# Colors
WHITE = (255, 255, 255)
GREY = (178, 190, 181)
BLACK = (0, 0, 0)
RED = (210, 43, 43)
GREEN = (49, 146, 54)
BLUE = (76, 81, 247)
PURPLE = (157, 77, 187)
GOLD = (243, 175, 25)
GREY2 = (100, 100, 100)
YELLOW = (255, 255, 0)

# Constants
G = 6.67430e-11  # Gravitational constant

class CelestialBody:
    def __init__(self, x, y, mass, radius, color, vx=0, vy=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update_position(self, bodies):
        ax, ay = 0, 0
        for body in bodies:
            if body != self:
                dx = body.x - self.x
                dy = body.y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance == 0:
                    continue
                force = G * self.mass * body.mass / distance ** 2
                ax += force * dx / distance / self.mass
                ay += force * dy / distance / self.mass
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy

def main():
    running = True
    clock = pygame.time.Clock()
    bodies = []

    # Add a central body (e.g., a star) with a large mass at the center of the screen
    star = CelestialBody(WIDTH / 2, HEIGHT / 2, 1e13, 10, YELLOW)
    bodies.append(star)

    # Main game loop
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print('yes')
                    key_mass = 1e-50
                    key_color = BLUE
                    key_radius = 5
                elif event.key == pygame.K_8:
                    key_mass = 1e10
                    key_color = PURPLE
                    key_radius = 15

                elif event.key == pygame.K_9:
                    key_mass = 1e10
                    key_color = RED
                    key_radius = 10
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                mass = key_mass # Arbitrary mass
                radius = key_radius  # Arbitrary radius
                color = key_color

                # Calculate initial velocity for orbital motion
                dx = x - star.x
                dy = y - star.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                speed = math.sqrt(G * star.mass / distance)
                vx = -dy / distance * speed
                vy = dx / distance * speed

                bodies.append(CelestialBody(x, y, mass, radius, color, vx, vy))

        for body in bodies:
            body.update_position(bodies)
            body.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()