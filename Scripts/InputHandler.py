import pygame

class InputHandler:
    def __init__(self, key_map):
        self.key_map = key_map

    def get_input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()  # Get mouse button states
        
        # You can map mouse buttons directly or use them for specific actions
        return {
            'move_left': keys[self.key_map['left']],
            'move_right': keys[self.key_map['right']],
            'jump': keys[self.key_map['jump']],
            'attack1': keys[self.key_map['attack1']],
            'attack2': keys[self.key_map['attack2']],
            'left_click': mouse_buttons[0],  # Left mouse button
            'right_click': mouse_buttons[2]  # Right mouse button
        }

