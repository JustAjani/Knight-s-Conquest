import pygame
from Enemies.BaseEnemy import Enemy

class FireWorm(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        
        # Define animations specific to FireWorm
        self.animations = {
            "idle": game.assetManager.get_asset('worm_idle'),
            "run": game.assetManager.get_asset('worm_walk'),
            "death": game.assetManager.get_asset('worm_death'),
            "attack": game.assetManager.get_asset('worm_attack'),
        }

        # Adjusted attributes for the FireWorm
        self.speed = 70
        self.move_distance = 80
        self.name = "FireWorm"
        self.attack_cooldown = 5000  # 5 seconds cooldown for attacks
        self.last_attack_time = pygame.time.get_ticks() - self.attack_cooldown  # Allow immediate attack on spawn

    def update(self, deltaTime, player):
        super().update(deltaTime, player)
        self.update_animation(deltaTime)
        # Debugging output to check positions
        # print(f"Update: pos={self.pos}, enemy_rect={self.enemy_rect}")

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            super().attack(player)  # Implement the attack logic from the base class
            self.last_attack_time = current_time
            print("FireWorm has attacked!")

    def update_animation(self, deltaTime):
        current_time = pygame.time.get_ticks()
        if current_time - self.lastUpdate > 1000 * self.animationSpeed:
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
            self.lastUpdate = current_time
            # print(f"Animation Update: Current Animation={self.currentAnimation}, Frame Index={self.frameIndex}, Image Size={self.image.get_size()}")
