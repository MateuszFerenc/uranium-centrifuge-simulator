import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog


class Cons:
    sim_background_color = "#AAAAAA"
    button_background_color = "#999999"
    checkbox_background_color = "#BBBBBB"
    list_background_color = "#999999"
    window_x = 800
    window_y = 500


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

    def create_root(self):
        pass


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()
