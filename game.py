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
from Scripts.Gravity import Gravity
from util.Audio import AudioPlayer
from Scripts.health import Health
# from util.SaveLoad import GameSaver
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.debug_mode = False
        self.screenSize = (SCREENW, SCREENH)
        self.screen = pygame.display.set_mode((SCREENW, SCREENH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Knight's Conquest")
        pygame.display.set_icon(pygame.image.load('Assets/gameIcon.webp'))
        self.font = pygame.font.SysFont('Arial', 24)

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
        self.assetManager.load_sprite_sheet('knight_death', HEROSPRITEPATH + "/Death.png", (180, 180))

        #Enemy Animation
        self.assetManager.load_sprite_sheet('skeleton_idle', SKELETONPATH + "/idle.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_walk', SKELETONPATH + "/Walk.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_attack', SKELETONPATH + "/Attack.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_death', SKELETONPATH + "/Death.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_shield', SKELETONPATH + "/Shield.png", (150, 150))
        self.assetManager.load_sprite_sheet('skeleton_hit', SKELETONPATH + "/Take Hit.png", (150, 150))

        #Goblin Animation
        self.assetManager.load_sprite_sheet('goblin_idle', GOBLINPATH + '/Idle.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_walk', GOBLINPATH + '/Run.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_attack', GOBLINPATH + '/Attack.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_death', GOBLINPATH + '/Death.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_attack2', GOBLINPATH + '/Attack2.png', (150, 150))
        self.assetManager.load_sprite_sheet('goblin_hit', GOBLINPATH + "/Take Hit.png", (150, 150))

        #Mushroom Animation
        self.assetManager.load_sprite_sheet('mushroom_idle', MUSHROOMPATH + '/Idle.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_walk', MUSHROOMPATH + '/Run.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_attack', MUSHROOMPATH + '/Attack.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_death', MUSHROOMPATH + '/Death.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_attack2', MUSHROOMPATH + '/Attack2.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_attack3', MUSHROOMPATH + '/Attack3.png', (150, 150))
        self.assetManager.load_sprite_sheet('mushroom_hit', MUSHROOMPATH + "/Take Hit.png", (150, 150))

        #Flying Eye Animation
        self.assetManager.load_sprite_sheet('eye_idle', EYEPATH + '/Flight.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_walk', EYEPATH + '/Flight.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_attack', EYEPATH + '/Attack.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_death', EYEPATH + '/Death.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_attack2', EYEPATH + '/Attack2.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_attack3', EYEPATH + '/Attack3.png', (150, 150))
        self.assetManager.load_sprite_sheet('eye_hit', EYEPATH + "/Take Hit.png", (150, 150))

        self.assetManager.load_sprite_sheet('worm_death', WORMPATH + '/Death.png', (90, 90))
        self.assetManager.load_sprite_sheet('worm_idle', WORMPATH + '/Idle.png', (90, 90))
        self.assetManager.load_sprite_sheet('worm_walk', WORMPATH + '/Walk.png', (90, 90))
        self.assetManager.load_sprite_sheet('worm_attack', WORMPATH + '/Attack.png', (90, 90))
        self.assetManager.load_sprite_sheet('worm_hit', WORMPATH + "/Get Hit.png", (90, 90))

        #Ability Animations
        self.assetManager.load_sprite_sheet('M_Projectile', ABILPATH + '/M_Projectile_sprite.png', (50, 50))
        self.assetManager.load_sprite_sheet('FE_Projectile', ABILPATH + '/FE_projectile_sprite.png', (48, 48))
        self.assetManager.load_sprite_sheet('Bomb', ABILPATH + '/Bomb_sprite.png', (100, 100))
        self.assetManager.load_sprite_sheet('Sword', ABILPATH + '/Sword_sprite.png', (102, 102))
        self.assetManager.load_sprite_sheet('Fireball', ABILPATH + '/Move.png', (46, 46))
        
        self.player = Player(self, pos=[-5, 300], size=[400, 400], inputHandler=self.PlayerInputHandler)
        
        self.enemies = []
        self.enemies.append(Enemy(self, pos=[110, 288], size=[400, 400], inputHandler=self.enemyInputHandler))
        self.enemies.append(Enemy(self, pos=[115, 288], size=[400, 400], inputHandler=self.enemyInputHandler))
        # self.enemies.append(Goblin(self, pos=[105, 288], size=[400, 400]))
        # self.enemies.append(Mushroom(self, pos=[105, 288], size=[400, 400]))
        # self.enemies.append(FireWorm(self, pos=[210, 360], size=[300, 300]))

        self.health = Health(self, 50, 20, 400, 20, 100, fg_color=(192,192,192), bg_color=(255, 0, 0))
        self.gravity = Gravity()
        # self.gameSaver = GameSaver(self)
        self.audioPlayer = AudioPlayer()

    def run(self):
        # try:
            while True:
                self.deltaTime = self.clock.tick(60) / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_x:  # Press 'x' to toggle debug mode
                            self.debug_mode = not self.debug_mode
                            if self.debug_mode:
                                print('debug on')
                            else:
                                print('debug off')

                self.screen.fill('#f7b32b')
                
                # Spawns All The Enemies
                for enemy in self.enemies:
                    enemy.update(self.deltaTime, self.player, self.enemies)
                    enemy.render()
                
                # Spawns and Updates The Player
                self.player.update(self.deltaTime, self.enemies)
                self.player.render()
                self.player.health.render()

                
                # Calculate and draw FPS
                fps = self.clock.get_fps()
                fps_text = self.font.render(f"FPS: {int(fps)}", True, pygame.Color('white'))
                self.screen.blit(fps_text, (SCREENW - fps_text.get_width() - 10, 10))

                pygame.display.update()
        # except Exception as e:
        #     self.cleanUp(e)
            
    def cleanUp(self, exception):
        print(f"An error occurred: {exception}")
        pygame.quit()
        sys.exit()

Game().run()
