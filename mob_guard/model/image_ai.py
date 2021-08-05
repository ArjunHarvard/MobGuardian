# ##############################
# # Title: Image AI
# # Desc: Object Detection and Alert Pipeline
# # Author: Arjun Singh
# ##############################


import time

from imageai.Detection.Custom import CustomObjectDetection
import tensorflow as tf
import cv2

from mob_guard.settings import yolo_json, yolo_h5
from mob_guard.model.stop_watch import StopWatch


def image_detector(q, r):
    """Perform ImageAI YOLOv3 detection on ever frame"""
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(yolo_h5)
    detector.setJsonPath(yolo_json)
    detector.loadModel()

    watch = StopWatch()
    cool_off = 3

    with tf.device('/GPU:0'):
        while True:
            img = q.get()
            img_2, dic, pos = detector.detectObjectsFromImage(
                input_image=img,
                input_type="array",
                extract_detected_objects=True,
                output_type="array",
                minimum_percentage_probability=30
            )
            r.put(img_2)
            if watch.past() and analyze_frame(img, dic):
                watch.reset(cool_off)


def overlap(R1, R2):
    """Determine if 2 rectangles overlap"""
    if (R1[0] >= R2[2]) or (R1[2] <= R2[0]) or (R1[3] <= R2[1]) or (R1[1] >= R2[3]):
        return False
    else:
        return True


def analyze_frame(img, dic):
    """Hard-coded grouping and determination of danger level"""
    states = {"none": 0, "Warning": 1, "DANGER": 2}
    state = "none"

    if len(dic) <= 1:
        return

    first = dic.pop()
    groupings = {tuple(first["box_points"]): {first["name"]: first}}

    for detected in dic:
        found_overlap = False
        new_group = tuple(detected["box_points"])
        for group in groupings.keys():
            if overlap(group, new_group):
                groupings[group][detected["name"]] = detected
                found_overlap = True
                break
        if not found_overlap:
            groupings[new_group] = {detected["name"]: detected}

    for grouping in groupings.keys():
        group = groupings[grouping]

        spartan = 0
        up = 0
        down = 0
        pistol = 0

        if "spartan" in group:
            spartan = group["spartan"]["percentage_probability"]
        if "up" in group:
            up = group["up"]["percentage_probability"]
        if "down" in group:
            down = group["down"]["percentage_probability"]
        if "pistol" in group:
            pistol = group["pistol"]["percentage_probability"]

        if up > down > 0 and not spartan and not pistol:
            level = "Warning"
            img = cv2.rectangle(img, (grouping[0], grouping[1]), (grouping[2], grouping[3]), (0, 255, 255), 2)
            state = level if states[level] > states[state] else state
        elif up > down and (pistol or spartan):
            level = "DANGER"
            img = cv2.rectangle(img, (grouping[0], grouping[1]), (grouping[2], grouping[3]), (0, 0, 255), 2)
            state = level if states[level] > states[state] else state
        elif pistol and (spartan or down):
            level = "Warning"
            img = cv2.rectangle(img, (grouping[0], grouping[1]), (grouping[2], grouping[3]), (0, 255, 255), 2)
            state = level if states[level] > states[state] else state
        time.sleep(0.1)

    if states[state]:
        cv2.imshow(f"{level}", img)
        cv2.waitKey(1)
        return True
    return False
