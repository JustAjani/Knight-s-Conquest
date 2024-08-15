import pygame
import random
import math

class Particle:
    def __init__(self, game, color, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = color  
        self.alpha = 255  
        self.speed = random.uniform(0, 5)
        self.angle = random.uniform(0, math.pi * 2)
        self.lifetime = 0.2 
        self.elapsed_time = 0

    def update(self, deltaTime):
        self.elapsed_time += deltaTime
        
        # Fade the particle over its lifetime
        lifetime_ratio = self.elapsed_time / self.lifetime
        self.alpha = max(0, 255 * (1 - lifetime_ratio))  # Fade from 255 to 0

        if self.elapsed_time >= self.lifetime:
            return False  # Indicate that this particle should be removed
        
        # Move the particle
        self.x += math.cos(self.angle) * self.speed * deltaTime
        self.y += math.sin(self.angle) * self.speed * deltaTime

        # Optionally, reduce the size
        self.size = max(0, self.size - 0.1 * deltaTime)

        return True  # Indicate that the particle is still alive

    def render(self):
        if self.size > 0 and self.alpha > 0:  # Only draw if the particle still has size and alpha
            color_with_alpha = (*self.color, int(self.alpha))  # Add alpha to the color
            surface_with_alpha = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)  # Create a surface with alpha
            pygame.draw.circle(surface_with_alpha, color_with_alpha, (self.size, self.size), int(self.size))
            self.game.screen.blit(surface_with_alpha, (int(self.x - self.size), int(self.y - self.size)))

class BloodParticle(Particle):
    def __init__(self, game, x, y):
        color = (255, 87, 51) 
        super().__init__(game, color, x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.size = random.randint(4, 7)  # Slightly bigger particles for blood
        self.speed = random.uniform(1, 10)  # Faster moving particles
        self.lifetime = random.uniform(0.5, 1.5)  # Longer lifetime for dramatic effect

    def update(self, deltaTime):
        super().update(deltaTime)

