import pygame
from Scripts.player import Player
from util.Audio import *

class Enemy(Player):
    def __init__(self, game, pos, size, moveDistance=100, inputHandler=None):
        super().__init__(game, pos, size, inputHandler)
        self.animations = {
            "idle": game.assetManager.get_asset('skeleton_idle'),
            "run": game.assetManager.get_asset('skeleton_walk'),
            "death": game.assetManager.get_asset('skeleton_death'),
            "attack": game.assetManager.get_asset('skeleton_attack'),
            "shield": game.assetManager.get_asset('skeleton_shield')
        }
        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)

        # Movement attributes
        self.move_distance = moveDistance
        self.start_pos = pos[0]  # Horizontal starting position
        self.end_pos = self.start_pos + moveDistance
        self.speed = 100
        self.state = "patrol"  # Initial state
        self.state_cooldown = 1000  # Cooldown time in milliseconds
        self.last_state_change = pygame.time.get_ticks()

    def update(self, deltaTime, player):
        self.adjustedspeed = self.speed * deltaTime
        current_time = pygame.time.get_ticks()

        if current_time - self.last_state_change > self.state_cooldown:
            if self.is_within_attack_range(player, 50):  # Closer range for attacks
                self.change_state("attack")
            elif self.is_within_attack_range(player):
                self.change_state("chase")
            else:
                self.change_state("patrol")
        
        if self.state == "patrol":
            self.patrol()
        elif self.state == "chase":
            self.chase(player)
        elif self.state == "attack":
            self.attack()

        self.animationUpdate()

    def change_state(self, new_state):
        if new_state != self.state:
            self.last_state_change = pygame.time.get_ticks()
            self.state = new_state

    def patrol(self):
        if self.enemy_rect.x >= self.end_pos or self.enemy_rect.x <= self.start_pos:
            self.flip = not self.flip

        if self.flip:
            self.enemy_rect.x -= self.adjustedspeed
            if not channel5.get_busy():  
                channel5.play(skeletonWalk)
        else:
            self.enemy_rect.x += self.adjustedspeed
            if not channel5.get_busy():  
                channel5.play(skeletonWalk)

    def chase(self, player):
        if player.pos[0] > self.enemy_rect.x:
            self.flip = False
            self.enemy_rect.x += self.adjustedspeed
        else:
            self.flip = True
            self.enemy_rect.x -= self.adjustedspeed

    def attack(self):
        self.currentAnimation = "attack"  
        if not channel3.get_busy():
            channel3.play(attack1Sound)

    def is_within_attack_range(self, player, range=100, offset=30):
        distance = abs(self.enemy_rect.x - player.pos[0]) - offset
        return distance <= range

    def render(self):
        current_anim = self.image_left if self.flip else self.image
        self.game.screen.blit(current_anim, (self.enemy_rect.x, self.enemy_rect.y))

    def animationUpdate(self):
        now = pygame.time.get_ticks()
        moving = self.state in ["patrol", "chase"]
        if moving and self.currentAnimation != "run":
            self.currentAnimation = "run"
            self.frameIndex = 0
        elif self.state == "attack" and self.currentAnimation != "attack":
            self.currentAnimation = "attack"
            self.frameIndex = 0

        if now - self.lastUpdate > int(1000 * self.animationSpeed):
            self.lastUpdate = now
            self.frameIndex += 1
            if self.frameIndex >= len(self.animations[self.currentAnimation]):
                self.frameIndex = 0  # Reset or loop the animation

        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
        self.image_left = pygame.transform.flip(self.image, True, False)
