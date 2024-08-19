import pygame
import os
import time
from collections import namedtuple, deque
import threading
from concurrent.futures import ThreadPoolExecutor
import logging

SoundData = namedtuple('SoundData', ['sound', 'priority'])

class AudioPlayer:
    DEBOUNCE_INTERVAL = 500  # milliseconds
    AUDIOFILES = {
        'MUSICPATH': 'audio/sword/',
        'KNIGHTSOUND': 'audio/knight/',
        'SKELETSOUND': 'audio/skeleton/',
        'GOBLINSOUND': 'audio/goblin/',
        'MUSHROOMSOUND': 'audio/Mushroom/',
        'FLYINGSOUND': 'audio/FlyingEye/',
        'WORMSOUND': 'audio/Worm/'
    }

    def __init__(self):
        """
        Initializes the AudioPlayer instance and sets up the thread pool.
        """
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.channels = []
        self.sound_queue = deque()
        self.currently_playing = {}
        self.sound_last_played = {}
        self.lock = threading.Lock()
        self.running = True
        self.executor = ThreadPoolExecutor(max_workers=10)  
        self.update_thread = threading.Thread(target=self.run_update)
        self.update_thread.start()

    def enqueue_sound(self, sound_data):
        """
        Enqueues a sound to be played in the thread pool.
        """
        self.executor.submit(self._enqueue_sound_task, sound_data)

    def _enqueue_sound_task(self, sound_data):
        """
        Task to enqueue sound, ensuring it adheres to the debounce interval.
        """
        if sound_data and sound_data.sound:
            current_time = pygame.time.get_ticks()
            last_played = self.sound_last_played.get(sound_data.sound, 0)
            if (current_time - last_played) >= self.DEBOUNCE_INTERVAL:
                with self.lock:
                    self.sound_queue.append(sound_data)
                    self.sound_last_played[sound_data.sound] = current_time

    def run_update(self):
        """
        Runs the update loop for the AudioPlayer.
        Continuously checks for new sounds to play in the thread pool.
        This method includes comprehensive error handling to manage potential issues
        with thread pool shutdown, task submission, and other unexpected errors.
        """
        while self.running:
            try:
                time.sleep(0.05)  # Adjust sleep time for better responsiveness

                # Only submit tasks if the player is still running and the executor is active
                if self.running:
                    try:
                        self.executor.submit(self.update)
                    except RuntimeError as e:
                        # Handle the case where the executor has been shut down
                        logging.error(f"Task submission failed: {e}")
                        break  # Exit the loop since we can't submit new tasks

            except Exception as e:
                # Catch any other unexpected exceptions that could crash the thread
                logging.error(f"An error occurred in run_update: {e}", exc_info=True)
                break  # Exit the loop to prevent continuous errors

        logging.info("Exiting run_update loop.")

    def play_sound(self, sound_data):
        """
        Plays a sound on a channel using the thread pool.
        """
        self.executor.submit(self._play_sound_task, sound_data)

    def _play_sound_task(self, sound_data):
        """
        Task to play sound on an appropriate channel based on priority.
        """
        channel = self.get_channel(sound_data.priority)
        if channel:
            channel.play(sound_data.sound)
            with self.lock:
                self.currently_playing[channel] = sound_data

    def update(self):
        """
        Updates the audio player by checking and playing sounds from the queue.
        """
        with self.lock:
            self.cleanup_channels()
            if self.sound_queue:
                sound_data = self.sound_queue.popleft()
                self.play_sound(sound_data)

    def stop(self):
        """
        Stops the audio player and shuts down the thread pool.
        """
        self.running = False
        self.update_thread.join()
        self.executor.shutdown(wait=True)  # Ensure all tasks are completed before shutting down

    def get_channel(self, required_priority):
        """
        Returns a channel from the list of channels or creates a new one if needed.
        """
        for channel in self.channels:
            if not channel.get_busy():
                return channel
            current_sound_data = self.currently_playing.get(channel)
            if current_sound_data and current_sound_data.priority < required_priority:
                channel.stop()  # Preemptively stop the lower priority sound
                return channel
        return self.create_new_channel()

    def create_new_channel(self):
        """
        Creates a new channel if possible.
        """
        if len(self.channels) < pygame.mixer.get_num_channels():
            new_channel = pygame.mixer.Channel(len(self.channels))
            self.channels.append(new_channel)
            return new_channel
        return None

    def cleanup_channels(self):
        """
        Cleans up channels that are no longer in use.
        """
        self.channels = [channel for channel in self.channels if channel.get_busy()]
        self.currently_playing = {channel: sound for channel, sound in self.currently_playing.items() if channel.get_busy()}

    def load_audio(self, path):
        """
        Load an audio file from the specified path.
        """
        directories = self.AUDIOFILES.values()
        for directory in directories:
            full_path = os.path.join(directory, path)
            if os.path.exists(full_path):
                return pygame.mixer.Sound(full_path)
        raise FileNotFoundError(f"Failed to load sound from any specified directory: {path}")

    def setup_sounds(self):
        """
        Set up sounds with associated priorities and debounce handling.
        """
        self.attack1Sound = SoundData(self.load_audio('sword-hit-medium.wav'), priority=3)
        self.attack2Sound = SoundData(self.load_audio('nasty-knife-stab-2.wav'), priority=3)
        self.rightfoot = SoundData(self.load_audio('knight-right-footstep-forestgrass-2-with-chainmail.wav'), priority=1)
        self.leftfoot = SoundData(self.load_audio('knight-left-footstep-forestgrass-5-with-chainmail.wav'), priority=1)
        self.skeletonWalk = SoundData(self.load_audio('step-skeleton.mp3'), priority=1)
        self.goblinWalk = SoundData(self.load_audio('goblin_03.wav'), priority=2)
        self.wormWalk = SoundData(self.load_audio('snake.wav'), priority=2)
        self.mushroomatt1 = SoundData(self.load_audio('clap.wav'), priority=2)
        self.mushroomatt2 = SoundData(self.load_audio('monster-bite.wav'), priority=2)
        self.mushroomatt3 = SoundData(self.load_audio('projectile-hit.flac'), priority=2)
        self.mushroomWalk = SoundData(self.load_audio('sludge-footsteps-1.wav'), priority=2)
        self.flyingEyeWalk = SoundData(self.load_audio('wing-flap.wav'), priority=1)
        self.flyingAttack = SoundData(self.load_audio('fast-collision-reverb.flac'), priority=3)
        self.wormAttack = SoundData(self.load_audio('fire-ball.wav'), priority=2)
    
    def get_audio_state(self):
        """
        Get the current audio state including currently playing sounds and their priorities.
        """
        audio_state = []
        for channel, sound_data in self.currently_playing.items():
            sound_name = sound_data.sound.get_buffer().raw  # Assuming the sound name can be extracted or stored somehow
            priority = sound_data.priority
            audio_state.append((sound_name, priority))
        return audio_state

    def set_audio_state(self, audio_state):
        """
        Set the audio state to the provided state.
        """
        self.stop_all_sounds()
        for sound_name, priority in audio_state:
            sound = self.load_audio(sound_name)  # Assuming you have a way to load the sound by name
            sound_data = SoundData(sound, priority)
            self.play_sound(sound_data)

    def stop_all_sounds(self):
        """
        Stop all currently playing sounds.
        """
        for channel in self.channels:
            channel.stop()
        self.currently_playing.clear()

    def print_currently_playing(self):
        """
        Prints the currently playing sounds and their associated priorities.
        """
        if not self.currently_playing:
            print("No sound is currently playing.")
        else:
            for channel, sound_data in self.currently_playing.items():
                print(f"Channel {self.channels.index(channel)} is playing: {sound_data.sound} with priority {sound_data.priority}")
