import pygame
import random
from Enemies.BaseEnemy import Enemy
from util.Audio import *

class Goblin(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)

        self.animations = {
            "idle": game.assetManager.get_asset('goblin_idle'),
            "run": game.assetManager.get_asset('goblin_walk'),
            "death": game.assetManager.get_asset('goblin_death'),
            "attack": game.assetManager.get_asset('goblin_attack'),
            "attack2": game.assetManager.get_asset('goblin_attack2')
        }

        self.speed = 150
        self.move_distance = 120
        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.update_image()

        # Attack cooldown management
        self.attack_cooldown = 1000  # Cooldown time in milliseconds
        self.last_attack_time = pygame.time.get_ticks()

    def update(self, deltaTime, player):
        super().update(deltaTime, player)
        current_time = pygame.time.get_ticks()
        if current_time - self.lastUpdate > 1000 * self.animationSpeed:
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.lastUpdate = current_time
            self.update_image()

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            if random.choice([True, False]):
                self.currentAnimation = "attack"
            else:
                self.currentAnimation = "attack2"
            
            if not channel3.get_busy():
                    channel3.play(attack1Sound)

            self.frameIndex = 0
            self.update_image()

    def update_image(self):
        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
        print(f"Current Animation: {self.currentAnimation}, Frame Index: {self.frameIndex}")
