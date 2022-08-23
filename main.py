import tkinter as tk
from tkinter import ttk
from lang_support import LangSupport

sim_background_color = "#AAAAAA"
button_background_color = "#999999"
checkbox_background_color = "#BBBBBB"
list_background_color = "#999999"
sim_title = "Uranium Centrifuge Simulator"
sim_windows_dimensions = "800x500"
sim_release_date = "23/08/2022"
sim_version = "V0.00.001.2308_22"

languages = LangSupport()


class MainContainer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(languages.get_text('sim_title'))
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
        self.parent = parent
        self.create_ui()

    def create_ui(self):
        # create the input frame
        input_frame = MainButtonsFrame(self, self.parent)
        input_frame.grid(column=0, row=0)

        # create the button frame
        button_frame = MainInfoFrame(self, self.parent)
        button_frame.grid(column=1, row=0)

    def update_ui(self):
        self.controller.update()  # todo window update


class MainInfoFrame(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.parent = parent

        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text=languages.get_text('siminfo0')).grid(column=0, row=0)
        ttk.Label(self, text=languages.get_text('siminfo1')).grid(column=1, row=1)
        ttk.Label(self, text=languages.get_text('siminfo2').format(sim_version)).grid(column=1, row=2)
        ttk.Label(self, text=languages.get_text('siminfo3').format(sim_release_date)).grid(column=1, row=3)


class MainButtonsFrame(ttk.Frame):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.lang_listbox = None
        self.columnconfigure(0, weight=1)
        self.parent = parent

        self.create_ui()

    def create_ui(self):
        ttk.Button(self, text=languages.get_text('lsim')).grid(column=0, row=0)
        ttk.Button(self, text=languages.get_text('wdocu')).grid(column=0, row=1)
        ttk.Label(self, text=languages.get_text('chlang')).grid(column=0, row=2)
        lang_list = languages.get_languages()
        lb0 = tk.Listbox(self, selectmode="SINGLE", height=1*len(lang_list))
        for LANG in lang_list:
            lb0.insert('end', LANG)
        lb0.grid(column=0, row=3)
        lb0.bind('<<ListboxSelect>>', self.lang_select)
        self.lang_listbox = lb0

        # ttk.Button(self, text=languages.get_text('chlang')).grid(column=0, row=2)

    def lang_select(self, event):
        selection = self.lang_listbox.get(self.lang_listbox.curselection())
        print("selected {}".format(selection))
        languages.set_language(selection)
        self.parent.update_ui() # todo window update


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
