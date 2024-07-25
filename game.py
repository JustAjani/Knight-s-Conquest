import pygame
from util.settings import SCREENH, SCREENW,HEROSPRITEPATH,SKELETONPATH,GOBLINPATH,MUSHROOMPATH,EYEPATH
from Scripts.player import Player
from Scripts.assetManager import AssetManager
from Scripts.InputHandler import InputHandler, DummyInputHandler
from Scripts.camera import Camera
from Enemies.BaseEnemy import Enemy 
from Enemies.Goblin import Goblin
from Enemies.Mushroom import Mushroom
from Enemies.FlyingEye import FlyingEye
from Scripts.health import Health
from Scripts.Gravity import Gravity
from util.SaveLoad import GameSaver
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
        
        #Player Animation
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

        #Goblin Animation
        self.assetManager.load_sprite_sheet('goblin_idle', GOBLINPATH + '/Idle.png', (150,150))
        self.assetManager.load_sprite_sheet('goblin_walk', GOBLINPATH + '/Run.png', (150,150))
        self.assetManager.load_sprite_sheet('goblin_attack', GOBLINPATH + '/Attack.png', (150,150))
        self.assetManager.load_sprite_sheet('goblin_death', GOBLINPATH + '/Death.png', (150,150))
        self.assetManager.load_sprite_sheet('goblin_attack2', GOBLINPATH + '/Attack2.png', (150,150))

        #Mushroom Animation
        self.assetManager.load_sprite_sheet('mushroom_idle', MUSHROOMPATH + '/Idle.png', (150,150))
        self.assetManager.load_sprite_sheet('mushroom_walk', MUSHROOMPATH + '/Run.png', (150,150))
        self.assetManager.load_sprite_sheet('mushroom_attack', MUSHROOMPATH + '/Attack.png', (150,150))
        self.assetManager.load_sprite_sheet('mushroom_death', MUSHROOMPATH + '/Death.png', (150,150))
        self.assetManager.load_sprite_sheet('mushroom_attack2', MUSHROOMPATH + '/Attack2.png', (150,150))
        self.assetManager.load_sprite_sheet('mushroom_attack3', MUSHROOMPATH + '/Attack3.png', (150,150))

        #Flying Eye Animation
        self.assetManager.load_sprite_sheet('eye_idle', EYEPATH + '/Flight.png', (150,150))
        self.assetManager.load_sprite_sheet('eye_walk', EYEPATH + '/Flight.png', (150,150))
        self.assetManager.load_sprite_sheet('eye_attack', EYEPATH + '/Attack.png', (150,150))
        self.assetManager.load_sprite_sheet('eye_death', EYEPATH + '/Death.png', (150,150))
        self.assetManager.load_sprite_sheet('eye_attack2', EYEPATH + '/Attack2.png', (150,150))
        self.assetManager.load_sprite_sheet('eye_attack3', EYEPATH + '/Attack3.png', (150,150))
        
        self.player = Player(self, pos=[-5, 300], size=[400, 400], inputHandler=self.PlayerInputHandler)
        
        self.enemy = []
        # self.enemy.append(Enemy(self, pos=[105,288], size= [400,400], moveDistance=400, inputHandler=self.enemyInputHandler))
        self.enemy.append(Goblin(self,pos=[105,288], size=[400,400]))
        self.enemy.append(Mushroom(self,pos=[105,288], size=[400,400]))
        # self.enemy.append(FlyingEye(self,pos=[105,20], size=[400,400]))

        self.health = Health(self,50, 20, 400, 20, 100, fg_color=(139,0,139), bg_color=(255, 0, 0))
        self.gravity = Gravity()
        self.gameSaver = GameSaver(self)

    def run(self):
        while True:
            self.deltaTime = pygame.time.Clock().tick(60) / 1000
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
                if event.type == pygame.KEYDOWN:
                    print("Key pressed:", pygame.key.name(event.key))  # Debug print for any key press
                    if event.key == pygame.K_p:
                        # print("Save key pressed")  # Debug print for saving
                        self.gameSaver.save_game()
                    if event.key == pygame.K_l:
                        # print("Load key pressed")  # Debug print for loading
                        self.gameSaver.load_game()

            self.screen.fill('#f7b32b')

            self.player.update(self.deltaTime)
            self.player.render()
            # self.gravity.apply(self.player,self.deltaTime)
            
            for enemy in self.enemy:
                # self.gravity.apply(enemy, self.deltaTime)
                enemy.update(self.deltaTime, self.player)
                enemy.render()
            
            pygame.display.update()
            self.clock.tick(60)

Game().run()
