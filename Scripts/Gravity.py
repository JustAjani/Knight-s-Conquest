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
    
    def check_platform_collision(self, entity, platforms):
        entity.grounded = False
        for platform in platforms:
            if entity.pos[1] + entity.size[1] > platform.pos[1] and \
            entity.pos[0] + entity.size[0] > platform.pos[0] and \
            entity.pos[0] < platform.pos[0] + platform.size[0]:
                if entity.velocity_y >= 0:  # Only stop the fall if moving downward
                    entity.pos[1] = platform.pos[1] - entity.size[1]
                    entity.velocity_y = 0
                    entity.grounded = True
                    break  # No need to check further platforms

    

