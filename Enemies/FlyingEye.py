import pygame
import random
from Enemies.BaseEnemy import Enemy
from util.Audio import *
from stateManager.stateManager import *

class FlyingEye(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.SCREENH = 600 + 35

        self.pos[1] = min(max(self.pos[1], 0), self.SCREENH - self.size[1])
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

        self.speed = 70
        self.move_distance = 80
        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.attack_cooldown = 2000
        self.last_attack_time = pygame.time.get_ticks()
        self.name = "flyingeye"
        self.update_image()

        self.state_machine.add_state('flying_eye_patrol', FlyingEyePatrolState(self))
        self.state_machine.add_state('flying_eye_attack', FlyingEyeAttackState(self))
        self.state_machine.change_state('flying_eye_patrol')

    def flying_eye_attack(self):
        current_time = pygame.time.get_ticks()
        distance_to_player = abs(self.enemy_rect.x - self.game.player.pos[0])
        if current_time - self.last_attack_time > self.attack_cooldown and distance_to_player <= self.attack_range:
            self.last_attack_time = current_time
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
    
        # Sync the enemy_rect to the new position
        self.enemy_rect.x = self.pos[0]
        self.enemy_rect.y = self.pos[1]

        # Check if the enemy should attack
        distance_to_player = abs(self.enemy_rect.x - player.pos[0])
        if distance_to_player <= self.attack_range and self.state_machine.current_state != "attacking":
            self.state_machine.change_state('attack')
        
        if self.state_machine.current_state == "attacking":
            if self.enemy_rect.y < self.target_y:
                self.enemy_rect.y = min(self.enemy_rect.y + self.speed * deltaTime, self.target_y)
            else:
                self.state_machine.change_state('returning')
        
        elif self.state_machine.current_state == "returning":
            if self.enemy_rect.y > self.original_y:
                self.enemy_rect.y = max(self.enemy_rect.y - self.speed * deltaTime, self.original_y)
            else:
                self.state_machine.change_state('idle')

        if current_time - self.lastUpdate > 1000 * self.animationSpeed:
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.lastUpdate = current_time
            self.update_image()
