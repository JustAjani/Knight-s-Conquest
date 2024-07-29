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
            game (object): The game object to be saved.
            path (str, optional): The path to the database where the game state will be stored. Defaults to 'game_states/default_save'.
            key (bytes, optional): The encryption key to be used for encrypting the game state. If not provided, a random 16-byte key will be generated. Defaults to None.

        Returns:
            None
        """
        self.game = game
        self.db_path = path
        self.key = key if key else os.urandom(16)
        self.iv = os.urandom(AES.block_size)
        self.db_ref = db.reference(self.db_path)
        self.local_db_path = 'local_game_state.db'
        self.lock = threading.Lock()
        self.init_local_db()

    def init_local_db(self):
        """
        Initializes a local SQLite database to store game state data.

        This function creates a new SQLite database file at the specified `local_db_path` if it does not already exist. It then creates a table named 'game_state' with three columns: 'id' (primary key), 'iv' (text), and 'data' (text).

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
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
            str: The JSON string representation of the game state.
        """
        player_state = {
            'position': self.game.player.pos,
            'health': self.game.health.current_health
        }
        enemies_state = [
            {'type': enemy.__class__.__name__,
             'position': enemy.pos,
             'size': enemy.size,
             'currentState': type(enemy.state_machine.current_state).__name__}
            for enemy in self.game.enemies
        ]
        audio_state = self.game.audioPlayer.get_audio_state()
        game_state = {'player': player_state, 'enemies': enemies_state, 'audio': audio_state}
        return json.dumps(game_state)

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))

    def save_game(self):
        thread = threading.Thread(target=self._save_game_thread)
        thread.start()

    def _save_game_thread(self):
        """
        Save the game state to Firebase and locally.

        This function saves the game state by serializing it, encrypting it, and storing it in both Firebase and a local SQLite database.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            None
        
        Raises:
            Exception: If an error occurs during the saving process.
        """
        with self.lock:
            try:
                state = self.serialize_game_state()
                encrypted_data = self.encrypt(state)
                self.db_ref.set({
                    'iv': self.iv.hex(),
                    'data': encrypted_data.hex()
                })
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
        Load a saved game from either the local database or the Firebase database.

        Parameters:
            from_local (bool): If True, load the game from the local database. If False, load the game from the Firebase database.

        Returns:
            None

        This function starts a new thread to load a saved game by calling the `_load_game_thread` method with the `from_local` parameter. The game state is loaded from either the local database or the Firebase database based on the value of the `from_local` parameter.

        Note:
            - The `_load_game_thread` method is assumed to be defined elsewhere in the class and is responsible for loading the game state.
            - The `self.lock` context manager is used to ensure thread safety during the loading process.
            - The `self.db_ref` object is assumed to be an instance of a Firebase database reference.
        """
        thread = threading.Thread(target=self._load_game_thread, args=(from_local,))
        thread.start()

    def _load_game_thread(self, from_local):
        """
        Load a saved game from either the local database or the Firebase database.

        Parameters:
            from_local (bool): If True, load the game from the local database. If False, load the game from the Firebase database.

        Returns:
            None

        This function loads a saved game by querying the appropriate database based on the value of the `from_local` parameter.
        If `from_local` is True, it connects to the local database, retrieves the most recent saved game data, and decrypts it.
        The decrypted data is then deserialized and used to restore the game state.
        If `from_local` is False, it retrieves the saved game data from the Firebase database and performs the same decryption and deserialization steps.
        If the game is loaded successfully, a message is printed to indicate that the game was loaded securely.
        If an exception occurs during the loading process, an error message is printed.

        Note:
            - The `self.lock` context manager is used to ensure thread safety during the loading process.
            - The `self.db_ref` object is assumed to be an instance of a Firebase database reference.
            - The `self.deserialize_game_state` method is assumed to be defined elsewhere in the class and is responsible for deserializing the decrypted game data.
            - The `self.decrypt` method is assumed to be defined elsewhere in the class and is responsible for decrypting the game data using the provided IV and cipher.
        """
        with self.lock:
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
        Deletes the game state from both Firebase and the local database.

        This function deletes the game state from the Firebase Realtime Database and the local SQLite database. It first deletes the game state from Firebase using the `delete()` method of the `db_ref` object. Then, it connects to the local SQLite database using the `connect()` method of the `sqlite3` module. It creates a cursor object and executes the SQL query to delete the game state from the `game_state` table using the `execute()` method of the cursor object. After that, it commits the changes to the database using the `commit()` method of the connection object. Finally, it closes the database connection using the `close()` method of the connection object.

        If any exception occurs during the execution of this function, it prints an error message with the exception details.

        Parameters:
            self (GameSaver): The instance of the GameSaver class.

        Returns:
            None
        """
        try:
            self.db_ref.delete()
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM game_state")
            conn.commit()
            conn.close()
            print("Game state deleted from Firebase and locally.")
        except Exception as e:
            print(f"Error deleting game: {e}")

    def decrypt(self, ciphertext, iv):
        """
        Decrypts the given ciphertext using AES encryption with the CBC mode and the provided initialization vector (iv).

        Parameters:
            ciphertext (bytes): The encrypted data to be decrypted.
            iv (bytes): The initialization vector used for decryption.

        Returns:
            str: The decrypted data as a UTF-8 encoded string.

        This function creates a new AES cipher object with the provided key and CBC mode. It then decrypts the ciphertext using the cipher object and the provided initialization vector. The decrypted data is unpadded and decoded as a UTF-8 string.

        Raises:
            ValueError: If the ciphertext is not a multiple of the block size.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

    def deserialize_game_state(self, state_json):
        """
        Deserialize the game state from a JSON string and update the game object accordingly.

        Parameters:
            state_json (str): The JSON string representing the game state.

        Returns:
            None

        This function loads the game state from the given JSON string and updates the game object accordingly. It sets the player's position and health, clears the list of enemies, and recreates the enemies based on the data in the JSON string. The enemies are created using the appropriate enemy class based on the enemy type in the JSON string. The state machine for each enemy is also set up with the appropriate states and the current state is set to the state specified in the JSON string. The audio state of the game is also updated based on the data in the JSON string.

        Note: This function assumes that the necessary enemy classes and state mapping are available in the global scope.
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
                enemy.state_machine = StateMachine(enemy)
                for state_name, state_cls in state_mapping.items():
                    enemy.state_machine.add_state(state_name, state_cls(enemy))
                state_instance = enemy.state_machine.states.get(enemy_data['currentState'], State)
                enemy.state_machine.current_state = state_instance
                enemy.state_machine.current_state.enter()
                self.game.enemies.append(enemy)

        self.game.audioPlayer.set_audio_state(state['audio'])



            

