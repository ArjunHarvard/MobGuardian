# ##############################
# # Title: Flight Pattern
# # Desc: Logic for AutoPilot
# # Author: Arjun Singh
# ##############################

from mob_guard.model.stop_watch import StopWatch


# Constants
fSpeed = 117 / 10  # Forward Speed in cm/s   (15cm/s)
aSpeed = 360 / 10  # Angular Speed Degrees/s  (50d/s)

# Parameters
clock = None
takeoff_thresh = 10
lower_thresh = 5
radius = 0.5
rotate = 3
flight_time = 20


def init_autopilot(me):
    """Set stopwatch"""
    global clock
    clock = StopWatch()
    clock.reset(takeoff_thresh)
    return (0, 0, 0, 0), True


def auto_takeoff(me):
    """Takeoff and wait several seconds for camera to catch up"""
    global clock

    # Takeoff
    if me.get_height() == 0:
        me.takeoff()

    # Evaluate time from takeoff
    if clock.past():
        clock.reset(lower_thresh)
        return (0, 0, 0, 0), True
    return (0, 0, 0, 0), False


def auto_lower(me):
    """Minimize elevation of drone"""
    global clock

    # Lower if time is still going
    if clock.past():
        clock.reset(radius)
        return (0, 0, 0, 0), True
    return (0, 0, -30, 0), False


def auto_position(me):
    """Move drone away from landing zone"""
    if clock.past():
        clock.reset(rotate)
        return (0, 0, 0, 0), True
    return (0, 50, 0, 0), False


def auto_rotate(me):
    """Reorient Yaw of drone"""
    if clock.past():
        clock.reset(flight_time)
        return (0, 0, 0, 0), True
    return (0, 0, 0, 30), False


def auto_pilot(me):
    """Move in a circle until battery runs low"""
    if clock.past() or me.get_battery() < 20:
        return (0, 0, 0, 0), True
    return (0, 20, -10, 25), False
