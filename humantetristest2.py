from nes_py.wrappers import JoypadSpace
import gym_tetris
from gym_tetris.actions import MOVEMENT
import pygame
import keyboard
from keyboard import is_pressed
from keyboard import on_release_key
from keyboard import on_press_key

env = gym_tetris.make('TetrisA-v0')
env = JoypadSpace(env, MOVEMENT)
# button_map = {
#         'right' | left B:  0b10000000, 8 rotates left
#         'left' A:   0b01000000, 7 rotates left
#         'down':   0b00100000, 6 moves left
#         'up':     0b00010000, 5 rotates right or left
#         'start':  0b00001000, 4 rotates right or left
#         'select' right: 0b00000100, 3 moves right
#         'B':      0b00000010, 2 rotates counter-clockwise
#         'A':      0b00000001, 1 rotates clockwise
#         'NOOP':   0b00000000, 0
#     }
#
#   up: X
#   down: X
#   move left: 6
#   move right: 3
#   rotate left: 7
#   rotate right: 4
#   rotate 90 clockwise: 1
#   rotate 90 counter-clockwise: 2

action = 0
class Input:
    def __init__(self):
        print('initialized')

        global action
        action = 0

        self.spacebar_pressed = False # uhhh there's no hard drop, or drop, so this will be either useless or removed
        self.leftarrow_pressed = False # move left | left | 6
        self.rightarrow_pressed = False # move right | right | 3
        self.z_pressed = False # rotates counter-clockwise | B | 2
        self.x_pressed = False # rotates clockwise | A | 1
        # self.c_pressed = False # rotate left
        # self.v_pressed = False # rotate right


    def get_action(self):
        global action
        return action


    def handle_spacebar(self):
        self.spacebar_pressed = True
        print("spacebar pressed")

    def handle_leftarrow(self):
        self.leftarrow_pressed = True
        print("leftarrow pressed")

    def handle_rightarrow(self):
        self.rightarrow_pressed = True
        print("rightarrow pressed")

    def handle_z(self):
        self.z_pressed = True
        print("z pressed")

    def handle_x(self):
        self.x_pressed = True
        print("x pressed")

    def take_action(self):
        if self.spacebar_pressed:
            global action
            action = 9
            self.spacebar_pressed = False
        elif self.leftarrow_pressed:
            action = 6
            self.leftarrow_pressed = False
        elif self.rightarrow_pressed:
            action = 3
            self.rightarrow_pressed = False
        elif self.z_pressed:
            action = 2
            self.z_pressed = False
        elif self.x_pressed:
            action = 1
            self.x_pressed = False
        else:
            action = 0
        return action


hasRunned_Space = False
hasRunned_LeftArrow = False
hasRunned_RightArrow = False
hasRunned_z = False
hasRunned_x = False
done = True
input1 = Input()

for step in range(500000):
    if done:
        state = env.reset()

    if is_pressed('space') and hasRunned_Space is False:
        input1.handle_spacebar()
        hasRunned_Space = True
    elif is_pressed('space') is False:
        hasRuhasRunned_Spacenned = False

    if is_pressed('left') and hasRunned_LeftArrow is False:
        input1.handle_leftarrow()
        hasRunned_LeftArrow = True
    elif is_pressed('left') is False:
        hasRunned_LeftArrow = False

    if is_pressed('right') and hasRunned_RightArrow is False:
        input1.handle_rightarrow()
        hasRunned_RightArrow = True
    elif is_pressed('right') is False:
        hasRunned_RightArrow = False

    if is_pressed('x') and hasRunned_x is False:
        input1.handle_x()
        hasRunned_x = True
    elif is_pressed('x') is False:
        hasRunned_x = False

    if is_pressed('z') and hasRunned_z is False:
        input1.handle_z()
        hasRunned_z = True
    elif is_pressed('z') is False:
        hasRunned_z = False


    currentAction = input1.take_action()
    print(currentAction)
    state, reward, done, info = env.step(currentAction)
    print(info['number_of_lines'])
    if info['number_of_lines'] == 10:
        env.close()

    env.render()



env.close()