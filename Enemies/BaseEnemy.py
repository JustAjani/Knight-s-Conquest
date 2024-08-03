import pygame
from Scripts.player import Player
from util.Audio import *
from stateManager.stateManager import StateMachine, PatrolState, ChaseState, AttackState, MemoryPatrolState
from Enemies.ability import Ability

class Enemy(Player):
    def __init__(self, game, pos, size, moveDistance=100, inputHandler=None):
        """
        Initializes an instance of the Enemy class.

        Args:
            game (Game): The game instance.
            pos (tuple): The position of the enemy as a tuple (x, y).
            size (tuple): The size of the enemy as a tuple (width, height).
            moveDistance (int, optional): The distance the enemy can move. Defaults to 100.
            inputHandler (InputHandler, optional): The input handler for the game. Defaults to None.

        Returns:
            None
        """
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
            "shield": game.assetManager.get_asset('skeleton_shield')
        }
        self.enemy_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
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
        
        # Initialize state machine
        self.state_machine = StateMachine(self)
        self.state_machine.add_state('patrol', PatrolState(self))
        self.state_machine.add_state('chase', ChaseState(self))
        self.state_machine.add_state('attack', AttackState(self))
        self.state_machine.add_state('memory_patrol', MemoryPatrolState(self))

        self.animating = False
        self.ability = Ability(self.game, "none", "none", "none", size, pos)

    def update(self, deltaTime, player):
        """
        Updates the enemy's position, state, and animation based on the given time delta and player position.

        Parameters:
            deltaTime (float): The time difference between the current and previous frames in seconds.
            player (Player): The player object that the enemy is interacting with.

        Returns:
            None
        """
        self.enemy_rect.y = self.pos[1]
        self.adjustedspeed = self.speed * deltaTime
        current_time = pygame.time.get_ticks()

        self.state_machine.update()
        self.evaluate_combat_state(current_time, player)
        self.animationUpdate()
    
    # def update_flip(self, player):
    #     """
    #     Updates the flip state of the enemy based on the player's position.

    #     Parameters:
    #         player (Player): The player object that the enemy is interacting with.

    #     Returns:
    #         None
    #     """
    #     current_time = pygame.time.get_ticks()
    #     if current_time - self.last_flip_time > self.flip_cooldown:
    #         if player.pos[0] > self.enemy_rect.x:
    #             self.flip = False
    #             self.last_flip_time = current_time
    #         elif player.pos[0] < self.enemy_rect.x:
    #             self.flip = True
    #             self.last_flip_time = current_time

    def evaluate_combat_state(self, current_time, player):
        player_distance = abs(self.enemy_rect.x - player.pos[0])
        if current_time - self.last_state_change > self.state_cooldown:
            if player_distance <= self.attack_range:
                self.last_known_player_pos = None  # Reset memory when engaging in combat
                self.state_machine.change_state('attack')
            elif player_distance <= self.chase_range:
                self.last_known_player_pos = player.pos  # Update last known position when in chase range
                self.state_machine.change_state('chase')
            else:
                if self.last_known_player_pos is not None:
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

        if self.flip:
            self.enemy_rect.x -= self.adjustedspeed
        else:
            self.enemy_rect.x += self.adjustedspeed
        
        self.audioHandling()

    def chase(self, player):
        current_time = pygame.time.get_ticks()
        self.last_known_player_pos = None  # Reset before updating new chase data
        self.last_known_player_pos = player.pos  # Update last known player position during chase
        
        if current_time - self.last_flip_time > self.flip_cooldown:
            if player.pos[0] > self.enemy_rect.x:
                self.flip = False
            else:
                self.flip = True
            self.last_flip_time = current_time

        if self.flip:
            self.enemy_rect.x -= self.adjustedspeed
        else:
            self.enemy_rect.x += self.adjustedspeed
        
        self.audioHandling()

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_flip_time > self.flip_cooldown:
            if player.pos[0] > self.enemy_rect.x:
                self.flip = False
            else:
                self.flip = True
            self.last_flip_time = current_time

        if self.audio_player.get_channel(2):
            self.audio_player.sound_queue(self.audio_player.attack1Sound)
        self.last_attack_time = pygame.time.get_ticks()
        
        self.attack_count += 1
        if self.attack_count % 3 == 0:
            self.is_third_attack = True
            self.ability.trigger_ability()
        else:
            self.is_third_attack = False

    def animationUpdate(self):
        """
        Update the animation of the enemy based on its current state.

        This function checks the current state of the enemy and updates the animation accordingly. It checks if the enemy is moving and if the current animation is not "run". If so, it sets the current animation to "run" and resets the frame index to 0. If the enemy's state is "attack" and the current animation does not start with "attack", it sets the current animation to "attack" and resets the frame index to 0.

        The function also checks if the enemy is animating and if the time elapsed since the last animation update is greater than the animation speed. If so, it updates the frame index by incrementing it by 1 modulo the length of the current animation. It then scales and flips the image of the current frame and updates the image and image_left attributes of the enemy.

        Parameters:
            None

        Returns:
            None
        """
        now = pygame.time.get_ticks()
        moving = self.state_machine.current_state in [self.state_machine.states['patrol'], self.state_machine.states['chase']]
        if moving and self.currentAnimation != "run":
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
        """
        Handles audio playback based on the enemy's name.

        This function checks the name of the enemy and plays the corresponding audio. It uses a match statement to check the name of the enemy and plays the appropriate audio. If the audio channel 2 is available, it enqueues the sound for the corresponding enemy.

        Parameters:
            None

        Returns:
            None
        """
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
        """
        Renders the current animation of the enemy on the game screen.

        This function determines the current animation based on the enemy's flip status and blits it onto the game screen at the enemy's position. It also prints the coordinates of the enemy's rendering position for debugging purposes.

        Parameters:
            None

        Returns:
            None
        """
        current_anim = self.image_left if self.flip else self.image
        self.game.screen.blit(current_anim, (self.enemy_rect.x, self.enemy_rect.y))
        # print(f"Rendering at x: {self.enemy_rect.x}, y: {self.enemy_rect.y}")  # Debugging output
