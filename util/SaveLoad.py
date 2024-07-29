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
from stateManager.stateManager import *
import threading

# Initialize Firebase
cred = credentials.Certificate('JSON/knight-s-conquest-firebase-adminsdk-cn4w0-1488726de2.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://knight-s-conquest-default-rtdb.firebaseio.com'
})

state_mapping = {
    'patrol': PatrolState,
    'chase': ChaseState,
    'attack': AttackState,
    'FlyingEyePatrolState': FlyingEyePatrolState,
    'FlyingEyeAttackState': FlyingEyeAttackState,
    'SpecialGoblinAttackState': SpecialGoblinAttackState,
    'SpecialMushroomAttackState': SpecialMushroomAttackState
}

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
            'currentState': type(enemy.state_machine.current_state).__name__}
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
        Initiate a thread to save the encrypted game state to Firebase and local SQLite database.
        """
        thread = threading.Thread(target=self._save_game_thread)
        thread.start()

    def _save_game_thread(self):
        """
        Save the encrypted game state to Firebase and local SQLite database.
        This function is run in a separate thread to avoid blocking the main game loop.
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
        Initiate a thread to load and decrypt the game state from Firebase or local database.
        """
        thread = threading.Thread(target=self._load_game_thread, args=(from_local,))
        thread.start()

    def _load_game_thread(self, from_local):
        """
        Load and decrypt the game state from Firebase or local database.
        This function is run in a separate thread to avoid blocking the main game loop.
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
        """
        Deserialize the game state from a JSON string and update the game objects accordingly.

        Parameters:
            state_json (str): The JSON string representing the game state.

        Returns:
            None

        This function deserializes the game state from a JSON string and updates the game objects accordingly. It first loads the JSON string into a Python dictionary using the `json.loads()` function. Then, it updates the position of the player object in the game using the 'position' value from the 'player' key in the dictionary. It also updates the current health of the player object using the 'health' value from the 'player' key. After that, it clears the list of enemies in the game.

        Next, it iterates over the 'enemies' key in the dictionary and creates an enemy object based on the 'type' value of each enemy data. It initializes the state machine for each enemy and populates it with all the states defined in the `state_mapping` dictionary. It then dynamically sets the current state of the enemy object using the 'currentState' value from the enemy data. Finally, it appends the enemy object to the list of enemies in the game.

        Note: This function assumes that the `game` object has the necessary attributes and methods to update the game state.
        """
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
            elif enemy_data['type'] == 'Enemy':
                enemy_class = Enemy

            if enemy_class:
                enemy = enemy_class(self.game, pos=enemy_data['position'], size=enemy_data['size'])
                # Initialize the state machine for each enemy
                enemy.state_machine = StateMachine(enemy)
                # Populate all states in the state machine
                for state_name, state_cls in state_mapping.items():
                    enemy.state_machine.add_state(state_name, state_cls(enemy))
                # Dynamically setting current state using a mapping
                state_instance = enemy.state_machine.states.get(enemy_data['currentState'], State)
                enemy.state_machine.current_state = state_instance
                enemy.state_machine.current_state.enter()  # Initialize the state properly
                self.game.enemies.append(enemy)


            

