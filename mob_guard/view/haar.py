# ##############################
# # Title: Haar Cascade Detector (REGRESSED)
# # Desc: Perform Haar Detection on current frame
# # Source: "SentDex" from pythonprogramming.net
# # Modified: Arjun Singh
# ##############################

import cv2

from mob_guard.settings import spartan_cascade
from mob_guard import globals as sett


def haar_overlay():
    """detect and overlay on image"""
    gray = cv2.cvtColor(sett.img, cv2.COLOR_BGR2GRAY)
    spartans = spartan_cascade.detectMultiScale(gray, 20, 20)
    for (x, y, w, h) in spartans:
        cv2.rectangle(sett.img, (x, y), (x + w, y + h), (255, 255, 0), 2)
    return sett.img
