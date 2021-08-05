# ##############################
# # Title: Filters
# # Desc: Perform thresholding on image
# # Author: Arjun Singh
# ##############################

import numpy as np
import cv2


# TODO: remove circular dependency
YDIM = 240
XDIM = 360


def filter_color(image, low, high):
    """isolate RGB range"""
    mask = cv2.inRange(image, low, high)
    return mask


def bounding_box(mask):
    """Find rectangle to bound positive pixels in binary image"""
    result = np.where(mask == 255)
    y1, x1 = np.amin(result, axis=1)
    y2, x2 = np.amax(result, axis=1)
    return y1, x1, y2, x2


def stacked_filter(image):
    """Ensemble 2 thresholds and find bounds
        isolate blue object inside red object (hard coded for landing)
    """
    try:
        mask_1 = filter_color(image, low=np.asarray([20, 0, 20]), high=np.asarray([60, 10, 250]))
        mask_2 = filter_color(image, low=np.asarray([150, 130, 130]), high=np.asarray([190, 180, 170]))
        y1, x1, y2, x2 = bounding_box(mask_1)
        mask = np.zeros((YDIM, XDIM), dtype="uint8")
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
        masked = cv2.bitwise_and(mask_2, mask_2, mask=mask)
    except:
        masked = np.zeros((YDIM, XDIM))
    return masked
