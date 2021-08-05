# ##############################
# # Title: Settings
# # Desc: Configure values to tune/manipulate the system
# # Author: Arjun Singh
# ##############################

from functools import partial
import numpy as np
import cv2

from mob_guard.model.filters import filter_color, stacked_filter


# Display Dimensions
XDIM = 360
YDIM = 240

# Movement Speed
fSpeed = 117 / 10  # Forward Speed in cm/s   (15cm/s)
aSpeed = 360 / 10  # Angular Speed Degrees/s  (50d/s)
interval = 0.05
dInterval = fSpeed * interval
aInterval = aSpeed * interval

# Snap Photos
IMAGE_DELAY = 0.3
PATH = "images/drone_images"

# Landing
LANDING_TIMEFRAME = 180

# Cascade
spartan_cascade = cv2.CascadeClassifier(
    'path_to_haar_cascade_if_needed'
)

# Filters
FILTER_LIST = ["normal", "red", "blue", "red-blue-stack"]
FILTERS = {
    "normal": lambda i: i,
    "red": partial(filter_color, low=np.asarray([20, 0, 20]), high=np.asarray([60, 10, 250])),
    "blue": partial(filter_color, low=np.asarray([150, 130, 130]), high=np.asarray([190, 180, 170])),
    "red-blue-stack": stacked_filter,
}

# System States
STATE_LIST = [
    "manual",
    "lz_descend", "lz_find", "lz_center", "lz_approach",
    "auto_init", "auto_takeoff", "auto_lower", "auto_position", "auto_rotate", "auto_pilot"
]

# Trained YOLOv3
yolo_h5 = r"path_to_yolo_h5"
yolo_json = r"path_to_yolo_json"
