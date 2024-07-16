import pygame
from util.settings import WORLD_WIDTH, WORLD_HEIGHT

class Camera:
    def __init__(self, player, width, height):
        self.player = player
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def update(self):
        self.rect.centerx = self.player.pos[0] + self.player.size[0] // 2
        self.rect.centery = self.player.pos[1] + self.player.size[1] // 2

        # Clamp the camera's rect so it doesn't move beyond the world boundaries
        self.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))
        print(f"Camera rect: {self.rect}")

    def apply(self, entity):
        # Adjust the entity's position relative to the camera and return the coordinates
        new_rect = entity.player_rect.move(-self.rect.topleft[0], -self.rect.topleft[1])
        return new_rect.topleft

