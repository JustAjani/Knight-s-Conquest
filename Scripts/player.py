import pygame
import random
import math
from util.settings import *
from util.Audio import AudioPlayer
from Scripts.Gravity import Gravity 
from Scripts.health import Health
from Scripts.CollisionHandler import CollisionHandler

class Player:
    def __init__(self, game, pos, size, inputHandler):
        """
        Initializes a new instance of the Player class.

        Parameters:
            game (Game): The game object to which this player belongs.
            pos (Tuple[int, int]): The initial position of the player as a tuple of x and y coordinates.
            size (Tuple[int, int]): The size of the player as a tuple of width and height.
            inputHandler (InputHandler): The input handler object to handle player input.

        Returns:
            None
        """
        self.game = game
        self.pos = list(pos)
        self.size = list(size)
        self.floorY = SCREENH
        self.inputHandler = inputHandler
        self.playerSpeed = 400
        self.gravity = 0.5
        self.velocity = [0,0]
        self.player_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.rect = self.player_rect
        self.Jumping = False
        self.flip = False
        self.attacked = False
        
        self.velocity_y = 0
        self.grounded = False
        self.ground_level = 600
        self.gravity = Gravity()

        self.audio_player = AudioPlayer()
        self.audio_player.setup_sounds()
        
        self.animations = {
              "idle": game.assetManager.get_asset('knight_idle'),
              "run": game.assetManager.get_asset('knight_run'),
              "jump": game.assetManager.get_asset('knight_jump'),
              "attack1": game.assetManager.get_asset('knight_attack'),
              "attack2": game.assetManager.get_asset('knight_attack2')
        }
        self.frameIndex = 0
        self.currentAnimation = "idle"
        self.animationSpeed = 0.1
        self.lastUpdate = pygame.time.get_ticks()
        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
        self.mask = pygame.mask.from_surface(self.image)
        
        self.health = Health(self, 50, 20, 400, 20, 100, fg_color=(192,192,192), bg_color=(255, 0, 0))

        self.attack_cooldown = 0.1
        self.last_attack_time = 0
        
        self.attacked = False
    def update(self,deltaTime,all_characters):
        """
        Updates the player's position and state based on the given time delta and input.

        Parameters:
            deltaTime (float): The time difference between the current and previous frames in seconds.

        Returns:
            None
        """
        
        # print(f"Player position before input: {self.pos}")
        inputs = self.inputHandler.get_input()
        moving = False
        attack1 = False
        attack2 = False

        movement = self.playerSpeed * deltaTime
        self.player_rect.x = self.pos[0]
        self.player_rect.y = self.pos[1]

        if inputs['move_left'] or inputs['move_right']:
            if inputs['move_right']:
                self.pos[0] += movement
            else:
                self.pos[0] -= movement
            moving = True
            self.flip = inputs['move_left']
            if self.audio_player.get_channel(1):
                self.audio_player.enqueue_sound(self.audio_player.rightfoot)  
                self.audio_player.enqueue_sound(self.audio_player.leftfoot)  

        if inputs['jump']:
            if self.Jumping:
                self.gravity.jump(self, jump_strength=250)

        if inputs['attack1']:
            attack1 = True
            if self.audio_player.get_channel(2):  
                self.audio_player.enqueue_sound(self.audio_player.attack1Sound)
                self.attack()

        if inputs['attack2']:
            attack2 = True
            if self.audio_player.get_channel(2):  
                self.audio_player.enqueue_sound(self.audio_player.attack2Sound)
                self.attack()

        self.animationUpdate(moving, self.Jumping, attack1,attack2)
        # print(f"Player position after input: {self.pos}")
        CollisionHandler.resolve_collisions(self, all_characters, allowed_overlap=305)
    
    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def animationUpdate(self, moving, jumping, attack1,attack2):
        """
        Updates the animation of the player based on its current state.

        This function checks the current state of the player and updates the animation accordingly. It checks if the player is attacking with attack1 or attack2, and if so, it sets the current animation to "attack1" or "attack2" respectively. If the player is moving, it checks if the current animation is not "run" and sets it to "run" with a frame index of 0. If the player is jumping, it checks if the current animation is not "jump" and sets it to "jump" with a frame index of 0. If none of the above conditions are met, it checks if the current animation is not "idle" and sets it to "idle" with a frame index of 0.

        The function also checks if enough time has passed since the last animation update. If so, it updates the frame index by incrementing it by 1 modulo the length of the current animation. It then scales and flips the image of the current frame and updates the image and image_left attributes of the player.

        Parameters:
            moving (bool): Indicates whether the player is moving or not.
            jumping (bool): Indicates whether the player is jumping or not.
            attack1 (bool): Indicates whether the player is attacking with attack1 or not.
            attack2 (bool): Indicates whether the player is attacking with attack2 or not.

        Returns:
            None
        """
        now = pygame.time.get_ticks()
        if attack1:
            self.currentAnimation != "attack1"
            self.currentAnimation = "attack1"
        elif attack2:
            self.currentAnimation != "attack2"
            self.currentAnimation = "attack2"
        elif moving:
            if self.currentAnimation != "run":
                self.currentAnimation = "run"
                self.frameIndex = 0
        elif jumping:
            if self.currentAnimation != "jump":
                self.currentAnimation = "jump"
                self.frameIndex = 0
        else:
            if self.currentAnimation != "idle":
                self.currentAnimation = "idle"
                self.frameIndex = 0

        if now - self.lastUpdate > int(1000 * self.animationSpeed):
            self.lastUpdate = now
            self.frameIndex += 1
        # Ensure the frameIndex does not exceed the number of frames in the animation
        if self.frameIndex >= len(self.animations[self.currentAnimation]):
            self.frameIndex = 0  # Reset or loop the animation
        
        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
        self.image_left = pygame.transform.flip(self.image,True,False)
    
    def render(self):
        """
        Renders the current animation of the player on the game screen.
        It uses a mask to create a precise border around the sprite.

        Parameters:
            None

        Returns:
            None
        """
        if self.flip:
            current_anim = self.image_left
        else:
            current_anim = self.image

        sprite_pos = (self.pos[0], self.pos[1])
        self.game.screen.blit(current_anim, sprite_pos)

        self.mask = pygame.mask.from_surface(current_anim)
        outline = self.mask.outline()  

        border_color = (0, 0, 0)  

        for point in outline:
            adjusted_point = (point[0] + sprite_pos[0], point[1] + sprite_pos[1])
            pygame.draw.circle(self.game.screen, border_color, adjusted_point, 1) 

        # self.health.render() 
    
    def can_attack(self):
        now = pygame.time.get_ticks()
        return now - self.last_attack_time >= self.attack_cooldown * 1000

    def attack(self):
        if self.can_attack():
            self.last_attack_time = pygame.time.get_ticks()

            if self.currentAnimation in ["attack1", "attack2"] and self.frameIndex in [4, 6]:
                ray_length = 5
                ray_start = (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

                # Calculate ray ends based on direction and multiple heights
                rays = [
                    ((ray_start[0], ray_start[1] - 10), (ray_start[0] - ray_length, ray_start[1] - 10) if self.flip else (ray_start[0] + ray_length, ray_start[1] - 10)),  # Higher ray
                    (ray_start, (ray_start[0] - ray_length, ray_start[1]) if self.flip else (ray_start[0] + ray_length, ray_start[1])),  # Middle ray
                    ((ray_start[0], ray_start[1] + 10), (ray_start[0] - ray_length, ray_start[1] + 10) if self.flip else (ray_start[0] + ray_length, ray_start[1] + 10))  # Lower ray
                ]

                for start, end in rays:
                    # if self.game.debug_mode:
                    pygame.draw.line(self.game.screen, (255, 0, 0), start, end, 2)
                        # self.render()

                    for enemy in self.game.enemies:
                        if self.line_rect_collision(start, end, enemy.enemy_rect):
                            if not enemy.attacked:
                                enemy.attacked = True
                                # Randomize the knockback distance within a range
                                knockback_distance = random.randint(20, 60) if self.currentAnimation == "attack2" else random.randint(10, 40)
                                direction_multiplier = -1 if self.flip else 1
                                enemy.pos[0] += knockback_distance * direction_multiplier
                                enemy.enemy_rect.x += knockback_distance * direction_multiplier
                                enemy.enemy_health.apply_decay(20) if self.currentAnimation == "attack2" else enemy.enemy_health.apply_decay(10)
                            else:
                                print("Already attacked")
                        else:
                            enemy.attacked = False
                            print("Miss")
                    else:
                        print("No enemies or not in range")

    def line_rect_collision(self,ray_start, ray_end, rect):
        # This function needs to determine if the line from ray_start to ray_end intersects the rectangle 'rect'
        # Simple algorithm to check intersection between a line and a rectangle
        # For simplicity, this might be an approximation or could use more sophisticated geometry libraries
        return rect.clipline(ray_start, ray_end)
    
    
    











    

    


        


            

          