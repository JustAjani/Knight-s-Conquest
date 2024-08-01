import pygame
import os
import time
from collections import namedtuple, deque
import threading

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
        Initializes the AudioPlayer instance.

        This method initializes the AudioPlayer instance by setting up the necessary
        audio parameters and starting the update thread. It initializes the channels
        list, sound queue, currently playing dictionary, sound last played dictionary,
        lock, running flag, and update thread.

        Parameters:
            None

        Returns:
            None
        """
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.channels = []
        self.sound_queue = deque()
        self.currently_playing = {}
        self.sound_last_played = {}
        self.lock = threading.Lock()
        self.running = True
        self.update_thread = threading.Thread(target=self.run_update)
        self.update_thread.start()

    def enqueue_sound(self, sound_data):
        """
        Enqueues a sound to be played.

        This method adds a sound to the sound queue if it is not already being played within the debounce interval.
        The debounce interval is a time period after which a sound can be played again.

        Parameters:
            sound_data (SoundData): The sound data to be enqueued.

        Returns:
            None
        """
        if sound_data and sound_data.sound:
            current_time = pygame.time.get_ticks()
            last_played = self.sound_last_played.get(sound_data.sound, 0)
            if (current_time - last_played) >= self.DEBOUNCE_INTERVAL:
                with self.lock:
                    self.sound_queue.append(sound_data)
                    self.sound_last_played[sound_data.sound] = current_time
        #             print(f"Enqueued {sound_data.sound} with priority {sound_data.priority}")
        #     else:
        #         print(f"Debounced {sound_data.sound}")
        # else:
        #     print("Attempted to enqueue invalid or non-existent sound.")

    def run_update(self):
        """
        Runs the update loop for the AudioPlayer.

        This method continuously runs the update loop while the AudioPlayer is running.
        It sleeps for a specified amount of time (0.05 seconds) to improve responsiveness.
        The update method is called within a lock to ensure thread safety.

        Parameters:
            None

        Returns:
            None
        """
        while self.running:
            time.sleep(0.05)  # Adjust sleep time for better responsiveness
            with self.lock:
                self.update()

    def get_channel(self, required_priority):
        """
        Returns a channel from the list of channels that is not currently busy and has a priority less than the required priority.
        If no such channel is found, a new channel is created and returned.

        Parameters:
            required_priority (int): The minimum priority required for the channel.

        Returns:
            Channel: The channel that meets the requirements.

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
        Creates a new channel if the number of channels is less than the maximum number of channels available.
        
        Returns:
            Channel: A new channel object if a new channel can be created. None otherwise.
        """
        if len(self.channels) < pygame.mixer.get_num_channels():
            new_channel = pygame.mixer.Channel(len(self.channels))
            self.channels.append(new_channel)
            return new_channel
        else:
            return None

    def play_sound(self, sound_data):
        """
        Plays a sound on a channel with the specified priority. If a channel is available with a priority lower than the required priority, the sound will preemptively stop the lower priority sound. If no channel is available, a new channel will be created if possible.

        Parameters:
            sound_data (SoundData): The sound data to be played.

        Returns:
            None
        """
        channel = self.get_channel(sound_data.priority)
        if channel:
            channel.play(sound_data.sound)
            self.currently_playing[channel] = sound_data
        #     print(f"Playing sound on channel {self.channels.index(channel)} with priority {sound_data.priority}")
        # else:
        #     print("Failed to obtain a channel")

    def update(self):
        """
        Updates the audio player by performing the following steps:
        
        1. Calls the `cleanup_channels` method to remove any channels that are no longer in use.
        2. Checks if there are any sounds in the `sound_queue`.
        3. If there are sounds in the queue, it removes the first sound from the queue and calls the `play_sound` method to play the sound on an available channel.
        
        This method does not take any parameters and does not return anything.
        """
        self.cleanup_channels()
        if self.sound_queue:
            sound_data = self.sound_queue.popleft()
            self.play_sound(sound_data)

    def stop(self):
        """
        Stops the audio player by setting the `running` flag to `False` and joining the `update_thread`.

        This method does not take any parameters.

        Returns:
            None
        """
        self.running = False
        self.update_thread.join()

    def cleanup_channels(self):
        """
        Removes any channels from the `channels` list that are not currently in use.
        Also removes any entries from the `currently_playing` dictionary that correspond to channels that are no longer in use.

        This method does not take any parameters.

        Returns:
            None
        """
        self.channels = [channel for channel in self.channels if channel.get_busy()]
        self.currently_playing = {channel: sound for channel, sound in self.currently_playing.items() if channel.get_busy()}

    def load_audio(self, path):
        """
        Load an audio file from the specified path.

        Args:
            path (str): The path to the audio file.

        Returns:
            pygame.mixer.Sound: The loaded audio file.

        Raises:
            FileNotFoundError: If the audio file cannot be found in any of the specified directories.

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

        This method initializes a series of SoundData objects with associated priorities.
        The sounds are loaded using the `load_audio` method.

        Returns:
            None
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

        Returns:
            list: A list of tuples containing sound names and their priorities.
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

        Args:
            audio_state (list): A list of tuples containing sound names and their priorities.

        Returns:
            None
        """
        self.stop_all_sounds()
        for sound_name, priority in audio_state:
            sound = self.load_audio(sound_name)  # Assuming you have a way to load the sound by name
            sound_data = SoundData(sound, priority)
            self.play_sound(sound_data)

    def stop_all_sounds(self):
        """
        Stop all currently playing sounds.

        Returns:
            None
        """
        for channel in self.channels:
            channel.stop()
        self.currently_playing.clear()

    def print_currently_playing(self):
        """
        Prints the currently playing sounds and their associated priorities.

        This method iterates over the `currently_playing` dictionary and prints the channel index, sound being played, and priority for each sound.

        Returns:
            None
        """
        if not self.currently_playing:
            print("No sound is currently playing.")
        else:
            for channel, sound_data in self.currently_playing.items():
                print(f"Channel {self.channels.index(channel)} is playing: {sound_data.sound} with priority {sound_data.priority}")
