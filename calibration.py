from __future__ import division
import cv2
from .pupil import Pupil


class Calibration:
    """Calibrates the pupil detection by determining the best threshold."""

    def __init__(self):
        self.nb_frames = 20
        self.thresholds_left = []
        self.thresholds_right = []

    def is_complete(self):
        """Checks if calibration is done."""
        return (
            len(self.thresholds_left) >= self.nb_frames
            and len(self.thresholds_right) >= self.nb_frames
        )

    def threshold(self, side):
        """Returns threshold for left (0) or right (1) eye."""
        thresholds = self.thresholds_left if side == 0 else self.thresholds_right
        return int(sum(thresholds) / len(thresholds)) if thresholds else 0

    @staticmethod
    def iris_size(frame):
        """Calculates iris coverage in the eye frame."""
        frame = frame[5:-5, 5:-5]
        nb_pixels = frame.size
        nb_blacks = nb_pixels - cv2.countNonZero(frame)
        return nb_blacks / nb_pixels

    @staticmethod
    def find_best_threshold(eye_frame):
        """Finds optimal threshold for binarization."""
        target_size = 0.48
        trials = {
            t: Calibration.iris_size(Pupil.image_processing(eye_frame, t))
            for t in range(5, 100, 5)
        }
        return min(trials, key=lambda t: abs(trials[t] - target_size))

    def evaluate(self, eye_frame, side):
        """Updates calibration with a new eye frame."""
        threshold = self.find_best_threshold(eye_frame)
        (self.thresholds_left if side == 0 else self.thresholds_right).append(threshold)
