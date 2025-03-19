import math
import numpy as np
import cv2
from .pupil import Pupil


class Eye(object):
    """
    This class processes an eye region from a face image, isolates the eye,
    calculates a blinking ratio, and detects the pupil.
    """

    # Landmark indices for the left and right eye in the 68-point facial landmark model
    LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
    RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]

    def __init__(self, original_frame, landmarks, side, calibration):
        self.frame = None  # Extracted eye region
        self.origin = None  # Top-left corner of the cropped eye region
        self.center = None  # Center point of the eye region
        self.pupil = None  # Detected pupil object
        self.landmark_points = None  # Eye region landmark points

        self._analyze(original_frame, landmarks, side, calibration)

    @staticmethod
    def _middle_point(p1, p2):
        """Calculates the midpoint between two given points."""
        x = int((p1.x + p2.x) / 2)
        y = int((p1.y + p2.y) / 2)
        return (x, y)

    def _isolate(self, frame, landmarks, points):
        """
        Extracts the eye region from the face image and applies a mask
        to remove surrounding facial features.
        """
        # Get coordinates of the eye region based on landmark points
        region = np.array(
            [(landmarks.part(point).x, landmarks.part(point).y) for point in points]
        )
        region = region.astype(np.int32)
        self.landmark_points = region

        # Create a mask to extract only the eye region
        height, width = frame.shape[:2]
        black_frame = np.zeros((height, width), np.uint8)
        mask = np.full((height, width), 255, np.uint8)
        cv2.fillPoly(mask, [region], (0, 0, 0))
        eye = cv2.bitwise_not(black_frame, frame.copy(), mask=mask)

        # Crop the eye region with a small margin
        margin = 5
        min_x = np.min(region[:, 0]) - margin
        max_x = np.max(region[:, 0]) + margin
        min_y = np.min(region[:, 1]) - margin
        max_y = np.max(region[:, 1]) + margin

        self.frame = eye[min_y:max_y, min_x:max_x]
        self.origin = (min_x, min_y)

        # Calculate the center of the eye region
        height, width = self.frame.shape[:2]
        self.center = (width / 2, height / 2)

    def _blinking_ratio(self, landmarks, points):
        """
        Computes the eye aspect ratio to estimate if the eye is open or closed.
        This is calculated as the ratio of the eye width to the eye height.
        """
        left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
        right = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
        top = self._middle_point(landmarks.part(points[1]), landmarks.part(points[2]))
        bottom = self._middle_point(
            landmarks.part(points[5]), landmarks.part(points[4])
        )

        # Compute distances
        eye_width = math.hypot((left[0] - right[0]), (left[1] - right[1]))
        eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))

        try:
            ratio = eye_width / eye_height
        except ZeroDivisionError:
            ratio = None  # Avoid division by zero errors

        return ratio

    def _analyze(self, original_frame, landmarks, side, calibration):
        """
        Detects and isolates the eye, calculates the blinking ratio,
        and initializes the pupil detection.
        """
        # Determine which eye to process
        if side == 0:
            points = self.LEFT_EYE_POINTS
        elif side == 1:
            points = self.RIGHT_EYE_POINTS
        else:
            return

        # Compute the blinking ratio
        self.blinking = self._blinking_ratio(landmarks, points)

        # Isolate the eye region
        self._isolate(original_frame, landmarks, points)

        # If calibration is incomplete, update it using the eye frame
        if not calibration.is_complete():
            calibration.evaluate(self.frame, side)

        # Get threshold for pupil detection and create a Pupil object
        threshold = calibration.threshold(side)
        self.pupil = Pupil(self.frame, threshold)
