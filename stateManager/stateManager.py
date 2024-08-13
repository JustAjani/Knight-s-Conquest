import random
import threading
import pygame

class State:
    def __init__(self, enemy):
        """
        Initializes a new instance of the State class.

        Parameters:
            enemy (Enemy): The enemy object to associate with the state.

        Returns:
            None
        """
        self.enemy = enemy
        self.deltaTime = pygame.time.Clock().tick(60) / 1000

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass

class PatrolState(State):
    def enter(self):
        """
        Set the current animation of the enemy to "run" and reset the frame index to 0.
        Print the message "Entering Patrol State" to indicate that the enemy has entered the patrol state.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        self.enemy.currentAnimation = "run"
        self.enemy.frameIndex = 0
        print("Entering Patrol State")

    def execute(self):
        # Start patrol in a separate thread
        patrol_thread = threading.Thread(target=self.handle_patrol)
        patrol_thread.start()

    def handle_patrol(self):
        # Patrol logic
        self.enemy.patrol()

    def exit(self):
        print("Exiting Patrol State")

class ChaseState(State):
    def enter(self):
        """
        Enter the current state.

        This method is called when the enemy enters the current state. It prints a message indicating the state being entered.
        It sets the enemy's current animation to "run" if the current state is PatrolState, otherwise it sets it to "attack".
        It resets the enemy's frame index to 0.
        It updates the enemy's animation.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        print(f"Entering {type(self).__name__} state")
        self.enemy.currentAnimation = "run" if type(self).__name__ == "PatrolState" else "attack"
        self.enemy.frameIndex = 0
        self.enemy.animationUpdate()  # Ensure the animation is updated immediately

    def execute(self):
        # Start chase in a separate thread
        chase_thread = threading.Thread(target=self.handle_chase)
        chase_thread.start()

    def handle_chase(self):
        # Chase logic
        self.enemy.chase(self.enemy.game.player)

    def exit(self):
        print("Exiting Chase State")

class AttackState(State):
    def enter(self):
        self.enemy.currentAnimation = "attack"
        self.enemy.frameIndex = 0
        print("Entering Attack State")

    def execute(self):
        # Start attack in a separate thread
        attack_thread = threading.Thread(target=self.handle_attack)
        attack_thread.start()

    def handle_attack(self):
        # Attack logic
        self.enemy.attack(self.enemy.game.player)

    def exit(self):
        print("Exiting Attack State")
    
class FleeState:
        def __init__(self, enemy):
            self.enemy = enemy
        
        def enter(self):
            self.enemy.currentAnimation = "run"  # Assuming the run animation shows the enemy in a fleeing state
            # self.enemy.audio_player.enqueue_sound(self.enemy.audio_player.fearSound)  # Play a fear sound if available
            self.enemy.frameIndex = 0
            print("Entering Flee State")

        def execute(self):
            flee_thread = threading.Thread(target=self.handle_flee)
            flee_thread.start()
        
        def handle_flee(self):
            self.enemy.flee()

        def exit(self):
            pass  # Clean up any flee-specific settings if needed

class DamageState:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self):
        self.enemy.currentAnimation = "hit"
        self.enemy.frameIndex in [1,3]
        print("Entering Damage State")

    def execute(self):
        damage_thread = threading.Thread(target=self.handle_damage)
        damage_thread.start()

    def handle_damage(self):
        self.enemy.attacked = True

    def exit(self):
        print("Exiting Damage State")

