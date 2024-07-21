import pygame
import os

AUDIOFILES = {
    'MUSICPATH' : 'audio/sword/',
    'KNIGHTSOUND' : 'audio/knight/',
    'SKELETSOUND' : 'audio/skeleton/',
    'GOBLINSOUND' : 'audio/goblin/',
    'MUSHROOMSOUND' : 'audio/Mushroom/',
    'FLYINGSOUND': 'audio/FlyingEye'
}

def load_audio(path):
    directories = AUDIOFILES.values()
    for directory in directories:
        full_path = os.path.join(directory, path)
        if os.path.exists(full_path):
            return pygame.mixer.Sound(full_path)
    raise FileNotFoundError(f"Failed to load sound from any specified directory: {path}")

pygame.mixer.init(frequency=44100, size=-16, channels=8)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
channel4 = pygame.mixer.Channel(3)
channel5 = pygame.mixer.Channel(4)
channel6 = pygame.mixer.Channel(5)
channel7 = pygame.mixer.Channel(6)
channel8 = pygame.mixer.Channel(7)

attack1Sound = load_audio('sword-hit-medium.wav')
attack2Sound = load_audio('nasty-knife-stab-2.wav')
rightfoot = load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav')
leftfoot = load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav')
skeletonWalk = load_audio('step-skeleton.mp3')
goblinWalk = load_audio('goblin_03.wav')
mushroomatt1 = load_audio('clap.wav')
mushroomatt2 = load_audio('monster-bite.wav')
mushroomatt3 = load_audio('projectile-hit.flac')
mushroomWalk = load_audio('sludge-footsteps-1.wav')
flyingEyeWalk = load_audio('wing-flap.wav')
flyingAttack = load_audio('fast-collision-reverb.flac')