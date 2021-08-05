# ##############################
# # Title: Map (REGRESSED)
# # Desc: Visualize map to track drone position in space
# # Source: Murtaza's Workshop
# # Modified: Arjun Singh
# ##############################

import numpy as np
import cv2

from mob_guard import globals as sett


def draw_points(img, points):
    """Draw points on the map"""
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(
        img,
        f"({(points[-1][0] - 500) / 100}, {(points[-1][1] - 500) / 100})m",
        (points[-1][0] + 10, points[-1][1] + 30),
        cv2.FONT_HERSHEY_PLAIN,
        1,
        (255, 0, 255),
        1,
    )


def map_points(vals):
    """Initialize array and draw points corresponding to input values"""
    img_map = np.zeros((1000, 1000, 3), np.uint8)

    if sett.points[-1][0] != vals[4] or sett.points[-1][1] != vals[5]:
        sett.points.append((int(vals[4]), int(vals[5])))
    draw_points(img_map, sett.points)
    cv2.imshow("Output", img_map)
