# ##############################
# # Title: Autopilot Controls
# # Desc: State Machine for Auto Pilot
# # Author: Arjun Singh
# ##############################

import time

from mob_guard.settings import LANDING_TIMEFRAME
from mob_guard import globals as sett
from mob_guard.model import init_autopilot, auto_takeoff, auto_lower, auto_position, auto_rotate, auto_pilot
from mob_guard.controller.pygame_interface import get_key


def auto(me):
    """Execute code based on global state"""
    lr, fb, ud, yv = 0, 0, 0, 0

    if get_key("m"):
        sett.current_state = "manual"
        sett.auto_deadline = time.time()
        return lr, fb, ud, yv
    elif 'auto_' in sett.current_state:
        if sett.current_state == "auto_init":
            sett.current_filter = "normal"
            (lr, fb, ud, yv), result = init_autopilot(me)
            if result:
                sett.current_state = "auto_takeoff"
        elif sett.current_state == "auto_takeoff":
            (lr, fb, ud, yv), result = auto_takeoff(me)
            if result:
                sett.current_state = "auto_lower"
        elif sett.current_state == "auto_lower":
            (lr, fb, ud, yv), result = auto_lower(me)
            if result:
                sett.current_state = "auto_position"
        elif sett.current_state == "auto_position":
            (lr, fb, ud, yv), result = auto_position(me)
            if result:
                sett.current_state = "auto_rotate"
        elif sett.current_state == "auto_rotate":
            (lr, fb, ud, yv), result = auto_rotate(me)
            if result:
                sett.current_state = "auto_pilot"
        elif sett.current_state == "auto_pilot":
            (lr, fb, ud, yv), result = auto_pilot(me)
            if result:
                sett.current_state = "lz_descend"
                sett.auto_deadline = time.time() + LANDING_TIMEFRAME
        return lr, fb, ud, yv
