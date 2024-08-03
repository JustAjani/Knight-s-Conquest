import pygame
from Enemies.BaseEnemy import Enemy

class FireWorm(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        
        # Define animations specific to FireWorm
        self.animations = {
            "idle": game.assetManager.get_asset('worm_idle'),
            "run": game.assetManager.get_asset('worm_walk'),
            "death": game.assetManager.get_asset('worm_death'),
            "attack": game.assetManager.get_asset('worm_attack'),
        }

        # Adjusted attributes for the FireWorm
        self.speed = 70
        self.move_distance = 80
        self.name = "fireworm"
        self.attack_cooldown = 5000  # 5 seconds cooldown for attacks
        self.last_attack_time = pygame.time.get_ticks() - self.attack_cooldown  # Allow immediate attack on spawn
        self.update_image()

    def update_image(self):
        """
        Updates the image of the object based on the current animation and frame index.

        This function checks if the frame index is within the range of the current animation. If it is, it scales and sets the image of the object to the corresponding frame. It also prints the current animation and frame index.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        if self.frameIndex < len(self.animations[self.currentAnimation]):
            self.image = pygame.transform.scale(self.animations[self.currentAnimation][self.frameIndex], self.size)
            print(f"Current Animation: {self.currentAnimation}, Frame Index: {self.frameIndex}")
        else:
            print(f"Error: Frame index out of range for animation {self.currentAnimation}")

    def update(self, deltaTime, player,all_enemies):
        """
        Updates the object's animation and image based on the time elapsed.

        Args:
            deltaTime (float): The time elapsed since the last update.
            player (Player): The player object for collision detection.

        Returns:
            None

        This function updates the object's animation and image based on the time elapsed. It first calls the update method of the parent class to update the object's position and state. Then, it checks if enough time has passed since the last update. If enough time has passed, it increments the frame index modulo the length of the current animation, updates the last update time, and calls the update_image method to update the object's image.
        """
        super().update(deltaTime, player,all_enemies)
        current_time = pygame.time.get_ticks()
        if current_time - self.lastUpdate > 1000 * self.animationSpeed:
            self.frameIndex = (self.frameIndex + 1) % len(self.animations[self.currentAnimation])
            self.lastUpdate = current_time
            self.update_image()

        

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            super().attack(player)  # Implement the attack logic from the base class
            attack = self.audio_player.enqueue_sound(self.audio_player.wormAttack)
            if self.audio_player.get_channel(2):
                self.audio_player.enqueue_sound(attack)
            self.last_attack_time = current_time
            print("FireWorm has attacked!")

