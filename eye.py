import math
import numpy as np
import cv2
from .pupil import Pupil


class Eye:
    """
    Represents an eye, isolates it from the face, and detects the pupil.
    """

    LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
    RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]

    def __init__(self, frame, landmarks, side, calibration):
        """
        Initializes the Eye object and processes the eye region.
        """
        self.frame = None
        self.origin = None
        self.center = None
        self.pupil = None
        self.landmark_points = None

        self._analyze(frame, landmarks, side, calibration)

    @staticmethod
    def _middle_point(p1, p2):
        """
        Computes the midpoint between two given points.
        """
        return (int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2))

    def _isolate(self, frame, landmarks, points):
        """
        Extracts the eye region from the frame.
        """
        region = np.array(
            [(landmarks.part(p).x, landmarks.part(p).y) for p in points], np.int32
        )
        self.landmark_points = region

        height, width = frame.shape[:2]
        mask = np.full((height, width), 255, np.uint8)
        cv2.fillPoly(mask, [region], 0)
        eye = cv2.bitwise_not(
            np.zeros((height, width), np.uint8), frame.copy(), mask=mask
        )

        # Crop the eye region with a margin
        margin = 5
        min_x, max_x = np.min(region[:, 0]) - margin, np.max(region[:, 0]) + margin
        min_y, max_y = np.min(region[:, 1]) - margin, np.max(region[:, 1]) + margin

        self.frame = eye[min_y:max_y, min_x:max_x]
        self.origin = (min_x, min_y)
        self.center = (self.frame.shape[1] / 2, self.frame.shape[0] / 2)

    def _blinking_ratio(self, landmarks, points):
        """
        Computes a ratio indicating whether the eye is open or closed.
        """
        left, right = landmarks.part(points[0]), landmarks.part(points[3])
        top, bottom = self._middle_point(
            landmarks.part(points[1]), landmarks.part(points[2])
        ), self._middle_point(landmarks.part(points[5]), landmarks.part(points[4]))

        eye_width = math.hypot(left.x - right.x, left.y - right.y)
        eye_height = math.hypot(top[0] - bottom[0], top[1] - bottom[1])

        return eye_width / eye_height if eye_height else None

    def _analyze(self, frame, landmarks, side, calibration):
        """
        Processes the eye region, detects blinking, and initializes the Pupil object.
        """
        points = (
            self.LEFT_EYE_POINTS
            if side == 0
            else self.RIGHT_EYE_POINTS if side == 1 else None
        )
        if not points:
            return

        self.blinking = self._blinking_ratio(landmarks, points)
        self._isolate(frame, landmarks, points)

        if not calibration.is_complete():
            calibration.evaluate(self.frame, side)

        self.pupil = Pupil(self.frame, calibration.threshold(side))
