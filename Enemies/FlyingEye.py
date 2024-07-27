import pygame
import random
from Enemies.BaseEnemy import Enemy
from util.Audio import *
from stateManager.stateManager import *

class FlyingEye(Enemy):
    def __init__(self, game, pos, size):
        """
        Initializes a FlyingEye enemy object with the given game, position, and size.
        
        Args:
            game (Game): The game object.
            pos (list): The position of the enemy as a list [x, y].
            size (list): The size of the enemy as a list [width, height].
        
        Returns:
            None
        
        This function initializes a FlyingEye enemy object by setting its attributes such as the screen height, position, attack range, animations, audio player, speed, move distance, enemy rectangle, frame index, current animation, animation speed, last update time, attack cooldown, last attack time, name, and state machine. It also adds states to the state machine and sets the initial state to 'flying_eye_patrol'. The enemy object is not returned, but is initialized within this function.
        """
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

        self.audio_player = AudioPlayer()
        self.audio_player.setup_sounds()

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

        self.is_attacking = False

    def attack(self,player):
        """
        Attacks the player if the cooldown has passed and the player is within the attack range.
        
        Args:
            player (Player): The player object.
        
        Returns:
            None
        
        This function checks if the current time minus the last attack time is greater than the attack cooldown and if the absolute difference between the enemy's x position and the player's x position is less than or equal to the attack range. If both conditions are met, it sets the last attack time to the current time, selects a random attack from a dictionary of attacks, sets the current animation to the chosen attack, and enqueues the chosen attack sound in the audio player if the second channel is available. If the conditions are not met, it sets the is_attacking attribute to False. It then resets the frame index and updates the image.
        """
        current_time = pygame.time.get_ticks()
        distance_to_player = abs(self.enemy_rect.x - self.game.player.pos[0])
        if current_time - self.last_attack_time > self.attack_cooldown and distance_to_player <= self.attack_range:
            self.last_attack_time = current_time
            attacks = {
                "attack": self.audio_player.enqueue_sound(self.audio_player.mushroomatt2),
                "attack2": self.audio_player.enqueue_sound(self.audio_player.flyingAttack),
                "attack3": self.audio_player.enqueue_sound(self.audio_player.mushroomatt3)  
            }
            chosen_attack = random.choice(list(attacks.keys()))
            self.currentAnimation = chosen_attack
            if self.audio_player.get_channel(2):
                self.audio_player.enqueue_sound(attacks[chosen_attack])  
        else:
            self.is_attacking = False

        self.frameIndex = 0
        self.update_image()

    def update_image(self):
        """
        Updates the image of the object based on the current animation and frame index.

        This function checks if the frame index is within the range of the current animation.
        If it is, it scales and sets the image of the object to the corresponding frame.
        It also prints the current animation and frame index.

        Parameters:
            None

        Returns:
            None
        """
        if self.frameIndex < len(self.animations[self.currentAnimation]):
            self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
            print(f"Current Animation: {self.currentAnimation}, Frame Index: {self.frameIndex}")
        else:
            print(f"Error: Frame index out of range for animation {self.currentAnimation}")

    def update(self, deltaTime, player):
        """
        Updates the FlyingEye enemy's position, state, and animation based on the given time delta and player position.

        Args:
            deltaTime (float): The time difference between the current and previous frames in seconds.
            player (Player): The player object that the enemy is interacting with.

        Returns:
            None
        """
        super().update(deltaTime, player)
        current_time = pygame.time.get_ticks()

        # Check if the enemy should attack
        distance_to_player = abs(self.enemy_rect.x - player.pos[0])
        if distance_to_player <= self.attack_range and self.state_machine.current_state != "flying_eye_attack":
            self.state_machine.change_state('flying_eye_attack')
        
        if self.state_machine.current_state == "flying_eye_attack":
            if self.enemy_rect.y < self.target_y:
                self.enemy_rect.y = min(self.enemy_rect.y + self.speed * deltaTime, self.target_y)
            else:
                self.state_machine.change_state('flying_eye_patrol')
        
        elif self.state_machine.current_state == "flying_eye_patrol":
            if self.enemy_rect.y > self.original_y:
                self.enemy_rect.y = max(self.enemy_rect.y - self.speed * deltaTime, self.original_y)
            else:
                self.state_machine.change_state('idle')
        
        self.state_machine.update()

        if current_time - self.lastUpdate > 1000 * self.animationSpeed:
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.lastUpdate = current_time
            self.update_image()
        
        
