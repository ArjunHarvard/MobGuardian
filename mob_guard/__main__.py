# ##############################
# # Title: Main
# # Desc: Manage Drone Pipeline
# # Author: Arjun Singh
# ##############################

from multiprocessing import Process, Queue
from djitellopy import tello
import time
import cv2

from settings import XDIM, YDIM, FILTERS
from mob_guard import globals as sett
from controller import get_keyboard_input, init
from model import image_detector
from view import display


if __name__ == "__main__":
    # Initialize Pygame
    init()

    # Connect to Drone
    me = tello.Tello()
    me.connect()
    print(f"Battery Level: [{me.get_battery()}]%")
    me.streamon()

    # Capture input stream from drones
    drone_frames = Queue()

    # Returned frames from detector
    detect_frames = Queue()

    # Returned frames from controller
    control_frames = Queue()

    # Image Detection Pipeline
    p = Process(target=image_detector, args=(drone_frames, detect_frames))
    p.start()

    # Display Pipeline
    d = Process(target=display, args=(drone_frames, detect_frames, control_frames))
    d.start()

    while True:
        # read image stream and write to drone_frames Queue
        img = me.get_frame_read().frame
        sett.img = cv2.resize(img, (XDIM, YDIM))
        drone_frames.put(sett.img)

        # Process Keyboard Input
        vals = get_keyboard_input(me)
        me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        sett.img = FILTERS[sett.current_filter](sett.img)
        control_frames.put(sett.img)

        # Give display time to render frame
        time.sleep(0.01)
