import pygame
from Enemies.BaseEnemy import Enemy
from util.Audio import *

class Goblin(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)

        # Overriding animation assets specifically for Goblin
        self.animations = {
            "idle": game.assetManager.get_asset('goblin_idle'),
            "run": game.assetManager.get_asset('goblin_walk'),
            "death": game.assetManager.get_asset('goblin_death'),
            "attack": game.assetManager.get_asset('goblin_attack'),
        }

        self.speed = 120 
        self.move_distance = 150 

        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)

