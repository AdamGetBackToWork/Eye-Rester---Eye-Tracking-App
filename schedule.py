from .eye_rester_app import EyeResterApp
from .example import Example

# or
# import eye_rester_app_scalable
import tkinter as tk
import time

# sleep time is the time program awaits to initialize (in seconds, that's why * 60)
sleep_time = 10


# function for calling the app
def run_eye_rester():
    root = tk.Tk()
    app = EyeResterApp(root)

    # Make the window appear on top
    root.attributes("-topmost", True)
    root.update()
    root.attributes("-topmost", False)

    root.mainloop()


# condition for the app to run infinitely
if __name__ == "__main__":
    while True:
        run_eye_rester()
        time.sleep(sleep_time)
        print("end of break")
        # print(away)
        # Example.example()
        # time.sleep(sleep_time)
