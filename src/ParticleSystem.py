import random
import math


class Particle:
    def __init__(self, color, radius, x, y, speed, angle):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = math.cos(angle) * speed
        self.vy = -abs(math.sin(angle) * speed * 3)


class ParticleSystem:
    def __init__(self):
        self._particles = []

    def get_particles(self):
        return self._particles

    def add_particle(self, x, y):
        color = (random.randint(180, 255), random.randint(180, 255), random.randint(0, 50))
        angle = random.randint(180, 360) / 180 * math.pi
        speed = random.randint(50, 100) * 0.02
        radius = 8
        self._particles.append(Particle(color, radius, x, y, speed, angle))

    def update_particles(self, width, height):
        gravity = 0.2
        to_delete = []
        for p in self._particles:
            p.radius -= random.randint(1, 5) * 0.05

            p.x += p.vx
            p.y += p.vy

            # add gravity
            p.vy += math.sin(math.pi / 2) * gravity

            if p.radius < 0 or p.x < -p.radius or p.x > width + p.radius or p.y < -p.radius or p.y > height + p.radius:
                to_delete.append(p)

        for p in to_delete:
            self._particles.remove(p)

