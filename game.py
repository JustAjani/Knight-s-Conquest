import pygame
import pygame.fastevent
from util.settings import SCREENH, SCREENW, HEROSPRITEPATH, SKELETONPATH, GOBLINPATH, MUSHROOMPATH, EYEPATH, ABILPATH, WORMPATH
from Scripts.player import Player
from Scripts.assetManager import AssetManager
from Scripts.InputHandler import InputHandler, DummyInputHandler
from Scripts.camera import Camera
from Enemies.BaseEnemy import Enemy 
from Enemies.Goblin import Goblin
from Enemies.Mushroom import Mushroom
from Enemies.FireWorm import FireWorm
from Scripts.health import Health
from Scripts.Gravity import Gravity
from util.Audio import AudioPlayer
from util.SaveLoad import GameSaver
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screenSize = (SCREENW, SCREENH)
        self.screen = pygame.display.set_mode((SCREENW, SCREENH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Knight's Conquest")

        player1_keys = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_SPACE, # X - PS   
            'attack1': pygame.K_v,  # B - Xbox, circle - PS
            'attack2': pygame.K_b,  # X - Xbox, Triangle - PS
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
        self.assetManager.load_sprite_sheet('skeleton_idle', SKELETONPATH + "/idle.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_walk', SKELETONPATH + "/Walk.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_attack', SKELETONPATH + "/Attack.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_death', SKELETONPATH + "/Death.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_shield', SKELETONPATH + "/Shield.png", (150, 150))

        #Goblin Animation
        self.assetManager.load_sprite_sheet('goblin_idle', GOBLINPATH + '/Idle.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_walk', GOBLINPATH + '/Run.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_attack', GOBLINPATH + '/Attack.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_death', GOBLINPATH + '/Death.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_attack2', GOBLINPATH + '/Attack2.png', (150, 150))

        #Mushroom Animation
        self.assetManager.load_sprite_sheet('mushroom_idle', MUSHROOMPATH + '/Idle.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_walk', MUSHROOMPATH + '/Run.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_attack', MUSHROOMPATH + '/Attack.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_death', MUSHROOMPATH + '/Death.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_attack2', MUSHROOMPATH + '/Attack2.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_attack3', MUSHROOMPATH + '/Attack3.png', (150, 150))

        #Flying Eye Animation
        self.assetManager.load_sprite_sheet('eye_idle', EYEPATH + '/Flight.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_walk', EYEPATH + '/Flight.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_attack', EYEPATH + '/Attack.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_death', EYEPATH + '/Death.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_attack2', EYEPATH + '/Attack2.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_attack3', EYEPATH + '/Attack3.png', (150, 150))

        self.assetManager.load_sprite_sheet('worm_death', WORMPATH + '/Death.png', (90, 90))
        self.assetManager.load_sprite_sheet('worm_idle', WORMPATH + '/Idle.png', (90, 90))
        self.assetManager.load_sprite_sheet('worm_walk', WORMPATH + '/Walk.png', (90, 90))
        self.assetManager.load_sprite_sheet('worm_attack', WORMPATH + '/Attack.png', (90, 90))

        # #Ability Animations
        # self.assetManager.load_sprite_sheet('M_Proectile', ABILPATH + '/M_Projectile_sprite.png', (150, 150))
        # self.assetManager.load_sprite_sheet('FE_Proectile', ABILPATH + '/FE_projectile_sprite.png', (150, 150))
        # self.assetManager.load_sprite_sheet('Bomb', ABILPATH + '/Bomb_sprite.png', (150, 150))
        # self.assetManager.load_sprite_sheet('Sword', ABILPATH + '/Sword_sprite.png', (150, 150))
        
        self.player = Player(self, pos=[-5, 300], size=[400, 400], inputHandler=self.PlayerInputHandler)
        
        self.enemies = []
        # self.enemies.append(Enemy(self, pos=[105, 288], size=[400, 400], inputHandler=self.enemyInputHandler))
        self.enemies.append(Goblin(self, pos=[105, 288], size=[400, 400]))
        self.enemies.append(Mushroom(self, pos=[105, 288], size=[400, 400]))
        self.enemies.append(FireWorm(self, pos=[210, 356], size=[300, 300]))

        self.health = Health(self, 50, 20, 400, 20, 100, fg_color=(139, 0, 139), bg_color=(255, 0, 0))
        self.gravity = Gravity()
        self.gameSaver = GameSaver(self)
        self.audioPlayer = AudioPlayer()

    def run(self):
        try:
            while True:
                self.deltaTime = pygame.time.Clock().tick(60) / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        print("Key pressed:", pygame.key.name(event.key))  # Debug print for any key press
                        if event.key == pygame.K_p:
                            self.gameSaver.save_game()
                        if event.key == pygame.K_l:
                            self.gameSaver.load_game()
                        if event.key == pygame.K_m:
                            self.gameSaver.delete_game()

                self.screen.fill('#f7b32b')

                self.audioPlayer.update()

                self.player.update(self.deltaTime)
                self.player.render()
                
                for enemy in self.enemies:
                    enemy.update(self.deltaTime, self.player)
                    enemy.render()
                
                pygame.display.update()
                self.deltaTime
        except Exception as e:
            self.handle_exception(e)

    def handle_exception(self, exception):
        print(f"An error occurred: {exception}")
        pygame.quit()
        sys.exit()

Game().run()
