import random
import threading
import pygame
from concurrent.futures import ThreadPoolExecutor


class State:
    def __init__(self, enemy):
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

class AttackState:
    def __init__(self, enemy):
        self.enemy = enemy
        self.has_attacked = False  # This flag will check if an attack has been made during this state entry

    def enter(self):
        self.enemy.currentAnimation = "attack"
        self.enemy.frameIndex = 0
        self.has_attacked = False  # Reset the flag when entering the state
        print("Entering Attack State")

    def execute(self):
        if not self.has_attacked:  # Only execute attack logic once per state entry
            self.draw_attack_rays()
            self.handle_attack()
        # Could also include logic here to transition out of attack state if conditions are met

    def draw_attack_rays(self):
        ray_length = 50
        ray_start = (self.enemy.pos[0] + self.enemy.size[0] // 2, self.enemy.pos[1] + self.enemy.size[1] // 2)
        rays = [
            ((ray_start[0], ray_start[1] - 10), (ray_start[0] - ray_length, ray_start[1] - 10) if self.enemy.flip else (ray_start[0] + ray_length, ray_start[1] - 10)),
            (ray_start, (ray_start[0] - ray_length, ray_start[1]) if self.enemy.flip else (ray_start[0] + ray_length, ray_start[1])),
            ((ray_start[0], ray_start[1] + 10), (ray_start[0] - ray_length, ray_start[1] + 10) if self.enemy.flip else (ray_start[0] + ray_length, ray_start[1] + 10))
        ]
        for start, end in rays:
            pygame.draw.line(self.enemy.game.screen, (255, 0, 0), start, end, 3)

    def handle_attack(self):
        self.enemy.attack(self.enemy.game.player)
        if self.line_rect_collision(self.enemy, self.enemy.game.player.rect) and not self.enemy.game.player.attacked:
            direction_multiplier = -1 if self.enemy.flip else 1
            knockback_distance = random.randint(20, 60)
            self.enemy.game.player.pos[0] += knockback_distance * direction_multiplier
            self.enemy.game.player.attacked = True
            damage = 20
            self.enemy.game.player.health.apply_decay(damage)
            print(f"Player hit with attack, knockback {knockback_distance}, damage {damage}.")
            self.has_attacked = True  # Set the flag indicating that an attack has been made

    def line_rect_collision(self, attacker, target_rect):
        attack_rect = pygame.Rect(attacker.pos[0], attacker.pos[1], 50, 50)
        return attack_rect.colliderect(target_rect)

    def exit(self):
        print("Exiting Attack State")
        self.enemy.game.player.attacked = False  # Ensure to reset the attacked flag when exiting the state

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


class DamageState():
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self):
        self.enemy.currentAnimation = "hit"
        self.enemy.frameIndex = 0
        self.time_in_state = 0
        self.start_time = pygame.time.get_ticks() / 1000.0  
        print("Entering Damage State")

    def execute(self):
        # Start the damage handling in a separate thread
        damage_thread = threading.Thread(target=self.handle_damage)
        damage_thread.start()

    def handle_damage(self):
        while self.time_in_state < 0.4:  
            current_time = pygame.time.get_ticks() / 1000.0
            self.time_in_state = current_time - self.start_time  
            pygame.time.wait(10) 

        self.exit()

    def exit(self):
        print("Exiting Damage State")
        self.enemy.attacked = False  
        # self.enemy.state_machine.change_state('patrol')  

class DeathState():
    def __init__(self, enemy, game):
        self.enemy = enemy
        self.game = game
        self.deltaTime = pygame.time.Clock().tick(60) / 1000
        self.animation_complete = False
        self.lock = threading.Lock()  

    def enter(self):
        self.enemy.currentAnimation = "death"
        self.enemy.frameIndex in [0,5]
        self.time_in_state = 0.4
        print("Entering Death State")

    def execute(self):
        death_thread = threading.Thread(target=self.handle_death)
        death_thread.start()

    def handle_death(self):
        start_time = pygame.time.get_ticks() / 1000.0  # get current time in seconds
        while not self.animation_complete:
            with self.lock:
                current_time = pygame.time.get_ticks() / 1000.0  # update current time
                if current_time - start_time >= self.time_in_state:
                    self.animation_complete = True
                    self.mark_enemy_dead()

        if self.animation_complete:
            self.remove_enemy()

    def mark_enemy_dead(self):
        if not self.enemy.dead:
            self.enemy.dead = True

    def remove_enemy(self):
        with self.lock:
            if self.enemy.dead and self.animation_complete:
                # Directly remove the specific enemy without additional checks
                if self.enemy in self.game.enemies:
                    self.game.enemies.remove(self.enemy)
                self.exit()

    def exit(self):
        print("Exiting Death State")

class FlyingEyePatrolState(State):
    def enter(self):
        super().enter()
        self.enemy.currentAnimation = "run" 
        # Set a new target y within bounds
        self.enemy.target_y = random.randint(0, self.enemy.SCREENH - self.enemy.size[1])

    def execute(self):
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
        super().enter()
        self.enemy.currentAnimation = "attack"
        self.enemy.frameIndex = 0

    def execute(self):
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
        self.is_changing_state = False

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, new_state):
        if not self.is_changing_state:
            self.is_changing_state = True

            # Check if the new state exists, default to 'patrol' if not found
            if new_state not in self.states:
                print(f"State '{new_state}' not found. Defaulting to 'patrol'.")
                new_state = 'patrol'

            if self.current_state:
                self.current_state.exit()

            # Set the current state to the new state if it exists, otherwise default to 'patrol'
            self.current_state = self.states.get(new_state, self.states['patrol'])
            self.current_state.enter()

            self.is_changing_state = False

    def update(self):
        if self.current_state:
            self.current_state.execute()






