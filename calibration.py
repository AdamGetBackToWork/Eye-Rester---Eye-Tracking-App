from __future__ import division
import cv2
from .pupil import Pupil


class Calibration(object):
    """
    Handles the calibration process by determining the optimal binarization threshold
    for pupil detection based on the user's eye and webcam conditions.
    """

    def __init__(self):
        self.nb_frames = 20  # Number of frames used for calibration
        self.thresholds_left = []  # List to store left eye threshold values
        self.thresholds_right = []  # List to store right eye threshold values

    def is_complete(self):
        """Checks if the calibration process has collected enough frames."""
        return (
            len(self.thresholds_left) >= self.nb_frames
            and len(self.thresholds_right) >= self.nb_frames
        )

    def threshold(self, side):
        """Returns the computed threshold value for the specified eye."""
        if side == 0:
            return int(sum(self.thresholds_left) / len(self.thresholds_left))
        elif side == 1:
            return int(sum(self.thresholds_right) / len(self.thresholds_right))

    @staticmethod
    def iris_size(frame):
        """Calculates the proportion of the eye occupied by the iris."""
        frame = frame[5:-5, 5:-5]  # Crop edges to remove noise
        height, width = frame.shape[:2]
        nb_pixels = height * width  # Total number of pixels
        nb_blacks = nb_pixels - cv2.countNonZero(
            frame
        )  # Count black pixels (iris region)
        return nb_blacks / nb_pixels  # Return iris size ratio

    @staticmethod
    def find_best_threshold(eye_frame):
        """Finds the optimal binarization threshold for detecting the pupil."""
        average_iris_size = 0.48  # Expected iris size ratio
        trials = {}

        for threshold in range(5, 100, 5):  # Iterate through potential threshold values
            iris_frame = Pupil.image_processing(eye_frame, threshold)
            trials[threshold] = Calibration.iris_size(iris_frame)

        # Select the threshold that produces the closest iris size to the expected value
        best_threshold, _ = min(
            trials.items(), key=lambda p: abs(p[1] - average_iris_size)
        )
        return best_threshold

    def evaluate(self, eye_frame, side):
        """Adds a newly computed threshold value to the calibration data for the given eye."""
        threshold = self.find_best_threshold(eye_frame)

        if side == 0:
            self.thresholds_left.append(threshold)
        elif side == 1:
            self.thresholds_right.append(threshold)
