import tkinter as tk
from tkinter import *
import random
from os.path import dirname
from .example import Example


class EyeResterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EYE rester")

        self.countdown_seconds = 20

        self.load_images()
        self.create_widgets()
        self.center_window()

        self.update_timer()

    def color_generator(self):
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
        self.bg_color = random.choice(
            self.colors1 if random.randrange(0, 2) == 1 else self.colors2
        )
        self.txt_color = "#000000" if self.bg_color in self.colors1 else "#f8f6e8"

    def folder_path(self):
        return dirname(__file__)

    def load_images(self):
        image_path = str(self.folder_path()) + "/images/option_2--.png"
        image_path = image_path.replace("\\", "/")

        self.image = PhotoImage(file=image_path)

    def create_widgets(self):
        self.color_generator()
        self.configuration_setting()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.image_label = tk.Label(self.root, image=self.image)
        self.image_label.pack(
            side=tk.LEFT,
            anchor=tk.NW,
            pady=40,
            padx=(60, 15),
        )
        self.image_label.configure(bg=self.bg_color)

        self.welcome_label = Label(
            self.root,
            text="It's time to give your eyes a rest!\n\nLook ~20 feet away",
            font=(
                "CIN",
                14,
            ),
            anchor=CENTER,
            fg=self.txt_color,
            pady=30,
        )
        self.welcome_label.configure(bg=self.bg_color)
        self.welcome_label.pack()

        self.timer_label = Label(
            self.root, text=f"Time left: {self.countdown_seconds} seconds", anchor=S
        )
        self.timer_label.configure(bg=self.bg_color)
        self.timer_label.pack()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        app_width = 540
        app_height = 180

        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        self.root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        self.root.configure(bg=self.bg_color)

    def update_timer(self):
        # Check if user is looking away
        if Example.is_away() == 1:
            # Only countdown when user is looking away
            if self.countdown_seconds > 0:
                self.countdown_seconds -= 1
                self.timer_label.config(
                    text=f"Time left: {self.countdown_seconds} seconds",
                    font=("Optima", 10),
                    fg=self.txt_color,
                )
            else:
                self.timer_label.config(text="Time's up!")
            eye_position_message = "Away"
        else:
            # Display "Not looking away" and pause countdown
            self.timer_label.config(
                text="Not looking away!", font=("Optima", 10), fg=self.txt_color
            )
            eye_position_message = "Not Away"

        # Call update_timer again after 1 second
        self.root.after(1000, self.update_timer)
        print("The current eye position is: " + eye_position_message)


if __name__ == "__main__":
    root = tk.Tk()
    app = EyeResterApp(root)

    root.mainloop()
