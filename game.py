# game.py
import pygame
from util.settings import SCREENH, SCREENW, WORLD_WIDTH, WORLD_HEIGHT, HEROSPRITEPATH
from Scripts.player import Player
from Scripts.assetManager import AssetManager
from Scripts.InputHandler import InputHandler
from Scripts.camera import Camera
import sys

class Game:
    def __init__(self):
        pygame.init()
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

        self.assetManager = AssetManager()
        self.assetManager.load_sprite_sheet('knight_idle', HEROSPRITEPATH + "/Idle.png", (180, 180))
        self.assetManager.load_sprite_sheet('knight_run', HEROSPRITEPATH + "/Run.png", (180, 180))
        self.assetManager.load_sprite_sheet('knight_jump', HEROSPRITEPATH + "/Jump.png", (180, 180))
        self.assetManager.load_sprite_sheet('knight_attack', HEROSPRITEPATH + "/Attack1.png", (180, 180))
        self.assetManager.load_sprite_sheet('knight_attack2', HEROSPRITEPATH + "/Attack2.png", (180, 180))

        self.player = Player(self, pos=[45, 60], size=[200, 200], inputHandler=self.PlayerInputHandler)
        self.camera = Camera(self.player,WORLD_WIDTH,WORLD_HEIGHT)  # Use screen dimensions

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update()
            self.camera.update()

            self.screen.fill('#f7b32b')

            self.player.render(self.camera)

            pygame.display.update()
            self.clock.tick(60)

Game().run()
