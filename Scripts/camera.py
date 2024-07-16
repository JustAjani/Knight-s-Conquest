import pygame
from util.settings import WORLD_WIDTH

class Camera:
    def __init__(self, player, width, height):
        self.player = player
        self.rect = pygame.Rect(0, 0, width, height)
        self.last_player_x = player.pos[0]  # Initialize with the player's starting x position
        self.follow_vertical = False

    def update(self):
        # Calculate the change in the player's x position since the last frame
        dx = self.player.pos[0] - self.last_player_x
        print(f"dx: {dx}")  # Debug statement to check the change in position

        # Move the camera rect in the opposite direction of the player's movement
        self.rect.x -= dx
        print(f"Camera rect after update: {self.rect}")  # Debug statement to check camera position

        # Update the last_player_x for the next frame
        self.last_player_x = self.player.pos[0]

        # Ensure the camera stays within the world bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH

    def apply(self, entity):
        # Adjust entity's position for rendering based on the camera's position
        return (entity.player_rect.x - self.rect.x, entity.player_rect.y - self.rect.y)






