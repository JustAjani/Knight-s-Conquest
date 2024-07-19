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

        self.move_distance = moveDistance
        self.start_pos = pos[0]
        self.end_pos = self.start_pos + moveDistance
        self.speed = 100
        self.state = "idle"  # Start in idle state
        self.state_cooldown = 2000  # Use same cooldown as post attack cooldown for initial idle
        self.last_state_change = pygame.time.get_ticks()
        self.attack_range = 100
        self.chase_range = 150  # Added buffer for chasing to provide hysteresis
        self.post_attack_cooldown = 2000  # 2000 milliseconds or 2 seconds
        self.last_attack_time = 0

        self.name = "skeleton"

    def update(self, deltaTime, player):
        self.adjustedspeed = self.speed * deltaTime
        current_time = pygame.time.get_ticks()

        if self.state == "idle":
            if current_time - self.last_state_change > self.state_cooldown:
                self.change_state("patrol",player)
        else:
            self.evaluate_combat_state(current_time, player)

        self.handle_movement(player)
        self.animationUpdate()

    def evaluate_combat_state(self, current_time, player):
        player_distance = abs(self.enemy_rect.x - player.pos[0])

        if self.state == "attack" and current_time - self.last_attack_time > self.post_attack_cooldown:
            if player_distance > self.attack_range + 20:  # Adding buffer
                self.change_state("chase", player)
        elif self.state != "attack":
            if player_distance <= self.attack_range:
                self.change_state("attack", player)
            elif player_distance <= self.chase_range:
                self.change_state("chase", player)
            else:
                self.change_state("patrol", player)

    def handle_movement(self, player):
        if self.state == "patrol":
            self.patrol()
        elif self.state == "chase":
            self.chase(player)
        elif self.state == "attack":
            self.attack()

    def change_state(self, new_state, player):
        current_time = pygame.time.get_ticks()
        if new_state != self.state and (current_time - self.last_state_change > self.state_cooldown):
            print(f"Changing state from {self.state} to {new_state}")
            self.state = new_state
            self.last_state_change = current_time

            # Reset flip based on player position
            if player.pos[0] > self.enemy_rect.x:
                self.flip = False
            else:
                self.flip = True

    def patrol(self):
        if self.enemy_rect.x >= self.end_pos or self.enemy_rect.x <= self.start_pos:
            self.flip = not self.flip

        if self.flip:
            self.enemy_rect.x -= self.adjustedspeed
        else:
            self.enemy_rect.x += self.adjustedspeed
        
        self.audioHandling()

    def chase(self, player):
        if player.pos[0] > self.enemy_rect.x:
            self.flip = False
            self.enemy_rect.x += self.adjustedspeed
        else:
            self.flip = True
            self.enemy_rect.x -= self.adjustedspeed
        
        self.audioHandling()

    def attack(self):
        self.currentAnimation = "attack"  
        if not channel3.get_busy():
            channel3.play(attack1Sound)
        self.last_attack_time = pygame.time.get_ticks()  # Update last attack time

    def is_within_attack_range(self, player, range=100, offset=30):
        distance = abs(self.enemy_rect.x - player.pos[0]) - offset
        return distance <= range
    
    def audioHandling(self):
        if self.name == "skeleton":
            if not channel5.get_busy():  
                    channel5.play(skeletonWalk)
        elif self.name == "goblin":
            if not channel6.get_busy():
                channel6.play(goblinwalk)
        elif self.name == "mushroom":
            if not channel7.get_busy():
                channel7.play(mushroomWalk)


    def render(self):
        current_anim = self.image_left if self.flip else self.image
        self.game.screen.blit(current_anim, (self.enemy_rect.x, self.enemy_rect.y))

    def animationUpdate(self):
        now = pygame.time.get_ticks()
        moving = self.state in ["patrol", "chase"]
        if moving and self.currentAnimation != "run":
            self.currentAnimation = "run"
            self.frameIndex = 0
        elif self.state == "attack" and not self.currentAnimation.startswith("attack"):
            self.currentAnimation = "attack"
            self.frameIndex = 0
        if now - self.lastUpdate > int(1000 * self.animationSpeed):
            self.lastUpdate = now
            self.frameIndex += 1
            if self.frameIndex >= len(self.animations[self.currentAnimation]):
                self.frameIndex = 0  # Reset or loop the animation

        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
        self.image_left = pygame.transform.flip(self.image, True, False)

