import pygame
import os
from collections import deque

class AudioPlayer:
    AUDIOFILES = {
        'MUSICPATH': 'audio/sword/',
        'KNIGHTSOUND': 'audio/knight/',
        'SKELETSOUND': 'audio/skeleton/',
        'GOBLINSOUND': 'audio/goblin/',
        'MUSHROOMSOUND': 'audio/Mushroom/',
        'FLYINGSOUND': 'audio/FlyingEye/'
    }

    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.channels = []
        self.sound_queue = deque()  # Queue to hold sounds to be played

    def enqueue_sound(self, sound):
        """Add a sound to the queue to be played."""
        self.sound_queue.append(sound)

    def get_channel(self):
        """Find an available channel for playing audio."""
        for channel in self.channels:
            if not channel.get_busy():
                return channel
        if len(self.channels) < pygame.mixer.get_num_channels():
            new_channel = pygame.mixer.Channel(len(self.channels))
            self.channels.append(new_channel)
            return new_channel
        return self.channels[0]  # Return the first channel as a fallback

    def play_sound(self, sound):
        """Play a sound on an available channel."""
        channel = self.get_channel()
        if channel.get_busy():
            channel.stop()  # Optional: stop the current sound if busy
        channel.play(sound)

    def update(self):
        """Update method to manage and play sounds from the queue."""
        self.cleanup_channels()  # Clean up channels that are no longer active
        if self.sound_queue:
            sound_to_play = self.sound_queue.popleft()  # Get the next sound from the queue
            self.play_sound(sound_to_play)  # Play the sound

    def cleanup_channels(self):
        """Clean up unused channels to optimize resource usage."""
        before_cleanup = len(self.channels)
        self.channels = [channel for channel in self.channels if channel.get_busy()]
        after_cleanup = len(self.channels)
        print(f"Cleaned up channels: {before_cleanup} to {after_cleanup}")

    def load_audio(self, path):
        """Load audio from the specified path."""
        directories = self.AUDIOFILES.values()
        for directory in directories:
            full_path = os.path.join(directory, path)
            if os.path.exists(full_path):
                return pygame.mixer.Sound(full_path)
        raise FileNotFoundError(f"Failed to load sound from any specified directory: {path}")

    def setup_sounds(self):
        """Setup common sounds used in the game."""
        self.attack1Sound = self.load_audio('sword-hit-medium.wav')
        self.attack2Sound = self.load_audio('nasty-knife-stab-2.wav')
        self.rightfoot = self.load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav')
        self.leftfoot = self.load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav')
        self.skeletonWalk = self.load_audio('step-skeleton.mp3')
        self.goblinWalk = self.load_audio('goblin_03.wav')
        self.mushroomatt1 = self.load_audio('clap.wav')
        self.mushroomatt2 = self.load_audio('monster-bite.wav')
        self.mushroomatt3 = self.load_audio('projectile-hit.flac')
        self.mushroomWalk = self.load_audio('sludge-footsteps-1.wav')
        self.flyingEyeWalk = self.load_audio('wing-flap.wav')
        self.flyingAttack = self.load_audio('fast-collision-reverb.flac')