# ##############################
# # Title: Landing
# # Desc: Logic to handle Auto-Landing
# # Author: Arjun Singh
# ##############################

from djitellopy import tello
import time
import cv2

from mob_guard.settings import YDIM, XDIM
from mob_guard import globals as sett
from mob_guard.model.filters import stacked_filter, bounding_box


def avg(n1, n2):
    """Average 2 values"""
    return (n1 + n2) / 2


def compute_bounds():
    """Hard-coded target window within frame"""
    x_inc = int(XDIM / 3)
    x_lo = x_inc
    x_hi = x_inc * 2
    y_inc = int(YDIM / 4)
    y_lo = y_inc * 2
    y_hi = y_inc * 3
    return y_lo, x_lo, y_hi, x_hi


def descend_to_lz(me: tello.Tello):
    """Minimize elevation to below 15 cm above ground"""
    elevation = me.get_height()
    print("Elevation:", elevation)
    if elevation > 15:
        print("descending")
        return (0, 0, -25, 0), False
    else:
        print("DESCENDED")
        return (0, 0, 0, 0), True


def search_for_lz(*args):
    """rotate until LZ is detected"""
    # Get the current frame and filter
    masked = stacked_filter(sett.img)

    # Try to isolate target
    try:
        y1, x1, y2, x2 = bounding_box(masked)
    except:
        y1, x1, y2, x2 = 0, 0, 0, 0

    # If target is found, return True and do nothing
    if 255 in masked[y1:y2, x1:x2]:
        print("Found LZ at:", (x1, y1), (x2, y2))
        return (0, 0, 0, 0), True
    else:
        print("lz not found")
        return (0, 0, -10, -50), False


def adjust_for_lz(me: tello.Tello):
    """Modify heading until the center of the LZ falls within target window"""
    sett.img = me.get_frame_read().frame
    sett.img = cv2.resize(sett.img, (XDIM, YDIM))

    try:
        # Build Mask
        masked = stacked_filter(sett.img)
        y1, x1, y2, x2 = bounding_box(masked)

        avg_x = avg(x1, x2)
        avg_y = avg(y1, y2)
        y_lo, x_lo, y_hi, x_hi = compute_bounds()

        if (x_lo <= avg_x <= x_hi) and (y_lo <= avg_y <= y_hi):
            print("CENTERED")
            return (0, 0, 0, 0), True
        else:
            yv = 0
            ud = 0

            if avg_x < x_lo:
                yv = -10
            elif avg_x > x_hi:
                yv = 10

            if avg_y < y_lo:
                ud = 10
            elif avg_y > y_hi:
                ud = -10

            print("lz not centered")
            return (0, 0, ud, yv), False
    except:
        return (0, 0, -20, 0), False


def approach_lz(me: tello.Tello):
    """Fly toward landing zone and land"""
    sett.img = me.get_frame_read().frame
    sett.img = cv2.resize(sett.img, (XDIM, YDIM))

    # Build Mask
    try:
        masked = stacked_filter(sett.img)
        y1, x1, y2, x2 = bounding_box(masked)

        avg_x = avg(x1, x2)
        avg_y = avg(y1, y2)
        y_lo, x_lo, y_hi, x_hi = compute_bounds()

        lr, fb, yv, ud = 0, 30, 0, 0

        if avg_x < x_lo:
            lr = -10
        elif avg_x > x_hi:
            lr = 10
        elif avg_y > y_hi:
            if me.get_height() <= 10:
                pass
            else:
                ud = -20
                fb = 0

        print("not ready to land")
        return (lr, fb, ud, yv), False

    except:
        sett.auto_deadline = time.time() + 2
        while time.time() < sett.auto_deadline:
            me.send_rc_control(0, 15, 0, 0)
        me.land()
        return (0, 0, 0, 0), True
