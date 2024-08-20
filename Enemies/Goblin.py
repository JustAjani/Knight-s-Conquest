import pygame
import random
from Enemies.BaseEnemy import Enemy
from util.Audio import *
from stateManager.stateManager import SpecialGoblinAttackState

class Goblin(Enemy):
    def __init__(self, game, pos, size):
        """
        Initializes a Goblin object with the given game, position, and size.

        Parameters:
            game (Game): The game object that the Goblin belongs to.
            pos (tuple): The position of the Goblin in the game world.
            size (tuple): The size of the Goblin.

        Returns:
            None

        Initializes the following attributes:
            - animations (dict): A dictionary containing the Goblin's animations.
            - speed (int): The speed of the Goblin.
            - move_distance (int): The distance the Goblin can move.
            - enemy_rect (pygame.Rect): The rectangle representing the Goblin's hitbox.
            - frameIndex (int): The current frame index of the Goblin's animation.
            - currentAnimation (str): The current animation of the Goblin.
            - animationSpeed (float): The speed of the Goblin's animation.
            - lastUpdate (int): The timestamp of the last update.
            - attack_cooldown (int): The cooldown time for the Goblin's attack.
            - last_attack_time (int): The timestamp of the last attack.
            - name (str): The name of the Goblin.

        Initializes the state machine with the 'attack' state and changes the state to 'patrol'.
        """
        super().__init__(game, pos, size)

        self.animations = {
            "idle": game.assetManager.get_asset('goblin_idle'),
            "run": game.assetManager.get_asset('goblin_walk'),
            "death": game.assetManager.get_asset('goblin_death'),
            "attack": game.assetManager.get_asset('goblin_attack'),
            "attack2": game.assetManager.get_asset('goblin_attack2'),
            "hit": game.assetManager.get_asset('goblin_hit'),
        }

        self.speed = 150
        self.move_distance = 120
        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.rect = self.enemy_rect
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.attack_cooldown = 2000
        self.last_attack_time = pygame.time.get_ticks()
        self.name = "goblin"
        # self.update_image()

        self.state_machine.add_state('attack', SpecialGoblinAttackState(self))
        self.state_machine.change_state('patrol')

    def goblin_attack(self):
        """
        Executes a goblin attack.

        This function checks if enough time has passed since the last attack. If enough time has passed, it updates the last attack time and generates a random attack from a dictionary of available attacks. The chosen attack is then set as the current animation of the goblin.

        If there is an available audio channel, the chosen attack sound is enqueued for playback.

        The frame index is reset to 0 and the goblin's image is updated.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            attacks = {
                "attack": self.audio_player.enqueue_sound(self.audio_player.attack1Sound),
                "attack2": self.audio_player.enqueue_sound(self.audio_player.attack2Sound)
            }
            chosen_attack = random.choice(list(attacks.keys()))
            self.currentAnimation = chosen_attack

            if self.audio_player.get_channel(2):
                self.audio_player.enqueue_sound(attacks[chosen_attack])  
                

            self.frameIndex = 0
            self.update_image()

    def update_image(self):
        """
        Updates the image of the object based on the current animation and frame index.

        This function checks if the frame index is within the range of the current animation. If it is, it scales and sets the image of the object to the corresponding frame. It also prints the current animation and frame index.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        if self.frameIndex < len(self.animations[self.currentAnimation]):
            self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
            print(f"Current Animation: {self.currentAnimation}, Frame Index: {self.frameIndex}")
        else:
            print(f"Error: Frame index out of range for animation {self.currentAnimation}")

    def update(self, deltaTime, player,all_enemies):
        """
        Updates the object's animation and image based on the time elapsed.

        Args:
            deltaTime (float): The time elapsed since the last update.
            player (Player): The player object for collision detection.

        Returns:
            None

        This function updates the object's animation and image based on the time elapsed. It first calls the update method of the parent class to update the object's position and state. Then, it checks if enough time has passed since the last update. If enough time has passed, it increments the frame index modulo the length of the current animation, updates the last update time, and calls the update_image method to update the object's image.
        """
        super().update(deltaTime, player,all_enemies)
        current_time = pygame.time.get_ticks()
        if current_time - self.lastUpdate > 1000 * self.animationSpeed:
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.lastUpdate = current_time
            self.update_image()
