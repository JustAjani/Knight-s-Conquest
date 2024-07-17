import pygame
from Scripts.player import Player

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
        self.flip = False
    
    def update(self,deltaTime):
        self.adjustedspeed = self.speed * deltaTime  # Calculate speed adjustment based on deltaTime
        self.move()
        self.animationUpdate()

        print(f"Update - Position: {self.pos}, Rect X: {self.enemy_rect.x}, Speed: {self.adjustedspeed}, Direction: {'Left' if self.flip else 'Right'}")
    
    def move(self):
        if self.enemy_rect.x >= self.end_pos:
            self.flip = True
        elif self.enemy_rect.x <= self.start_pos:
            self.flip = False

        # Apply movement
        if self.flip:
            self.enemy_rect.x -= self.adjustedspeed  # Move left if flipped
        else:
            self.enemy_rect.x += self.adjustedspeed  # Move right if not flipped
        
        self.pos[0] = self.enemy_rect.x

    def animationUpdate(self):
        now = pygame.time.get_ticks()
        moving = self.flip or not self.flip  # Simplify: moving is always True if there's horizontal movement

        if moving:
            self.currentAnimation = "run"
        else:
            self.currentAnimation = "idle"

        if now - self.lastUpdate > int(1000 * self.animationSpeed):
            self.lastUpdate = now
            self.frameIndex += 1
            if self.frameIndex >= len(self.animations[self.currentAnimation]):
                self.frameIndex = 0  # Reset or loop the animation

        self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
        self.image_left = pygame.transform.flip(self.image, True, False)
        
    def render(self):
        # adjusted_pos = camera.apply(self)
        if self.flip:
            current_anim = self.image_left
        else:
            current_anim = self.image
        self.game.screen.blit(current_anim, (self.pos[0],self.pos[1]))
