class Gravity:
    def __init__(self, gravity=9.81, max_fall_speed=400):
        """
        Initializes the Gravity object.

        Args:
            gravity (float, optional): The acceleration due to gravity. Defaults to 9.81.
            max_fall_speed (float, optional): The maximum speed at which the object can fall. Defaults to 400.

        Returns:
            None
        """
        self.gravity = gravity
        self.max_fall_speed = max_fall_speed

    def apply(self, entity, deltaTime):
        """
        Applies gravity to the entity and updates its position based on velocity.

        Args:
            entity (Entity): The entity to apply gravity to.
            deltaTime (float): The time elapsed since the last frame.

        Returns:
            None
        """
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
        """
        Makes the entity jump by applying a vertical velocity to it.

        Args:
            entity (Entity): The entity to jump.
            jump_strength (float): The strength of the jump, determines how high the entity jumps.

        Returns:
            None
        """
        if entity.grounded:  # Can only jump if on the ground
            entity.velocity_y = -jump_strength  # Negative to move up
            entity.grounded = False
    
    def check_platform_collision(self, entity, platforms):
        """
        Checks for collision between the entity and the platforms.

        Args:
            entity (Entity): The entity to check collision for.
            platforms (List[Platform]): The list of platforms to check collision against.

        Returns:
            None
        """
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

    

