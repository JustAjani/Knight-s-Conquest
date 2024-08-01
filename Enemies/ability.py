import pygame

class Ability:
    def __init__(self, game, name, description, effect, size, pos):
        self.game = game
        self.name = name
        self.description = description
        self.effect = effect
        self.size = list(size)
        self.pos = list(pos)
        self.abilityRect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.animation_speed = 0.1
        self.animations =  {
            "M_shoot": self.game.assetManager.get_asset('M_Projectile'),
            "FE_shoot": self.game.assetManager.get_asset('FE_Projectile'),
            "Bomb": self.game.assetManager.get_asset('Bomb'),
            "Sword": self.game.assetManager.get_asset('Sword'),
            "Fireball": self.game.assetManager.get_asset('Fireball'),
        }
        self.frame_index = 0
        self.current_animation = 'M_shoot'
        self.last_update = pygame.time.get_ticks()
        self.image = pygame.transform.scale(self.animations[self.current_animation][self.frame_index], self.size)

        # Counting attacks
        self.attack_counter = 0

    def update(self):
        self.animation_update()

    def animation_update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > int(1000 * self.animation_speed):
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_animation])
            self.image = pygame.transform.scale(self.animations[self.current_animation][self.frame_index], self.size)

    def trigger_ability(self):
        self.attack_counter += 1
        if self.attack_counter == 3:
            self.activate_ability()
            self.attack_counter = 0  # Reset counter after the ability is triggered

    def activate_ability(self):
        # Set the current animation to the ability's effect
        self.current_animation = self.effect
        print(f"{self.name} ability activated!")

# This Ability class now includes an attack counter that increments with each attack. 
# The ability is triggered on the 3rd attack, which can be used to activate a specific animation or effect.
