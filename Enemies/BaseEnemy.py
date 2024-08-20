import pygame
from Scripts.player import Player
from util.Audio import *
from stateManager.stateManager import StateMachine, PatrolState, ChaseState, AttackState, MemoryPatrolState , FleeState, DamageState, DeathState
from Enemies.ability import Ability
from Scripts.CollisionHandler import CollisionHandler
from Scripts.health import Health
import random

class Enemy(Player):
    def __init__(self, game, pos, size, moveDistance=100, inputHandler=None):
        super().__init__(game, pos, size, inputHandler)
        self.last_known_player_pos = None  # Initialize as None, will store (x, y) tuple
        self.velocity_y = 0
        self.grounded = False
        self.ground_level = 600

        self.animations = {
            "idle": game.assetManager.get_asset('skeleton_idle'),
            "run": game.assetManager.get_asset('skeleton_walk'),
            "death": game.assetManager.get_asset('skeleton_death'),
            "attack": game.assetManager.get_asset('skeleton_attack'),
            "shield": game.assetManager.get_asset('skeleton_shield'),
            "hit": game.assetManager.get_asset('skeleton_hit')
        }
        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.rect = self.enemy_rect
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)

        self.audio_player = AudioPlayer()
        self.audio_player.setup_sounds()

        self.move_distance = moveDistance
        self.start_pos = pos[0]
        self.end_pos = self.start_pos + moveDistance
        self.speed = 100
        self.state_cooldown = 2000
        self.last_state_change = pygame.time.get_ticks()
        self.attack_range = 100
        self.chase_range = 200
        self.post_attack_cooldown = 2000
        self.last_attack_time = 0

        self.last_flip_time = pygame.time.get_ticks()
        self.flip_cooldown = 500  # 500 milliseconds between flips
        self.name = "skeleton"

        self.attack_count = 0
        self.is_third_attack = False
        
        # Emotions variables
        self.fear = 0
        self.anger = 0
        self.isolated = False
        self.witnessed_powerful_player = False
        
        # Initialize state machine
        self.state_machine = StateMachine(self)
        self.state_machine.add_state('patrol', PatrolState(self))
        self.state_machine.add_state('chase', ChaseState(self))
        self.state_machine.add_state('attack', AttackState(self))
        self.state_machine.add_state('memory_patrol', MemoryPatrolState(self))
        self.state_machine.add_state('flee', FleeState(self))
        self.state_machine.add_state('hit', DamageState(self))
        self.state_machine.add_state('death', DeathState(self,self.game))

        self.animating = False
        self.ability = Ability(self.game, "none", "none", "none", size, pos)
        self.attacked = False
        self.dead = False

        self.mask = pygame.mask.from_surface(self.image)
        self.enemy_health = Health(self.game, 50, 20, 400, 20, max_health=self.health_max(), fg_color=(192,192,192), bg_color=(255, 0, 0))
    
    def update(self, deltaTime, player, all_enemies):
        self.enemy_rect.y = self.pos[1]
        self.adjustedspeed = self.speed * deltaTime
        current_time = pygame.time.get_ticks()

        self.check_isolation(all_enemies)
        self.update_emotions(player)  # Update emotions based on player interactions and game state
        self.state_machine.update()
        self.evaluate_combat_state(current_time, player)
        self.animationUpdate()
        CollisionHandler.resolve_collisions(self, all_enemies, allowed_overlap=305)

    def health_max(self):
        match self.name:
            case "skeleton":
                self.max_health = 25
            case "goblin":
                self.max_health = 28
            case "mushroom":
                self.max_health = 30
            case "flyingeye":
                self.max_health = 40
            case "fireworm":
                self.max_health = 45
        return self.max_health
   
    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
    
    def check_isolation(self, all_enemies, isolation_distance=200):
        nearby_enemies = sum(1 for enemy in all_enemies if enemy != self and 
                             self.distance_to(enemy) < isolation_distance)
        self.isolated = nearby_enemies == 0
    
    def distance_to(self, other):
        return ((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2) ** 0.5

    def update_emotions(self, player):
        if self.isolated:
            self.fear += 1
        if self.witnessed_powerful_player:
            self.fear += 2
            self.witnessed_powerful_player = False  

        self.fear = min(max(self.fear, 0), 100)  
        self.anger = min(max(self.anger, 0), 100)

    def evaluate_combat_state(self, current_time, player):
        player_distance = abs(self.enemy_rect.x - player.pos[0])

        # Check if the state needs updating based on cooldown
        if current_time - self.last_state_change > self.state_cooldown:
            if self.enemy_health.current_health <= 0 and not self.dead:
                self.state_machine.change_state('death')
                return  # Early exit to ensure no other state changes override this

            if self.attacked:
                self.state_machine.change_state('hit')
                return  # Early exit for immediate response to being hit

            if self.fear >= 20 and not self.attacked:  # Check fear only if not currently being hit
                self.state_machine.change_state('flee')
                return

            if player_distance <= self.attack_range:
                self.last_known_player_pos = None  # Engage in combat, forget last seen position
                self.state_machine.change_state('attack')
            elif player_distance <= self.chase_range:
                self.last_known_player_pos = player.pos  # Keep track of player position during chase
                self.state_machine.change_state('chase')
            else:
                if self.last_known_player_pos:
                    self.state_machine.change_state('memory_patrol')
                else:
                    self.state_machine.change_state('patrol')

            self.last_state_change = current_time  # Update the time of the last state change


    def patrol(self):
        current_time = pygame.time.get_ticks()
        if self.enemy_rect.x >= self.end_pos or self.enemy_rect.x <= self.start_pos:
            if current_time - self.last_flip_time > self.flip_cooldown:
                self.flip = not self.flip
                self.last_flip_time = current_time
        self.movement()
        self.audioHandling()

    def chase(self, player):
        current_time = pygame.time.get_ticks()
        self.last_known_player_pos = None  # Reset before updating new chase data
        self.last_known_player_pos = player.pos  # Update last known player position during chase
        self.handle_flip(current_time, player)
        self.movement()
        self.audioHandling()
    
    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_flip_time > self.flip_cooldown:
            self.handle_flip(current_time, player)
    
        # if self.audio_player.get_channel(2):
        #     self.audio_player.sound_queue(self.audio_player.attack1Sound)
    
    def handle_flip(self, current_time, player):
        if current_time - self.last_flip_time > self.flip_cooldown:
            previous_flip = self.flip
            if player.pos[0] > self.enemy_rect.x:
                self.flip = False
            else:
                self.flip = True
            print(f"Flipped from {previous_flip} to {self.flip} at time {current_time}")
            self.last_flip_time = current_time
   
    def movement (self):
        if self.flip:
            self.enemy_rect.x -= self.adjustedspeed
        else:
            self.enemy_rect.x += self.adjustedspeed
    
    def attack_counter(self):
        self.attack_count += 1
        if self.attack_count % 3 == 0:
            self.is_third_attack = True
            self.ability.trigger_ability()
        else:
            self.is_third_attack = False
  
    def flee(self):
        if self.last_known_player_pos is None:
            player_position = (self.enemy_rect.x, self.enemy_rect.y)
        else:
            player_position = self.last_known_player_pos

        print("Debug: player_position used for comparison:", player_position)  

        if player_position[0] < self.enemy_rect.x:
            self.flip = False
            self.enemy_rect.x += self.adjustedspeed
        else:
            self.flip = True
            self.enemy_rect.x -= self.adjustedspeed
        
        self.adjustedspeed *= 1.5
        self.animationUpdate()

    def animationUpdate(self):
        now = pygame.time.get_ticks()
        moving = self.state_machine.current_state in [self.state_machine.states['patrol'], self.state_machine.states['chase']]
        if self.state_machine.current_state == self.state_machine.states['death']:
            self.currentAnimation = "death"
            self.frameIndex = 0
        elif self.state_machine.current_state == self.state_machine.states['hit']:
            self.currentAnimation = "hit"
            self.frameIndex in [1, 3]
        elif moving and self.currentAnimation != "run":
            self.currentAnimation = "run"
            self.frameIndex = 0
        elif self.state_machine.current_state == self.state_machine.states['attack'] and not self.currentAnimation.startswith("attack"):
            self.currentAnimation = "attack"
            self.frameIndex = 0
        if self.animating and now - self.lastUpdate > int(1000 * self.animationSpeed):
            self.lastUpdate = now
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
            self.image_left = pygame.transform.flip(self.image, True, False)

        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
        self.image_left = pygame.transform.flip(self.image, True, False)
        self.continue_animation()
    
    def continue_animation(self):
        self.animating = True  

    def audioHandling(self):
        match self.name:
            case "skeleton":
                if self.audio_player.get_channel(2):
                    self.audio_player.enqueue_sound(self.audio_player.skeletonWalk)
            case "goblin":
                if self.audio_player.get_channel(2):
                    self.audio_player.enqueue_sound(self.audio_player.goblinWalk)
            case "mushroom":
                if self.audio_player.get_channel(2):
                    self.audio_player.enqueue_sound(self.audio_player.mushroomWalk)
            case "flyingeye":
                if self.audio_player.get_channel(2):
                    self.audio_player.enqueue_sound(self.audio_player.flyingEyeWalk)
            case "fireworm":
                if self.audio_player.get_channel(2):
                    self.audio_player.enqueue_sound(self.audio_player.wormWalk)

    def render(self):
        current_anim = self.image_left if self.flip else self.image
        if current_anim.get_locked():
            current_anim.unlock()
        self.game.screen.blit(current_anim, (self.enemy_rect.x, self.enemy_rect.y))


        self.enemy_mask = pygame.mask.from_surface(current_anim)
        outline = self.enemy_mask.outline()

        adjusted_outline = [(x + self.enemy_rect.x, y + self.enemy_rect.y) for x, y in outline]
        
        border_color = (0, 0, 255)  # Neutral
        if self.fear > 0:
            border_color = (192,192,192)  # Fear
        elif self.anger > 0:
            border_color = (139, 0, 0)  # Anger

        for point in adjusted_outline:
            pygame.draw.circle(self.game.screen, border_color, point, 1)
 

    



