import pygame

class InputHandler:
    def __init__(self, key_map):
        """
        Initializes an instance of the InputHandler class.

        Args:
            key_map (dict): A dictionary that maps keyboard keys to their corresponding actions.

        Initializes the joystick module using pygame.joystick.init().
        Sets the key_map attribute to the provided key_map.
        Creates a list of initialized joystick objects using pygame.joystick.Joystick().
        Initializes each joystick object using the init() method.

        Returns:
            None
        """
        pygame.joystick.init()  # Initialize the joystick module
        self.key_map = key_map
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()  # Initialize each joystick

    def get_input(self):
        """
        Retrieves input from the keyboard and mouse, as well as any connected joysticks.

        Returns:
            dict: A dictionary containing the following keys:
                - 'move_left' (bool): True if the left arrow key or the left mouse button is pressed, False otherwise.
                - 'move_right' (bool): True if the right arrow key or the right mouse button is pressed, False otherwise.
                - 'jump' (bool): True if the space bar key or the X button on the joystick is pressed, False otherwise.
                - 'attack1' (bool): True if the 'A' key or the left mouse button is pressed, False otherwise.
                - 'attack2' (bool): True if the 'D' key or the right mouse button is pressed, False otherwise.
        """
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()  # Get mouse button states
        
        # Keyboard Controlls
        inputs = {
            'move_left': keys[self.key_map['left']],
            'move_right': keys[self.key_map['right']],
            'jump': keys[self.key_map['jump']],
            'attack1': keys[self.key_map['attack1']] or mouse_buttons[0],  # Left mouse button
            'attack2': keys[self.key_map['attack2']] or mouse_buttons[2]  # Right mouse button
        }

        # Joystick Controlls
        for joystick in self.joysticks:
            horizontal_axis = joystick.get_axis(0)  # Get horizontal axis value

            #XBOX Controllers
            XBOX_JUMP = joystick.get_button(0) # Get jump button state
            XBOX_ATT1 = joystick.get_button(1) # Assign 'B' button (button 1) to attack1
            XBOX_ATT2 = joystick.get_button(2) # Assign 'X' button (button 2) to attack2
            
            #PS4 Controllers
            PS_JUMP = joystick.get_button(1)  # 'X' button for jump
            PS_ATT1 = joystick.get_button(2)  # 'Circle' button for primary attack
            PS_ATT2 = joystick.get_button(3)  # 'Triangle' button for secondary attac
             
            inputs['move_left'] |= (horizontal_axis < -0.5)
            inputs['move_right']  |=  (horizontal_axis > 0.5)
            inputs['jump']  |=  XBOX_JUMP or PS_JUMP
            inputs['attack1'] |=  XBOX_ATT1 or PS_ATT1
            inputs['attack2'] |= XBOX_ATT2 or PS_ATT2
        return inputs

class DummyInputHandler:
    def get_input(self):
        return {
            'move_left': False,
            'move_right': False,
            'jump': False,
            'attack1': False,
            'attack2': False
        }

        # Xbox Controller Controls
        # https://www.pygame.org/docs/ref/joystick.html
        # A - 0
        # B - 1
        # X - 2
        # Y - 3
        # LB - 4
        # RB - 5
        # BACK - 6
        # START - 7
        # LT - 8
        # RT - 9
        # DPAD Left - 12
        # DPAD Right - 13
        # DPAD Up - 14
        # DPAD Down - 15
        # Left Analog Button - 16
        # Right Analog Button - 17
        # Left Analog Horizontal - 0
        # Left Analog Vertical - 1
        # Right Analog Horizontal - 2
        # Right Analog Vertical - 3

        # Playstation Controller Controls
        # https://www.pygame.org/docs/ref/joystick.html
        # Square - 0
        # Cross - 1
        # Circle - 2
        # Triangle - 3
        # L1 - 4
        # R1 - 5
        # L2 - 6
        # R2 - 7
        # DPAD Left - 12
        # DPAD Right - 13
        # DPAD Up - 14
        # DPAD Down - 15
        # Left Analog Button - 16
        # Right Analog Button - 17
        # Left Analog Horizontal - 0
        # Left Analog Vertical - 1
        # Right Analog Horizontal - 2
        # Right Analog Vertical - 3