class FlyingEyePatrolState(State):
    def enter(self):
        """
        Enter the current state.

        This method is called when the enemy enters the current state. It calls the parent class's enter method using super(). It sets the enemy's current animation to "run". It also sets a new target y within bounds for the enemy's movement. The target y is randomly generated within the range of 0 to the enemy's SCREENH minus the enemy's size in the y-direction.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        super().enter()
        self.enemy.currentAnimation = "run" 
        # Set a new target y within bounds
        self.enemy.target_y = random.randint(0, self.enemy.SCREENH - self.enemy.size[1])

    def execute(self):
        """
        Executes the current state of the enemy.

        This method updates the enemy's position based on its current position and target y-coordinate. If the enemy's y-coordinate is less than its target y-coordinate, it moves down towards the target y-coordinate. If the enemy's y-coordinate is greater than its target y-coordinate, it moves up towards the target y-coordinate. If the enemy's y-coordinate reaches the target y-coordinate, it changes the state to 'flying_eye_patrol'.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        self.enemy.enemy_rect.y = self.enemy.pos[0]
        self.enemy.enemy_rect.x = self.enemy.pos[1]

        if self.enemy.enemy_rect.y < self.enemy.target_y:
            self.enemy.enemy_rect.y += self.enemy.speed * self.deltaTime  # Adjust this calculation
            print(f"Moving down to target. New y: {self.enemy.enemy_rect.y}")
        elif self.enemy.enemy_rect.y > self.enemy.target_y:
            self.enemy.enemy_rect.y -= self.enemy.speed * self.deltaTime  # Adjust this calculation
            print(f"Moving up to target. New y: {self.enemy.enemy_rect.y}")
        else:
            print("Target Y reached, changing state.")
            self.enemy.change_state('flying_eye_patrol')

    def exit(self):
        super().exit()

class FlyingEyeAttackState(State):
    def enter(self):
        """
        Enter the current state.

        This method is called when the enemy enters the current state. It calls the parent class's enter method using super(). It sets the enemy's current animation to "attack" and resets the frame index to 0.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        super().enter()
        self.enemy.currentAnimation = "attack"
        self.enemy.frameIndex = 0

    def execute(self):
        """
        Executes the attack state for the flying eye enemy.

        This method assumes that the attack involves some sort of dive or projectile. It calls the `attack` method on the `enemy` object, passing in the `game.player` object as the target. After the attack is completed, it checks if the enemy is still attacking by calling the `is_attacking` method on the `enemy` object. If the enemy is not attacking, it changes the state of the enemy to `'flying_eye_patrol'` by calling the `change_state` method on the `state_machine` object of the `enemy`.

        Parameters:
            self (FlyingEyeAttackState): The instance of the `FlyingEyeAttackState` class.

        Returns:
            None
        """
        # Assume the attack involves some sort of dive or projectile
        self.enemy.attack(self.enemy.game.player)
        # Check if attack is completed
        if not self.enemy.is_attacking:
            self.enemy.state_machine.change_state('flying_eye_patrol')

    def exit(self):
        super().exit()
        self.enemy.currentAnimation = "idle"

class SpecialGoblinAttackState(AttackState):
    def execute(self):
        self.enemy.goblin_attack()

class SpecialMushroomAttackState(AttackState):
    def execute(self):
        self.enemy.mushroom_attack()

class MemoryPatrolState(State):
    def __init__(self, enemy):
        self.enemy = enemy
        self.patrol_time = 5000  # Time in milliseconds to patrol last known position
        self.start_patrol_time = pygame.time.get_ticks()

    def enter(self):
        self.target_pos = self.enemy.last_known_player_pos

    def execute(self):
        if self.target_pos is not None:
            # Move towards the last known player position
            if self.enemy.enemy_rect.x < self.target_pos[0]:
                self.enemy.enemy_rect.x += self.enemy.adjustedspeed
                self.enemy.flip = False
            elif self.enemy.enemy_rect.x > self.target_pos[0]:
                self.enemy.enemy_rect.x -= self.enemy.adjustedspeed
                self.enemy.flip = True

            # Check if reached or close to last known position
            if abs(self.enemy.enemy_rect.x - self.target_pos[0]) < 10:
                self.enemy.patrol()
            
            # Check if patrol time has elapsed
            if pygame.time.get_ticks() - self.start_patrol_time > self.patrol_time:
                self.enemy.last_known_player_pos = None  # Reset memory
                self.enemy.state_machine.change_state('patrol')  # Change state to normal patrol

    def exit(self):
        pass

    def patrol_around_last_known_position(self):
        # Implement logic to patrol around this area
        pass


class StateMachine:
    def __init__(self, enemy):
        self.enemy = enemy
        self.states = {}
        self.current_state = None
        self.last_state_change_time = 0
        self.state_change_delay = 2000

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, new_state):
        current_time = pygame.time.get_ticks()
        if self.current_state != new_state and (current_time - self.last_state_change_time > self.state_change_delay):
            if self.current_state:
                self.current_state.exit()
            self.current_state = self.states[new_state]
            self.current_state.enter()
            self.last_state_change_time = current_time

    def update(self):
        if self.current_state:
            self.current_state.execute()


