import tkinter as tk
from tkinter import *
import random
from os.path import dirname
from .example import Example


class EyeResterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EYE rester")

        self.countdown_seconds = 20  # Countdown timer initialized to 20 seconds

        self.load_images()
        self.create_widgets()
        self.center_window()

        self.update_timer()

    def color_generator(self):
        """Generates two lists of colors for background selection."""
        self.colors1 = [
            "#856ff8",
            "#46ACC0",
            "#9CD4FE",
            "#78bdf5",
            "#348a4d",
            "#CE6190",
            "#E6B6BB",
            "#CEBC61",
            "#ffc02e",
        ]
        self.colors2 = [
            "#217947",
            "#496757",
            "#991a20",
            "#8D4545",
            "#404ca1",
            "#6e056f",
        ]

    def configuration_setting(self):
        """Randomly selects a background color and sets text color accordingly."""
        self.bg_color = random.choice(
            self.colors1 if random.randrange(0, 2) == 1 else self.colors2
        )
        self.txt_color = "#000000" if self.bg_color in self.colors1 else "#f8f6e8"

    def folder_path(self):
        """Returns the directory of the current script file."""
        return dirname(__file__)

    def load_images(self):
        """Loads an image from the 'images' directory."""
        image_path = str(self.folder_path()) + "/images/option_2--.png"
        image_path = image_path.replace(
            "\\", "/"
        )  # Ensures compatibility with different OS
        self.image = PhotoImage(file=image_path)

    def create_widgets(self):
        """Creates UI elements such as labels and images."""
        self.color_generator()
        self.configuration_setting()

        # Set up an image label
        self.image_label = tk.Label(self.root, image=self.image)
        self.image_label.pack(side=tk.LEFT, anchor=tk.NW, pady=40, padx=(60, 15))
        self.image_label.configure(bg=self.bg_color)

        # Instruction label
        self.welcome_label = Label(
            self.root,
            text="It's time to give your eyes a rest!\n\nLook ~20 feet away",
            font=("CIN", 14),
            anchor=CENTER,
            fg=self.txt_color,
            pady=30,
        )
        self.welcome_label.configure(bg=self.bg_color)
        self.welcome_label.pack()

        # Timer label
        self.timer_label = Label(
            self.root, text=f"Time left: {self.countdown_seconds} seconds", anchor=S
        )
        self.timer_label.configure(bg=self.bg_color)
        self.timer_label.pack()

    def center_window(self):
        """Centers the application window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        app_width = 540
        app_height = 180

        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        self.root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        self.root.configure(bg=self.bg_color)

    def update_timer(self):
        """Updates the timer every second, checking if the user is looking away."""
        if Example.is_away() == 1:
            # Decrement timer only if user is looking away
            if self.countdown_seconds > 0:
                self.countdown_seconds -= 1
                self.timer_label.config(
                    text=f"Time left: {self.countdown_seconds} seconds",
                    font=("Optima", 10),
                    fg=self.txt_color,
                )
            else:
                self.timer_label.config(text="Time's up!")
        else:
            # Pause countdown and notify user to look away
            self.timer_label.config(
                text="Not looking away!", font=("Optima", 10), fg=self.txt_color
            )

        # Schedule update_timer to run again after 1 second
        self.root.after(1000, self.update_timer)
        print(Example.is_away())  # Debugging output


if __name__ == "__main__":
    root = tk.Tk()
    app = EyeResterApp(root)
    root.mainloop()
