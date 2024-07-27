import firebase_admin
from firebase_admin import credentials, db
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import sys
import json
import os

# Initialize Firebase
cred = credentials.Certificate('JSON/knight-s-conquest-firebase-adminsdk-cn4w0-1488726de2.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://knight-s-conquest-default-rtdb.firebaseio.com'
})

class GameSaver:
    def __init__(self, game, path='game_states/default_save', key=None):
        """
        Initialize the GameSaver with game reference, database path, and encryption key.
        """
        self.game = game
        self.db_path = path
        self.key = key if key else os.urandom(16)
        self.iv = os.urandom(AES.block_size)
        self.db_ref = db.reference(self.db_path)

    def serialize_game_state(self):
        """
        Serialize the game state to a dictionary.
        """
        player_state = {
            'position': self.game.player.pos,
            'health': self.game.health.current_health
        }
        enemies_state = [ {'type': enemy.__class__.__name__, 'position': enemy.pos} for enemy in self.game.enemy ]
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
        Save the encrypted game state to Firebase.
        """
        try:
            state = json.dumps(self.serialize_game_state())
            encrypted_data = self.encrypt(state)
            self.db_ref.set({
                'iv': self.iv.hex(),
                'data': encrypted_data.hex()
            })
            print("Game saved securely to Firebase.")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        """
        Load and decrypt the game state from Firebase.
        """
        try:
            saved_data = self.db_ref.get()
            if saved_data:
                iv = bytes.fromhex(saved_data['iv'])
                encrypted_data = bytes.fromhex(saved_data['data'])
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
                decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
                self.deserialize_game_state(json.loads(decrypted_data))
            print("Game loaded securely from Firebase.")
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

