# ##############################
# # Title: Get Keyboard Input
# # Desc: Retrieve Flight Instructions from appropriate system (auto-land, manual, or auto-pilot)
# # Author: Arjun Singh
# ##############################

import math

from mob_guard import globals as sett
from mob_guard.controller.manual_controls import manual
from mob_guard.controller.landing_controls import land
from mob_guard.controller.auto_controls import auto
from mob_guard.controller.other_controls import other


def get_keyboard_input(me):
    """fly drone manually

    Controls:
        "LEFT": strafe left
        "RIGHT": strafe right
        "UP": move forward
        "DOWN": move backward

        "w": increase elevation
        "s": decrease elevation
        "a": rotate counter-clockwise
        "d": rotate clockwise

        "q": land
        "e": takeoff

        "t": auto-landing
        "n": full auto-pilot

        "z": snap a photo
        "c": toggle filter
        "p": print Height | State | Battery
    """
    lr, fb, ud, yv = 0, 0, 0, 0
    d = 0

    if sett.current_state == "manual":
        lr, fb, ud, yv, d = manual(me)

    elif "lz_" in sett.current_state:
        lr, fb, ud, yv = land(me)

    elif "auto_" in sett.current_state:
        lr, fb, ud, yv = auto(me)

    other(me)

    sett.a += sett.yaw
    sett.x += d * math.cos(math.radians(sett.a))
    sett.y += d * math.sin(math.radians(sett.a))

    return [lr, fb, ud, yv, sett.x, sett.y]
