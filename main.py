import tkinter as tk
from tkinter import ttk

sim_background_color = "#AAAAAA"
sim_title = "Uranium Centrifuge Simulator"
sim_windows_dimensions = "800x500"


class MainContainer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(sim_title)
        self.geometry(sim_windows_dimensions)
        self.resizable(False, False)
        self.attributes('-toolwindow', True)
        self.configure(bg=sim_background_color)

        mywindow = tk.Frame(self)
        mywindow.pack(side="top", fill="both", expand=True)
        mywindow.grid_rowconfigure(0, weight=1)
        mywindow.grid_columnconfigure(0, weight=1)
        mywindow.grid_columnconfigure(1, weight=1)

        self.openwindows = {}
        for Window in sim_windows:
            window_name = Window.__name__
            frame = Window(parent=mywindow, controller=self)
            self.openwindows[window_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartWindow")

    def show_frame(self, window_name):
        frame = self.openwindows[window_name]
        frame.tkraise()


class StartWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        # create the input frame
        input_frame = MainButtonsFrame(self)
        input_frame.grid(column=0, row=0)

        # create the button frame
        button_frame = MainInfosFrame(self)
        button_frame.grid(column=1, row=0)


class MainInfosFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text='Simulator infos:').grid(column=0, row=0)
        ttk.Label(self, text='Design and programming: Mateusz Ferenc').grid(column=1, row=1)
        ttk.Label(self, text='Version: 0.00.000.2256_22').grid(column=1, row=2)
        ttk.Label(self, text='Release date: 22/08/2022').grid(column=1, row=3)


class MainButtonsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.create_ui()

    def create_ui(self):
        ttk.Button(self, text="Launch Simulator").grid(column=0, row=0)
        ttk.Button(self, text="Wiew documentation").grid(column=0, row=1)


class InputsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        pass


class ControllersWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        pass


class OutputWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        pass


class ChartsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        pass


sim_windows = (StartWindow, InputsWindow, ControllersWindow, OutputWindow, ChartsWindow)

if __name__ == "__main__":
    main = MainContainer()
    main.mainloop()
