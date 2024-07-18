import pygame
import os

AUDIOFILES = {
    'MUSICPATH' : 'audio/sword/',
    'KNIGHTSOUND' : 'audio/knight/',
    'SKELETSOUND' : 'audio/skeleton/'
}

def load_audio(path):
    directories = AUDIOFILES.values()
    for directory in directories:
        full_path = os.path.join(directory, path)
        if os.path.exists(full_path):
            return pygame.mixer.Sound(full_path)
    raise FileNotFoundError(f"Failed to load sound from any specified directory: {path}")

pygame.mixer.init(frequency=44100, size=-16, channels=5)
channel1 = pygame.mixer.Channel(1)
channel2 = pygame.mixer.Channel(2)
channel3 = pygame.mixer.Channel(3)
channel4 = pygame.mixer.Channel(4)
channel5 = pygame.mixer.Channel(5)

attack1Sound = load_audio('sword-hit-medium.wav')
attack2Sound = load_audio('nasty-knife-stab-2.wav')
rightfoot = load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav')
leftfoot = load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav')
skeletonWalk = load_audio('step-skeleton.mp3')