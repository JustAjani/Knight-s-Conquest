# mushroom.py
import pygame
import random
from Enemies.BaseEnemy import Enemy
from util.Audio import *
from stateManager.stateManager import SpecialMushroomAttackState

class Mushroom(Enemy):
    def __init__(self, game, pos, size):
        """
        Initializes a new instance of the Mushroom class.

        Parameters:
            game (Game): The game object to which this mushroom belongs.
            pos (Tuple[int, int]): The initial position of the mushroom as a tuple of x and y coordinates.
            size (Tuple[int, int]): The size of the mushroom as a tuple of width and height.

        Returns:
            None
        """
        super().__init__(game, pos, size)

        self.animations = {
            "idle": game.assetManager.get_asset('mushroom_idle'),
            "run": game.assetManager.get_asset('mushroom_walk'),
            "death": game.assetManager.get_asset('mushroom_death'),
            "attack": game.assetManager.get_asset('mushroom_attack'),
            "attack2": game.assetManager.get_asset('mushroom_attack2'),
            "attack3": game.assetManager.get_asset('mushroom_attack3'),
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
        self.name = "mushroom"
        self.update_image()

        self.state_machine.add_state('attack', SpecialMushroomAttackState(self))
        self.state_machine.change_state('patrol')

    def mushroom_attack(self):
        """
        Executes a mushroom attack.

        This function checks if the current time minus the last attack time is greater than the attack cooldown. If it is,
        it updates the last attack time, selects a random attack from a dictionary of attacks, sets the current animation
        to the chosen attack, and enqueues the chosen attack sound in the audio player if the second channel is available.
        It then resets the frame index and updates the image.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            attacks = {
                "attack": self.audio_player.enqueue_sound(self.audio_player.mushroomatt1),
                "attack2": self.audio_player.enqueue_sound(self.audio_player.mushroomatt2),
                "attack3": self.audio_player.enqueue_sound(self.audio_player.mushroomatt3)
            }
            chosen_attack = random.choice(list(attacks.keys()))
            self.currentAnimation = chosen_attack

            if self.audio_player.get_channel(2):
                self.audio_player.enqueue_sound(attacks[chosen_attack])  

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
