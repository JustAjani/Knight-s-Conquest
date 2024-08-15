import pygame
import random
import math

class Particle:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = color 
        self.speed = random.uniform(0, 5)  
        self.angle = random.uniform(0, math.pi * 2)  # Angle should be between 0 and 2π
        self.lifetime = random.randint(50, 100)

    def update(self):
        # Move the particle based on its speed and angle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Gradually reduce the size (simulating decay)
        self.size = max(0, self.size - 0.1)

        # Reduce lifetime
        self.lifetime -= 1

    def draw(self, surface):
        if self.size > 0:  # Only draw if the particle still has size
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
