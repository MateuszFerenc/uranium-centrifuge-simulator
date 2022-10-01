import tkinter as tk
import tkinter.ttk as ttk

from lang_support import LangSupport

sim_background_color = "#AAAAAA"
button_background_color = "#999999"
checkbox_background_color = "#BBBBBB"
list_background_color = "#999999"
sim_title = "Uranium Centrifuge Simulator"
window_x = 800
window_y = 500

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


class MainContainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(sim_title)
        center_x = int(self.winfo_screenwidth() / 2 - window_x / 2)
        center_y = int(self.winfo_screenheight() / 2 - window_y / 2)
        self.geometry(f"{window_x}x{window_y}+{center_x}+{center_y}")
        self.resizable(False, False)
        self.configure(bg=sim_background_color)

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Export")
        filemenu.add_command(label="Import")
        langmenu = tk.Menu(filemenu)
        for lang in languages.lang_list:
            langmenu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        filemenu.add_cascade(label="Language", menu=langmenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        infomenu = tk.Menu(menubar)
        infomenu.add_command(label="Version")
        infomenu.add_command(label="Developer")
        infomenu.add_separator()
        infomenu.add_command(label="Help")
        menubar.add_cascade(label="Info", menu=infomenu)

        notebook = ttk.Notebook(self, takefocus=True, height=window_y, width=window_x)
        notebook.place(rely=0, relwidth=1)

        self.notebook_frames = {}
        for win_frame in sim_windows:
            frame = win_frame(parent=self)
            frame_name = frame.name
            frame.pack(expand=False)
            notebook.add(frame, text=frame_name)
            # self.notebook_frames[frame_name] = tab

    def change_language(self, lang):
        print(lang)

    def exit(self):
        self.quit()


class StartWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Start"
        self.parent = parent
        label = ttk.Label(self, text="Tab 0")
        label.pack()

    def create_ui(self):
        self.buttons_frame.grid(column=0, row=0)
        self.text_frame.grid(column=1, row=0)

    def update_frames(self):
        self.buttons_frame.update_ui()
        self.text_frame.update_ui()


"""class StartInfoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.label0 = ttk.Label(self, text="")
        self.label1 = ttk.Label(self, text="")
        self.label2 = ttk.Label(self, text="")
        self.label3 = ttk.Label(self, text="")
        self.label4 = ttk.Label(self, text="")

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


class StartButtonsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.button0 = ttk.Button(self, text="", command=lambda: self.parent.controller.show_frame('InputsWindow'))
        self.button1 = ttk.Button(self, text="")
        self.label0 = ttk.Label(self, text="")
        self.lang_list = languages.get_languages()
        self.listbox0 = tk.Listbox(self, selectmode="SINGLE", height=1 * len(self.lang_list))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

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
"""


class InputsWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Inputs"
        self.parent = parent
        label = ttk.Label(self, text="Tab 1")
        label.pack()

    def create_ui(self):
        self.input_buttons.grid(row=0, column=0)

    def update_frames(self):
        self.input_buttons.update_ui()


"""class InputsButtonsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.button0 = ttk.Button(self, text="", command=lambda: self.parent.controller.show_frame('StartWindow'))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_ui()
        self.update_ui()

    def create_ui(self):
        self.button0.grid(column=0, row=0)

    def update_ui(self):
        self.button0.configure(text=languages.get_text('winstart'))
"""


class ControllersWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Controllers"
        self.parent = parent
        label = ttk.Label(self, text="Tab 2")
        label.pack()
        # self.create_ui()

    def create_ui(self):
        pass


class OutputWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Output"
        self.parent = parent
        label = ttk.Label(self, text="Tab 3")
        label.pack()
        # self.create_ui()

    def create_ui(self):
        pass


class ChartsWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Charts"
        self.parent = parent
        label = ttk.Label(self, text="Tab 4")
        label.pack()
        # self.create_ui()

    def create_ui(self):
        pass


sim_windows = (StartWindow, InputsWindow, ControllersWindow, OutputWindow, ChartsWindow)

if __name__ == "__main__":
    main = MainContainer()
    main.mainloop()
