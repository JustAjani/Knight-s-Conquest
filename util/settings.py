import pygame

SCREENH = 600
SCREENW = 800

WORLD_WIDTH = 1600  # Example width of the game world
WORLD_HEIGHT = 1200  # Example height of the game world

HEROSPRITEPATH = "Assets\Hero Knight\Sprites"
MUSICPATH = 'audio/sword/'
KNIGHTSOUND = 'audio/knight/'

pygame.mixer.init(frequency=44100, size=-16, channels=2)
channel1 = pygame.mixer.Channel(1)
channel2 = pygame.mixer.Channel(2)
channel3 = pygame.mixer.Channel(3)
channel4 = pygame.mixer.Channel(4)

def load_audio(path):
    try:
        audio = pygame.mixer.Sound(MUSICPATH + path)
    except:
        audio = pygame.mixer.Sound(KNIGHTSOUND + path)
    return audio

attack1Sound = load_audio('sword-hit-medium.wav')
attack2Sound = load_audio('nasty-knife-stab-2.wav')
rightfoot = load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav')
leftfoot = load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav')