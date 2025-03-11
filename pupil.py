import numpy as np
import cv2


class Pupil:
    """
    Detects the iris of an eye and estimates the position of the pupil.
    """

    def __init__(self, eye_frame, threshold):
        """
        Initializes the Pupil object and detects the iris.
        """
        self.iris_frame = None
        self.threshold = threshold
        self.x = None
        self.y = None

        self._detect_iris(eye_frame)

    @staticmethod
    def _image_processing(eye_frame, threshold):
        """
        Processes the eye frame to isolate the iris using filtering and thresholding.
        """
        kernel = np.ones((3, 3), np.uint8)
        processed_frame = cv2.bilateralFilter(eye_frame, 10, 15, 15)
        processed_frame = cv2.erode(processed_frame, kernel, iterations=3)
        processed_frame = cv2.threshold(
            processed_frame, threshold, 255, cv2.THRESH_BINARY
        )[1]

        return processed_frame

    def _detect_iris(self, eye_frame):
        """
        Detects the iris and estimates the pupil position by calculating the centroid.
        """
        self.iris_frame = self._image_processing(eye_frame, self.threshold)

        contours, _ = cv2.findContours(
            self.iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )[-2:]
        contours = sorted(contours, key=cv2.contourArea)

        try:
            moments = cv2.moments(contours[-2])
            self.x = int(moments["m10"] / moments["m00"])
            self.y = int(moments["m01"] / moments["m00"])
        except (IndexError, ZeroDivisionError):
            self.x = None
            self.y = None
