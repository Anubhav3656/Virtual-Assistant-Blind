"""
navigation_assistant.py
------------------------
Continuous real-time obstacle detection and voice guidance for navigation.
"""

import cv2
from ultralytics import YOLO
import numpy as np
import time

# Load YOLO model once
model = YOLO("yolov8n.pt")


def continuous_navigation(talk, listen_for_stop, update_interval=2):
    """
    Continuously guides the user by detecting obstacles in real-time.
    
    Args:
        talk: function from main.py for text-to-speech
        listen_for_stop: function that listens for stop commands (like "stop navigation")
        update_interval: seconds between spoken updates
    """

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        talk("Camera not detected.")
        return

    talk("Navigation mode activated. I will guide you. Say 'stop navigation' to exit.")

    last_direction = None
    last_update_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        results = model(frame, stream=True)
        frame_h, frame_w = frame.shape[:2]
        directions = {"left": 0, "center": 0, "right": 0}

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                name = model.names[cls]
                conf = float(box.conf[0])
                if conf < 0.5:
                    continue

                # Ignore small objects
                x1, y1, x2, y2 = box.xyxy[0]
                area = (x2 - x1) * (y2 - y1)
                if area < (frame_h * frame_w * 0.02):
                    continue

                # Determine horizontal direction
                cx = (x1 + x2) / 2
                if cx < frame_w / 3:
                    directions["left"] += 1
                elif cx > frame_w * 2 / 3:
                    directions["right"] += 1
                else:
                    directions["center"] += 1

        # Find most blocked direction
        left, center, right = directions["left"], directions["center"], directions["right"]
        new_direction = None

        if all(v == 0 for v in directions.values()):
            new_direction = "clear"
        elif center > max(left, right):
            new_direction = "front_blocked"
        elif left > right:
            new_direction = "left_blocked"
        elif right > left:
            new_direction = "right_blocked"
        else:
            new_direction = "uncertain"

        # Speak only if direction changed or enough time passed
        now = time.time()
        if new_direction != last_direction and (now - last_update_time > update_interval):
            if new_direction == "clear":
                talk("Path is clear ahead.")
            elif new_direction == "front_blocked":
                talk("Obstacle ahead. Move slightly left or right.")
            elif new_direction == "left_blocked":
                talk("Obstacle on the left. Move to your right.")
            elif new_direction == "right_blocked":
                talk("Obstacle on the right. Move to your left.")
            elif new_direction == "uncertain":
                talk("Obstacles detected around. Move slowly.")
            
            last_update_time = now
            last_direction = new_direction

        # Check if user says stop
        if listen_for_stop():
            talk("Stopping navigation mode.")
            break

    cap.release()
    cv2.destroyAllWindows()
