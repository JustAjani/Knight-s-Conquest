from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import sys
import json
import os

class GameSaver:
    def __init__(self, game, filename='JSON/savegame.json', key=None):
        """
        Initialize the GameSaver with game reference, filename, and encryption key.
        """
        self.game = game
        self.filename = filename
        self.key = key if key else os.urandom(16)
        self.iv = os.urandom(AES.block_size)

    def serialize_game_state(self):
        """
        Serialize the game state to a dictionary.
        """
        player_state = {
            'position': self.game.player.pos,
            'health': self.game.health.current_health
        }

        enemies_state = []
        for enemy in self.game.enemy:
            enemies_state.append({
                'type': enemy.__class__.__name__,
                'position': enemy.pos,
            })

        game_state = {'player': player_state, 'enemies': enemies_state}
        print("Serializing game state:", game_state)
        return game_state

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using AES encryption.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using AES decryption.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

    def save_game(self):
        """
        Save the encrypted game state to a file.
        """
        try:
            state = json.dumps(self.serialize_game_state())
            encrypted_data = self.encrypt(state)
            with open(self.filename, 'wb') as f:
                f.write(self.iv)
                f.write(encrypted_data)
                f.flush()
            print("Game saved securely.")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        """
        Load and decrypt the game state from a file.
        """
        try:
            with open(self.filename, 'rb') as f:
                iv = f.read(AES.block_size)
                encrypted_data = f.read()
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
                decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
                self.deserialize_game_state(json.loads(decrypted_data))
            print("Game loaded securely.")
        except Exception as e:
            print(f"Failed to load game: {e}")

    def deserialize_game_state(self, state):
        """
        Deserialize the game state from a dictionary and apply it to the game.
        """
        self.game.player.pos = state['player']['position']
        self.game.health.current_health = state['player']['health']

        self.game.enemy = []
        for enemy_data in state['enemies']:
            enemy_class = getattr(sys.modules[__name__], enemy_data['type'])
            enemy = enemy_class(self.game, pos=enemy_data['position'])
            self.game.enemy.append(enemy)
