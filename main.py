from tkinter import *
from lang_support import LangSupport

sim_background_color = "#AAAAAA"
button_background_color = "#999999"
checkbox_background_color = "#BBBBBB"
list_background_color = "#999999"
sim_title = "Uranium Centrifuge Simulator"
sim_windows_dimensions = "800x500"

try:
    with open("version_status", "r") as version_data:
        data = {}
        for line in version_data:
            split_line = line.strip().split("#", 1)
            data[split_line[0]] = split_line[1]
        version_data.close()
        sim_version = data['version']
        sim_release_date = data['release_date']
except FileNotFoundError:
    sim_version = "Not specified"
    sim_release_date = "Not specified"


languages = LangSupport()


class MainContainer(Tk):
    def __init__(self):
        super().__init__()
        self.title(sim_title)
        self.geometry(sim_windows_dimensions)
        self.resizable(False, False)
        self.configure(bg=sim_background_color)

        mywindow = Frame(self)
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


class StartWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.buttons_frame = MainButtonsFrame(self)
        self.text_frame = MainInfoFrame(self)
        self.create_ui()

    def create_ui(self):
        self.buttons_frame.grid(column=0, row=0)
        self.text_frame.grid(column=1, row=0)

    def update_frames(self):
        self.buttons_frame.update_ui()
        self.text_frame.update_ui()


class MainInfoFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.label0 = Label(self, text="")
        self.label1 = Label(self, text="")
        self.label2 = Label(self, text="")
        self.label3 = Label(self, text="")
        self.label4 = Label(self, text="")

        self.create_ui()
        self.update_ui()

    def create_ui(self):
        self.label0.grid(column=0, row=0)
        self.label1.grid(column=1, row=1)
        self.label2.grid(column=1, row=2)
        self.label3.grid(column=1, row=3)
        self.label4.grid(column=1, row=4)

    def update_ui(self):
        self.label0.configure(text=languages.get_text('simtitle'))
        self.label1.configure(text=languages.get_text('siminfo0'))
        self.label2.configure(text=languages.get_text('siminfo1'))
        self.label3.configure(text=languages.get_text('siminfo2').format(sim_version))
        self.label4.configure(text=languages.get_text('siminfo3').format(sim_release_date))


class MainButtonsFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.button0 = Button(self, text="")
        self.button1 = Button(self, text="")
        self.label0 = Label(self, text="")
        self.lang_list = languages.get_languages()
        self.listbox0 = Listbox(self, selectmode="SINGLE", height=1 * len(self.lang_list))
        self.columnconfigure(0, weight=1)

        self.create_ui()
        self.update_ui()

    def create_ui(self):
        self.button0.grid(column=0, row=0)
        self.button1.grid(column=0, row=1)
        self.label0.grid(column=0, row=2)
        for LANG in self.lang_list:
            self.listbox0.insert('end', LANG)
        self.listbox0.grid(column=0, row=3)
        self.listbox0.bind('<<ListboxSelect>>', self.lang_select)

    def lang_select(self, event):
        selection = self.listbox0.get(self.listbox0.curselection())
        languages.set_language(selection)
        self.parent.update_frames()

    def update_ui(self):
        self.button0.configure(text=languages.get_text('lsim'))
        self.button1.configure(text=languages.get_text('wdocu'))
        self.label0.configure(text=languages.get_text('chlang'))


class InputsWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        pass


class ControllersWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        pass


class OutputWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        pass


class ChartsWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        pass


sim_windows = (StartWindow, InputsWindow, ControllersWindow, OutputWindow, ChartsWindow)

if __name__ == "__main__":
    main = MainContainer()
    main.mainloop()
