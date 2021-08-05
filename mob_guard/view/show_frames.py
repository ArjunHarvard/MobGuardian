# ##############################
# # Title: Show Frames
# # Desc: Visualize different Image pipelines
# # Author: Arjun Singh
# ##############################

import numpy as np
import cv2
import time

from mob_guard.settings import YDIM, XDIM


def display(q, r, s):
    """Subprocess to manage Detection frames and Filtered frames"""
    # Initialize empty images
    img_1 = np.zeros((YDIM, XDIM))
    img_2 = np.zeros((YDIM, XDIM))

    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out = cv2.VideoWriter(f'data/detector{time.time()}.avi', fourcc, 30.0, (XDIM, YDIM))

    while True:
        # Burn leftover frames
        if not q.empty():
            q.get()

        # Display Detector Boxes
        if not r.empty():
            img_1 = r.get()
        #     if len(img_1.shape) < 3:
        #         img_1 = np.dstack((img_1, img_1, img_1))
        # out.write(img_1)
        cv2.imshow("Detector", img_1)

        # Display Filtered Input
        if not s.empty():
            img_2 = s.get()
        #     if len(img_2.shape) < 3:
        #         img_2 = np.dstack((img_2, img_2, img_2))
        # out.write(img_2)
        cv2.imshow("Tracker", img_2)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    out.release()
    cv2.destroyAllWindows()
