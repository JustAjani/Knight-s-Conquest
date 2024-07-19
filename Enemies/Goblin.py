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

        # Debugging: Check the number of frames loaded for each animation
        for key, frames in self.animations.items():
            print(f"Animation: {key}, Frames Loaded: {len(frames)}")

        self.speed = 150
        self.move_distance = 120
        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.attack_cooldown = 2000  # Increased cooldown to slow down attack transitions
        self.last_attack_time = pygame.time.get_ticks()
        self.name = "goblin"
        self.update_image()

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            # Choosing the attack type
            attacks = {
                "attack": attack1Sound,
                "attack2": attack2Sound
            }
            chosen_attack = random.choice(list(attacks.keys()))
            self.currentAnimation = chosen_attack

            if not channel3.get_busy():
                channel3.play(attacks[chosen_attack])  

            self.frameIndex = 0
            self.update_image()
    

    def update_image(self):
        if self.frameIndex < len(self.animations[self.currentAnimation]):
            self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
            print(f"Current Animation: {self.currentAnimation}, Frame Index: {self.frameIndex}")
        else:
            print(f"Error: Frame index out of range for animation {self.currentAnimation}")

    def update(self, deltaTime, player):
        super().update(deltaTime, player)
        current_time = pygame.time.get_ticks()
        if current_time - self.lastUpdate > 1000 * self.animationSpeed:
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.lastUpdate = current_time
            self.update_image()
