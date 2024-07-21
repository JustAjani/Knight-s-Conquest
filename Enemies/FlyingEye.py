import pygame
import random
from Enemies.BaseEnemy import Enemy
from util.Audio import *

class FlyingEye(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.SCREENH = (600 + 35)

        self.pos[1] = min(max(self.pos[1], 0), self.SCREENH  - self.size[1])
        self.original_y = self.pos[1]
        self.target_y = self.pos[1]
        self.attack_range = 150

        self.animations = {
            "idle": game.assetManager.get_asset('eye_idle'),
            "run": game.assetManager.get_asset('eye_walk'),
            "death": game.assetManager.get_asset('eye_death'),
            "attack": game.assetManager.get_asset('eye_attack'),
            "attack2": game.assetManager.get_asset('eye_attack2'),
            "attack3": game.assetManager.get_asset('eye_attack3'),
        }

        # Debugging: Check the number of frames loaded for each animation
        for key, frames in self.animations.items():
            print(f"Animation: {key}, Frames Loaded: {len(frames)}")

        self.speed = 70
        self.move_distance = 80
        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.attack_cooldown = 2000  # Increased cooldown to slow down attack transitions
        self.last_attack_time = pygame.time.get_ticks()
        self.name = "flyingeye"
        self.update_image()

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        distance_to_player = abs(self.enemy_rect.x - player.pos[0])
        if current_time - self.last_attack_time > self.attack_cooldown and distance_to_player <= self.attack_range and self.state != "returning":
            self.last_attack_time = current_time
            self.state = "attacking"

            self.target_y = min(self.enemy_rect.y + player.pos[0], self.SCREENH - self.size[1])
            # Choosing the attack type
            attacks = {
                "attack": mushroomatt2,
                "attack2": flyingAttack,
                "attack3": mushroomatt3  
            }
            chosen_attack = random.choice(list(attacks.keys()))
            self.currentAnimation = chosen_attack

            if not channel8.get_busy():
                channel8.play(attacks[chosen_attack])  

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

        # Check if the enemy should attack
        distance_to_player = abs(self.enemy_rect.x - player.pos[0])
        if distance_to_player <= self.attack_range and self.state not in ["attacking", "returning"]:
            self.attack(player)
        
        # Existing code to handle movement during attack and return
        if self.state == "attacking":
            if self.enemy_rect.y < self.target_y:
                self.enemy_rect.y = min(self.enemy_rect.y + self.speed * deltaTime, self.target_y)
            else:
                self.state = "returning"
        
        elif self.state == "returning":
            if self.enemy_rect.y > self.original_y:
                self.enemy_rect.y = max(self.enemy_rect.y - self.speed * deltaTime, self.original_y)
            else:
                self.state = "idle"

        if current_time - self.lastUpdate > 1000 * self.animationSpeed:
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.lastUpdate = current_time
            self.update_image()


