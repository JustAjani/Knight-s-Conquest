import pygame
from util.settings import *
from util.Audio import AudioPlayer
from Scripts.Gravity import Gravity 

class Player:
    def __init__(self, game, pos, size, inputHandler):
        self.game = game
        self.pos = list(pos)
        self.size = list(size)
        self.floorY = SCREENH
        self.inputHandler = inputHandler
        self.playerSpeed = 400
        self.gravity = 0.5
        self.velocity = [0,0]
        self.player_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.Jumping = False
        self.flip = False
        
        self.velocity_y = 0
        self.grounded = False
        self.ground_level = 600
        self.gravity = Gravity()

        self.audio_player = AudioPlayer()
        self.audio_player.setup_sounds()
        self.channel = self.audio_player.get_channel()
        
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

    def update(self,deltaTime):
        
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
            if not self.channel.get_busy():
                self.audio_player.enqueue_sound(self.audio_player.rightfoot)  
                self.audio_player.enqueue_sound(self.audio_player.leftfoot)  

        if inputs['jump']:
            if self.Jumping:
                self.gravity.jump(self, jump_strength=250)

        if inputs['attack1'] or inputs['left_click']:
            attack1 = True
            if not self.channel.get_busy():  
                self.audio_player.enqueue_sound(self.audio_player.attack1Sound)

        if inputs['attack2'] or inputs['right_click']:
            attack2 = True
            if not self.channel.get_busy():  
                self.audio_player.enqueue_sound(self.audio_player.attack2Sound)

        self.animationUpdate(moving, self.Jumping, attack1,attack2)
        # print(f"Player position after input: {self.pos}")

    def animationUpdate(self, moving, jumping, attack1,attack2):
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
        # adjusted_pos = camera.apply(self)
        if self.flip:
            current_anim = self.image_left
        else:
            current_anim = self.image
        self.game.screen.blit(current_anim, (self.pos[0],self.pos[1]))


        


            

          