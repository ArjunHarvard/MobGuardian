# ##############################
# # Title: Pygame Interface
# # Desc: Use Pygame to pass key inputs to drone
# # Source: "Murtaza's Workshop"
# # Modified: Arjun Singh
# ##############################

import pygame


def init():
    """Initialize pygame"""
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def get_key(key_name):
    """Check pygame to see if key 'key_name' has been pressed"""
    ans = False
    for eve in pygame.event.get():
        pass

    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame, "K_{}".format(key_name))

    if key_input[my_key]:
        ans = True
        print("K_{}".format(key_name))

    pygame.display.update()
    return ans
