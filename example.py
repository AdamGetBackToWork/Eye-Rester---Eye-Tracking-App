"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)


class Example:

    def example():
        while True:
            # We get a new frame from the webcam
            _, frame = webcam.read()

            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            away = "not away"
            frame = gaze.annotated_frame()
            text = ""

            if gaze.is_blinking():
                text = "Blinking"
            elif gaze.is_right():
                text = "Looking right"
            elif gaze.is_left():
                text = "Looking left"
            elif gaze.is_center():
                text = "Looking center"
            else:
                text = "Cant see your eyes"
                away = "away"

            print(away)

            # cv2.putText(
            #     frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2
            # )
            # cv2.putText(
            #     frame, away, (120, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (147, 58, 31), 2
            # )

            # left_pupil = gaze.pupil_left_coords()
            # right_pupil = gaze.pupil_right_coords()
            # cv2.putText(
            #     frame,
            #     "Left pupil:  " + str(left_pupil),
            #     (90, 130),
            #     cv2.FONT_HERSHEY_DUPLEX,
            #     0.9,
            #     (147, 58, 31),
            #     1,
            # )
            # cv2.putText(
            #     frame,
            #     "Right pupil: " + str(right_pupil),
            #     (90, 165),
            #     cv2.FONT_HERSHEY_DUPLEX,
            #     0.9,
            #     (147, 58, 31),
            #     1,
            # )

            # cv2.imshow("Demo", frame)

            if cv2.waitKey(1) == 27:
                break

        webcam.release()
        cv2.destroyAllWindows()

    def is_away() -> int:
        # Get a single frame from the webcam
        _, frame = webcam.read()

        # Analyze this frame for gaze status
        gaze.refresh(frame)
        if gaze.is_blinking() or gaze.is_right() or gaze.is_left() or gaze.is_center():
            return 0  # Not away
        else:
            return 1  # Away
