# ##############################
# # Title: Other Controls
# # Desc: Arbitrary controls always available
# # Author: Arjun Singh
# ##############################

import cv2
import time

from mob_guard.settings import PATH, FILTER_LIST, IMAGE_DELAY
from mob_guard import globals as sett
from mob_guard.controller.pygame_interface import get_key


def other(me):
    """Misc: Take Picture, change filter, or get metadata"""
    if get_key("z"):
        cv2.imwrite(f"{PATH}/{time.time()}.jpg", sett.img)
        time.sleep(IMAGE_DELAY)

    if get_key("c"):
        sett.current_filter = FILTER_LIST[(FILTER_LIST.index(sett.current_filter) + 1) % len(FILTER_LIST)]
        time.sleep(0.1)

    if get_key("p"):
        print(f"Height: {me.get_height()} | State: {sett.current_state} | Battery: {me.get_battery()}")
