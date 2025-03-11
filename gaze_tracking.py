import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration


class GazeTracking:
    """
    Tracks the user's gaze, determining eye position and whether the eyes are open or closed.
    """

    def __init__(self):
        """
        Initializes the gaze tracking system.
        """
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()

        # Load face detection and facial landmarks model
        self._face_detector = dlib.get_frontal_face_detector()
        model_path = os.path.join(
            os.path.dirname(__file__),
            "trained_models/shape_predictor_68_face_landmarks.dat",
        )
        self._predictor = dlib.shape_predictor(model_path)

    def _detect_faces(self, frame):
        """
        Detects faces in the given frame.
        """
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self._face_detector(gray_frame)

    def _analyze(self):
        """
        Detects the face, extracts eye regions, and initializes Eye objects.
        """
        faces = self._detect_faces(self.frame)
        if faces:
            landmarks = self._predictor(self.frame, faces[0])
            self.eye_left = Eye(self.frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(self.frame, landmarks, 1, self.calibration)
        else:
            self.eye_left = self.eye_right = None

    def refresh(self, frame):
        """
        Updates the frame and processes eye tracking.
        """
        self.frame = frame
        self._analyze()

    @property
    def pupils_located(self):
        """
        Checks if pupil coordinates are available.
        """
        return all(
            getattr(self.eye_left, "pupil", None)
            and getattr(self.eye_right, "pupil", None)
        )

    def pupil_coords(self, eye):
        """
        Returns pupil coordinates for the given eye.
        """
        if self.pupils_located:
            return (eye.origin[0] + eye.pupil.x, eye.origin[1] + eye.pupil.y)
        return None

    def horizontal_ratio(self):
        """
        Computes the horizontal gaze direction ratio.
        """
        if self.pupils_located:
            return (
                sum(
                    eye.pupil.x / (eye.center[0] * 2 - 10)
                    for eye in (self.eye_left, self.eye_right)
                )
                / 2
            )

    def vertical_ratio(self):
        """
        Computes the vertical gaze direction ratio.
        """
        if self.pupils_located:
            return (
                sum(
                    eye.pupil.y / (eye.center[1] * 2 - 10)
                    for eye in (self.eye_left, self.eye_right)
                )
                / 2
            )

    def is_right(self):
        """
        Determines if the user is looking to the right.
        """
        return self.horizontal_ratio() <= 0.35 if self.pupils_located else False

    def is_left(self):
        """
        Determines if the user is looking to the left.
        """
        return self.horizontal_ratio() >= 0.65 if self.pupils_located else False

    def is_center(self):
        """
        Determines if the user is looking at the center.
        """
        return not (self.is_right() or self.is_left())

    def is_blinking(self):
        """
        Determines if the user is blinking.
        """
        if self.pupils_located:
            return (self.eye_left.blinking + self.eye_right.blinking) / 2 > 3.8
        return False

    def annotated_frame(self):
        """
        Returns the frame with pupils highlighted.
        """
        frame = self.frame.copy()
        if self.pupils_located:
            color = (0, 255, 0)
            for eye in (self.eye_left, self.eye_right):
                x, y = self.pupil_coords(eye)
                cv2.drawMarker(
                    frame, (x, y), color, markerType=cv2.MARKER_CROSS, thickness=2
                )
        return frame
