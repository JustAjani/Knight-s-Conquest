import sqlite3
import json
import os
import firebase_admin
from firebase_admin import credentials, db
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Enemies.Goblin import Goblin
from Enemies.Mushroom import Mushroom
from Enemies.FlyingEye import FlyingEye
from Enemies.BaseEnemy import Enemy  
class GameSaver:
    def __init__(self, game, path='game_states/default_save', key=None):
        """
        Initializes a new instance of the GameSaver class.

        Args:
            game (object): The game object to save.
            path (str, optional): The path of the game state in Firebase. Defaults to 'game_states/default_save'.
            key (bytes, optional): The encryption key for the game state. If not provided, a random key will be generated. Defaults to None.

        Returns:
            None
        """
        self.game = game
        self.db_path = path
        self.key = key if key else os.urandom(16)
        self.iv = os.urandom(AES.block_size)
        self.db_ref = db.reference(self.db_path)
        self.local_db_path = 'local_game_state.db'
        self.init_local_db()

    def init_local_db(self):
        """
        Initialize or create the local database and table.
        """
        conn = sqlite3.connect(self.local_db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS game_state
                          (id INTEGER PRIMARY KEY, iv TEXT, data TEXT)''')
        conn.commit()
        conn.close()

    def serialize_game_state(self):
        """
        Serializes the game state into a JSON string.

        Returns:
            str: The serialized game state in JSON format.
        """
        player_state = {
            'position': self.game.player.pos,
            'health': self.game.health.current_health
        }
        enemies_state = [
            {'type': enemy.__class__.__name__,
            'position': enemy.pos,
            'size': enemy.size,  # Ensure this is an attribute of your enemy objects
            }
            for enemy in self.game.enemies
        ]
        game_state = {'player': player_state, 'enemies': enemies_state}
        return json.dumps(game_state)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using AES encryption.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))

    def save_game(self):
        """
        Save the encrypted game state to Firebase and local SQLite database.
        """
        try:
            state = self.serialize_game_state()
            encrypted_data = self.encrypt(state)
            # Save to Firebase
            self.db_ref.set({
                'iv': self.iv.hex(),
                'data': encrypted_data.hex()
            })
            # Save locally
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO game_state (iv, data) VALUES (?, ?)",
                           (self.iv.hex(), encrypted_data.hex()))
            conn.commit()
            conn.close()
            print("Game saved securely to Firebase and locally.")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self, from_local=False):
        """
        Load and decrypt the game state from Firebase or local database.
        """
        try:
            if from_local:
                conn = sqlite3.connect(self.local_db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT iv, data FROM game_state ORDER BY id DESC LIMIT 1")
                saved_data = cursor.fetchone()
                conn.close()
                if saved_data:
                    iv, data = saved_data
                    iv = bytes.fromhex(iv)
                    encrypted_data = bytes.fromhex(data)
            else:
                saved_data = self.db_ref.get()
                if saved_data:
                    iv = bytes.fromhex(saved_data['iv'])
                    encrypted_data = bytes.fromhex(saved_data['data'])

            decrypted_data = self.decrypt(encrypted_data, iv)
            self.deserialize_game_state(decrypted_data)
            print("Game loaded securely.")
        except Exception as e:
            print(f"Failed to load game: {e}")
    
    def delete_game(self):
        """
        Delete the game state from Firebase and the local SQLite database.
        """
        try:
            # Delete from Firebase
            self.db_ref.delete()

            # Delete locally
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM game_state")  # This deletes all entries; adjust if needed
            conn.commit()
            conn.close()

            print("Game state deleted from Firebase and locally.")
        except Exception as e:
            print(f"Error deleting game: {e}")

    def decrypt(self, ciphertext, iv):
        """
        Decrypt the ciphertext using AES decryption.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

    def deserialize_game_state(self, state_json):
        state = json.loads(state_json)
        self.game.player.pos = state['player']['position']
        self.game.health.current_health = state['player']['health']
        self.game.enemies.clear()

        for enemy_data in state['enemies']:
            enemy_class = None
            if enemy_data['type'] == 'Goblin':
                enemy_class = Goblin
            elif enemy_data['type'] == 'Mushroom':
                enemy_class = Mushroom
            elif enemy_data['type'] == 'FlyingEye':
                enemy_class = FlyingEye
            elif enemy_data['type'] == 'Enemy':  # Base class, if needed
                enemy_class = Enemy

            if enemy_class:
                enemy = enemy_class(self.game,
                                    pos=enemy_data['position'],
                                    size=enemy_data['size'])  # Handle optional parameters
                self.game.enemies.append(enemy)


