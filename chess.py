import tkinter as tk
import sys

from utils.board import Board


class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('Chess V2')
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()

        if sys.platform == "linux":
            self.window_arg = "-zoomed"
        else:
            self.window_arg = "-fullscreen"

        self.fullscreenState = False
        self.attributes(self.window_arg, self.fullscreenState)

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        self.board = Board(self)
        self.mainloop()

    def toggle_fullscreen(self, event):
        self.fullscreenState = not self.fullscreenState
        self.attributes(self.window_arg, self.fullscreenState)

    def exit_fullscreen(self, event):
        self.attributes(self.window_arg, False)

    def on_resize(self, event):
        print(f"on resize: {event.width}, {event.height}")


if __name__ == "__main__":
    App()
