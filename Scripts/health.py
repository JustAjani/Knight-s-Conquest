import pygame

class Health:
    def __init__(self, game, x, y, width, height, max_health, bg_color=(255, 0, 0), fg_color=(0, 255, 0), border_color=(255, 255, 255), border_width=2):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.border_color = border_color
        self.border_width = border_width

    def update_health(self, change):
        """ Update the health by a specified change amount. """
        self.current_health = max(0, min(self.current_health + change, self.max_health))
    
    def apply_decay(self, decay_rate):
        """Apply a decay to the health over time."""
        self.update_health(-decay_rate)

    def render(self):
        """ Render the health bar directly on the game's main screen. """
        health_percentage = self.current_health / self.max_health
        current_width = int(self.width * health_percentage)

        # Draw the background (empty part of the health bar)
        pygame.draw.rect(self.game.screen, self.bg_color, (self.x, self.y, self.width, self.height))

        # Draw the foreground (filled part of the health bar)
        pygame.draw.rect(self.game.screen, self.fg_color, (self.x, self.y, current_width, self.height))

        # Draw a border around the health bar, if needed
        if self.border_width > 0:
            pygame.draw.rect(self.game.screen, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)
        
         # Debugging text
        debug_font = pygame.font.Font(None, 30)  # Adjust size as necessary
        debug_text = debug_font.render(f'Health: {self.current_health}/{self.max_health}', True, (255, 255, 255))
        self.game.screen.blit(debug_text, (self.x, self.y - 30))  # Adjust position as necessary
