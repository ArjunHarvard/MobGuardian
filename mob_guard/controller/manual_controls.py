# ##############################
# # Title: Manual Controls
# # Desc: Control drone from laptop
# # Source: Based on "Murtaza's Workshop"
# # Modified: Arjun Singh
# ##############################

import time

from mob_guard.settings import dInterval, aInterval, LANDING_TIMEFRAME
from mob_guard import globals as sett
from mob_guard.controller.pygame_interface import get_key


def manual(me):
    """Process keyboard inputs to start auto-pilot or fly drone"""
    speed = 50
    aspeed = 50

    d = 0
    lr, fb, ud, yv = 0, 0, 0, 0

    # Left and Right
    if get_key("LEFT"):
        lr = -speed
        d = dInterval
        sett.a = -180
    elif get_key("RIGHT"):
        lr = speed
        d = -dInterval
        sett.a = 180

    # Forward and Back
    if get_key("UP"):
        fb = speed
        d = dInterval
        sett.a = 270
    elif get_key("DOWN"):
        fb = -speed
        d = -dInterval
        sett.a = -90

    # Up and Down
    if get_key("w"):
        ud = speed
    elif get_key("s"):
        ud = -speed

    # Yaw / Turn
    if get_key("a"):
        yv = -aspeed
        sett.yaw -= aInterval
    elif get_key("d"):
        yv = aspeed
        sett.yaw += aInterval

    # Takeoff and Land
    if get_key("q"):
        me.land()
        time.sleep(3)
    if get_key("e"):
        me.takeoff()
        time.sleep(0.1)

    # Switch to landing
    if get_key("t"):
        print("Starting Detection")
        sett.current_state = "lz_descend"
        sett.auto_deadline = time.time() + LANDING_TIMEFRAME

    # Switch to Autopilot
    if get_key("n"):
        print("Starting Autopilot")
        sett.current_state = "auto_init"

    return lr, fb, ud, yv, d
