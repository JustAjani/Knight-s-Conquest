import random
import pygame

class State:
    def __init__(self, enemy):
        self.enemy = enemy

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
        self.enemy.chase(self.enemy.game.player)

    def exit(self):
        print("Exiting Chase State")

class AttackState(State):
    def enter(self):
        self.enemy.currentAnimation = "attack"
        self.enemy.frameIndex = 0
        print("Entering Attack State")

    def execute(self):
        self.enemy.attack(self.enemy.game.player)

    def exit(self):
        print("Exiting Attack State")

class FlyingEyePatrolState(State):
    def enter(self):
        super().enter()
        self.enemy.currentAnimation = "run"
        # Set a new target y within bounds
        self.enemy.target_y = random.randint(0, self.enemy.SCREENH - self.enemy.size[1])

    def execute(self):
        # Move vertically towards target_y
        if self.enemy.enemy_rect.y < self.enemy.target_y:
            self.enemy.enemy_rect.y += self.enemy.speed
        elif self.enemy.enemy_rect.y > self.enemy.target_y:
            self.enemy.enemy_rect.y -= self.enemy.speed
        else:
            # Target reached, pick a new target
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
        self.enemy.flying_eye_attack()
        # Check if attack is completed
        if not self.enemy.is_attacking:
            self.enemy.change_state('flying_eye_patrol')

    def exit(self):
        super().exit()
        self.enemy.currentAnimation = "idle"

class SpecialGoblinAttackState(AttackState):
    def execute(self):
        self.enemy.goblin_attack()

class SpecialMushroomAttackState(AttackState):
    def execute(self):
        self.enemy.mushroom_attack()

class StateMachine:
    def __init__(self, enemy):
        self.enemy = enemy
        self.states = {}
        self.current_state = None
        self.last_state_change_time = 0
        self.state_change_delay = 2000  # Delay in milliseconds

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


