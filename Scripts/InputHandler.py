import pygame

class InputHandler:
    def __init__(self, key_map):
        """
        Initializes the InputHandler object with the given key_map.

        Parameters:
            key_map (dict): A dictionary mapping key names to their corresponding key codes.

        Returns:
            None
        """
        self.key_map = key_map

    def get_input(self):
        """
        Returns a dictionary of input states based on the current state of the keyboard and mouse.

        :return: A dictionary with the following keys:
                 - 'move_left': Boolean indicating if the left arrow key is pressed.
                 - 'move_right': Boolean indicating if the right arrow key is pressed.
                 - 'jump': Boolean indicating if the space key is pressed.
                 - 'attack1': Boolean indicating if the first attack key is pressed.
                 - 'attack2': Boolean indicating if the second attack key is pressed.
                 - 'left_click': Boolean indicating if the left mouse button is pressed.
                 - 'right_click': Boolean indicating if the right mouse button is pressed.
        """
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

class DummyInputHandler:
    def get_input(self):
        return {
            'move_left': False,
            'move_right': False,
            'jump': False,
            'attack1': False,
            'attack2': False
        }

