"""Module to run the chess game"""
import tkinter as tk
import sys

from utils.board import Board


class App(tk.Tk):
    """Controls the window and contains the board"""

    def __init__(self):
        super().__init__()
        self.title('Chess V2')

        if sys.platform == "linux":
            self.window_arg = "-zoomed"
        else:
            self.window_arg = "-fullscreen"

        self.fullscreen_state = False
        self.attributes(self.window_arg, self.fullscreen_state)

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        self.board = Board(self)
        self.mainloop()

    def toggle_fullscreen(self, _):
        """Gives user ability to toggle fullscreen"""

        self.fullscreen_state = not self.fullscreen_state
        self.attributes(self.window_arg, self.fullscreen_state)

    def exit_fullscreen(self, _):
        """Allows user to escape fullscreen with escape key"""

        self.attributes(self.window_arg, False)


if __name__ == "__main__":
    App()
