# ##############################
# # Title: Landing Control
# # Desc: State machine for automated landing
# # Author: Arjun Singh
# ##############################

import time

from mob_guard import globals as sett
from mob_guard.model import descend_to_lz, search_for_lz, adjust_for_lz, approach_lz
from mob_guard.controller.pygame_interface import get_key


def land(me):
    """Determine flight instructions based on global state"""
    lr, fb, ud, yv = 0, 0, 0, 0

    if time.time() > sett.auto_deadline:
        sett.current_state = "manual"
        print("RAN OUT OF TIME")
        return lr, fb, ud, yv
    elif get_key("m"):
        sett.current_state = "manual"
        sett.auto_deadline = time.time()
        return lr, fb, ud, yv
    elif 'lz_' in sett.current_state:
        if sett.current_state == "lz_descend":
            (lr, fb, ud, yv), result = descend_to_lz(me)
            if result:
                sett.current_state = "lz_find"
        elif sett.current_state == "lz_find":
            sett.current_filter = "red-blue-stack"
            (lr, fb, ud, yv), result = search_for_lz(me)
            if result:
                sett.current_state = "lz_center"
        elif sett.current_state == "lz_center":
            sett.current_filter = "red-blue-stack"
            (lr, fb, ud, yv), result = adjust_for_lz(me)
            if result:
                sett.current_state = "lz_approach"
        elif sett.current_state == "lz_approach":
            sett.current_filter = "red-blue-stack"
            (lr, fb, ud, yv), result = approach_lz(me)
            if result:
                sett.current_state = "manual"
                sett.auto_deadline = time.time()
        return lr, fb, ud, yv
