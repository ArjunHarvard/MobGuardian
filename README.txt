Author: Arjun Singh
Created: 08/03/2021

Video Link: https://drive.google.com/file/d/1MdHGD4K9J_V2d5MijeXqfSACDlc1TTid/view?usp=sharing

+-------------+
| Description |
+-------------+
Autonomous drone for object detection and pose detection in action figures.
If a gun is detected, the system identifies the location of the figure in an image.
If a gun is detected and the hands are above the head, the figure is highlighted Red. 

+--------------+
| Installation |
+--------------+
1. Install Python 3.8+
2. pip install opencv-python
3. pip install tensorflow
   * "pip install tenserflow-gpu" if applicable
4. pip install imageai
5. pip install djitellopy

Depending on the machine, there may be other dependencies.
The install for tensorflow is especially complicated. 
Check ImageAI, TensorFlow, and OpenCV when troubleshooting.


+---------------+
| Configuration |
+---------------+
All configurable values reside in settings.py
Settings of note:

* yolo_h5 - path to yolo h5 file for image detection
* yolo_json - path to yolo JSON file for image detection
* PATH - path to photo directory for snapshots

There is a yolo folder in mob_guard that has example and JSON. Set the path to this in configuration.
Cannot include h5 because it exceeds GitHub's file size limit


+-----------+
| Controlls |
+-----------+
There are 3 "modes": Manual, Autopilot, and Autoland

The system starts in the Manual Control Mode. There are several controls available:

FLIGHT
* "w": increase elevation
* "s": decrease elevation
* "a": rotate counter-clockwise
* "d": rotate clockwise
* "e": take-off
* "q": land
* "UP": fly forward
* "DOWN": fly backward
* "LEFT": strafe left
* "RIGHT": strafe right

DATA ANALYSIS
* "c": change image filter (normal, red isolation, blue isolation, stacked)
* "p": print elevation, state, and battery
* "z": snap a picture and save the frame

MODE
* "t": initiate auto-landing
* "n": initiate auto-pilot

Auto-Landing siezes control and runs the landing pipeline. Pressing "m" returns control back to the user.

Auto-Pilot runs the drone in a predetermined route until the time expires, battery hits 20%, or "m" is pressed.
If time expires or the battery is exceeded, the Auto-Pilot initiates Auto-Land

