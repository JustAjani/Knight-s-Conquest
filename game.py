import pygame
from util.settings import SCREENH, SCREENW,HEROSPRITEPATH,SKELETONPATH
from Scripts.player import Player
from Scripts.assetManager import AssetManager
from Scripts.InputHandler import InputHandler, DummyInputHandler
from Scripts.camera import Camera
from Scripts.BaseEnemy import Enemy 
from Scripts.health import Health
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screenSize = (SCREENW,SCREENH)
        self.screen = pygame.display.set_mode((SCREENW, SCREENH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Knight's Conquest")

        player1_keys = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_SPACE,
            'attack1': pygame.K_v,
            'attack2': pygame.K_b
        }
        self.PlayerInputHandler = InputHandler(player1_keys)
        self.enemyInputHandler = DummyInputHandler()

        self.assetManager = AssetManager()

        self.assetManager.load_sprite_sheet('knight_idle', HEROSPRITEPATH + "/Idle.png", (180, 180))
        self.assetManager.load_sprite_sheet('knight_run', HEROSPRITEPATH + "/Run.png", (180, 180))
        self.assetManager.load_sprite_sheet('knight_jump', HEROSPRITEPATH + "/Jump.png", (180, 180))
        self.assetManager.load_sprite_sheet('knight_attack', HEROSPRITEPATH + "/Attack1.png", (180, 180))
        self.assetManager.load_sprite_sheet('knight_attack2', HEROSPRITEPATH + "/Attack2.png", (180, 180))

        #Enemy Animation
        self.assetManager.load_sprite_sheet('skeleton_idle', SKELETONPATH + "/idle.png", (150,150))
        self.assetManager.load_sprite_sheet('skeleton_walk', SKELETONPATH + "/Walk.png", (150,150))
        self.assetManager.load_sprite_sheet('skeleton_attack',SKELETONPATH + "/Attack.png", (150,150))
        self.assetManager.load_sprite_sheet('skeleton_death',SKELETONPATH + "/Death.png", (150,150))
        self.assetManager.load_sprite_sheet('skeleton_shield', SKELETONPATH + "/Shield.png", (150,150))
        
        self.player = Player(self, pos=[-5, 300], size=[400, 400], inputHandler=self.PlayerInputHandler)
        self.enemy = Enemy(self, pos=[100,288], size= [400,400], moveDistance=400, inputHandler=self.enemyInputHandler)
        # self.camera = Camera(self.player,SCREENW,SCREENH)  # Use screen dimensions

        self.health = Health(self,50, 20, 400, 20, 100, fg_color=(139,0,139), bg_color=(255, 0, 0))

    def run(self):
        while True:
            self.deltaTime = pygame.time.Clock().tick(60) / 1000
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update(self.deltaTime)
            self.enemy.update(self.deltaTime,self.player)
            # self.camera.update()

            self.screen.fill('#f7b32b')

            self.player.render()
            self.enemy.render()
            self.health.render()

            pygame.display.update()
            self.clock.tick(60)

Game().run()
