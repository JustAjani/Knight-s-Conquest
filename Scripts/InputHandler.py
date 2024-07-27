import pygame

class InputHandler:
    def __init__(self, key_map):
        pygame.joystick.init()  # Initialize the joystick module
        self.key_map = key_map
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()  # Initialize each joystick

    def get_input(self):
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
            XBOX_JUMP = joystick.get_button(0)  # Get jump button state
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

