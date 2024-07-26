import pygame
import os
import time
from collections import namedtuple, deque
import threading

# Define a namedtuple for sounds that includes the sound object and priority
SoundData = namedtuple('SoundData', ['sound', 'priority'])

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
        self.currently_playing = {}
        self.lock = threading.Lock()
        self.running = True
        self.update_thread = threading.Thread(target=self.run_update)
        self.update_thread.start()

    def enqueue_sound(self, sound_data):
        """Enqueue sound with priority directly associated with the sound data."""
        with self.lock:
            self.sound_queue.append(sound_data)
            print(f"Enqueued {sound_data.sound} with priority {sound_data.priority}")

    def run_update(self):
        while self.running:
            time.sleep(0.05)  # Adjust sleep time for better responsiveness
            with self.lock:
                self.update()

    def get_channel(self, required_priority):
        """Find an available channel or override a lower priority sound."""
        for channel in self.channels:
            if not channel.get_busy():
                return channel
            current_sound_data = self.currently_playing.get(channel)
            if current_sound_data and current_sound_data.priority < required_priority:
                channel.stop()  # Preemptively stop the current sound
                return channel
        if len(self.channels) < pygame.mixer.get_num_channels():
            new_channel = pygame.mixer.Channel(len(self.channels))
            self.channels.append(new_channel)
            return new_channel
        return None

    def play_sound(self, sound_data):
        """Play a sound from a sound data object."""
        channel = self.get_channel(sound_data.priority)
        if channel:
            channel.play(sound_data.sound)
            self.currently_playing[channel] = sound_data
            print(f"Playing sound on channel {self.channels.index(channel)} with priority {sound_data.priority}")
        else:
            print("Failed to obtain a channel")

    def update(self):
        """Update method to manage and play sounds from the queue."""
        self.cleanup_channels()
        if self.sound_queue:
            sound_data = self.sound_queue.popleft()  # Get the next sound from the queue
            self.play_sound(sound_data)

    def stop(self):
        """Stop the update thread."""
        self.running = False
        self.update_thread.join()

    def cleanup_channels(self):
        """Clean up unused channels to optimize resource usage."""
        self.channels = [channel for channel in self.channels if channel.get_busy()]
        self.currently_playing = {channel: sound for channel, sound in self.currently_playing.items() if channel.get_busy()}

    def load_audio(self, path):
        """Load audio from the specified path."""
        directories = self.AUDIOFILES.values()
        for directory in directories:
            full_path = os.path.join(directory, path)
            if os.path.exists(full_path):
                return pygame.mixer.Sound(full_path)
        raise FileNotFoundError(f"Failed to load sound from any specified directory: {path}")

    def setup_sounds(self):
        """Setup common sounds used in the game with associated priorities."""
        self.attack1Sound = SoundData(self.load_audio('sword-hit-medium.wav'), priority=3)
        self.attack2Sound = SoundData(self.load_audio('nasty-knife-stab-2.wav'), priority=3)
        self.rightfoot = SoundData(self.load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav'), priority=1)
        self.leftfoot = SoundData(self.load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav'), priority=1)
        self.skeletonWalk = SoundData(self.load_audio('step-skeleton.mp3'), priority=1)
        self.goblinWalk = SoundData(self.load_audio('goblin_03.wav'), priority=2)
        self.mushroomatt1 = SoundData(self.load_audio('clap.wav'), priority=2)
        self.mushroomatt2 = SoundData(self.load_audio('monster-bite.wav'), priority=2)
        self.mushroomatt3 = SoundData(self.load_audio('projectile-hit.flac'), priority=2)
        self.mushroomWalk = SoundData(self.load_audio('sludge-footsteps-1.wav'), priority=2)
        self.flyingEyeWalk = SoundData(self.load_audio('wing-flap.wav'), priority=1)
        self.flyingAttack = SoundData(self.load_audio('fast-collision-reverb.flac'), priority=3)

    def print_currently_playing(self):
        """Print the current sounds being played on all channels."""
        if not self.currently_playing:
            print("No sound is currently playing.")
        else:
            for channel, sound_data in self.currently_playing.items():
                print(f"Channel {self.channels.index(channel)} is playing: {sound_data.sound} with priority {sound_data.priority}")
