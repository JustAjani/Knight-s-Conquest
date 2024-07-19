class Gravity:
    def __init__(self, gravity=9.81, max_fall_speed=400):
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed

    def apply(self, entity, deltaTime):
        if not entity.grounded:
            entity.velocity_y += self.gravity * deltaTime
            entity.velocity_y = min(entity.velocity_y, self.max_fall_speed)
        entity.pos[1] += entity.velocity_y * deltaTime

        # Check for ground collisions
        if entity.pos[1] > entity.ground_level:
            entity.pos[1] = entity.ground_level
            entity.velocity_y = 0
            entity.grounded = True

    def jump(self, entity, jump_strength):
        if entity.grounded:  # Can only jump if on the ground
            entity.velocity_y = -jump_strength  # Negative to move up
            entity.grounded = False
