import pygame
from util.settings import SCREENH, SCREENW

class Player:
    def __init__(self, game, pos, size, inputHandler):
        self.game = game
        self.pos = list(pos)
        self.size = list(size)
        self.floorY = SCREENH
        self.inputHandler = inputHandler
        self.deltaTime = pygame.time.Clock().tick(60) / 1000
        self.playerSpeed = 200
        self.gravity = 0.5
        self.velocity = [0,0]
        self.playerX = SCREENW // 2 - self.size[0] //2
        self.playerY = SCREENH - self.size[1] //2 - self.floorY
        self.Jumping = False
        self.flip = False

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

    def update(self):
        inputs = self.inputHandler.get_input()
        moving = False
        attack1 = False
        attack2 = False

        movement = self.playerSpeed * self.deltaTime

        if inputs['move_left']:
            self.pos[0] -= movement
            moving = True
            if not self.flip:
                self.flip = True
        if inputs['move_right']:
            self.pos[0] += movement
            moving = True
            if self.flip:
                self.flip = False
        if inputs['jump']:
            if self.Jumping:
                self.jump()
        if inputs['attack1'] or inputs['left_click']:
            attack1 = True
        if inputs['attack2'] or inputs['right_click']:
            attack2 = True

        self.animationUpdate(moving, self.Jumping, attack1,attack2)

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

    def jump(self):
        self.Jumping = False
        if self.Jumping:
            self.playerY -= self.velocity[1]
        elif self.playerY >= self.floorY - self.size[1]:
             self.playerY = self.floorY - self.size[1]
             self.Jumping = True
    
    def render(self):
        if self.flip:
            current_anim =  self.image_left 
        else:
            current_anim = self.image

        self.game.screen.blit(current_anim,(self.pos[0],self.pos[1]))
        pygame.display.update()


        


            

          