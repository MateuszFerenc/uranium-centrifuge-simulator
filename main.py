import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog

from lang_support import LangSupport

sim_background_color = "#AAAAAA"
button_background_color = "#999999"
checkbox_background_color = "#BBBBBB"
list_background_color = "#999999"
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
        self.title(languages.get_text('simtitle'))
        center_x = int(self.winfo_screenwidth() / 2 - window_x / 2)
        center_y = int(self.winfo_screenheight() / 2 - window_y / 2)
        self.geometry(f"{window_x}x{window_y}+{center_x}+{center_y}")
        self.resizable(False, False)
        self.configure(bg=sim_background_color)

        self.menubar = tk.Menu(self, tearoff=False)
        self.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.filemenu.insert_command(index=0, label="")
        self.filemenu.insert_command(index=1, label="")
        self.filemenu.insert_command(index=2, label="")
        self.langmenu = tk.Menu(self.filemenu, tearoff=False)
        for lang in languages.lang_list:
            self.langmenu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        self.filemenu.insert_cascade(index=3, label="", menu=self.langmenu)
        self.filemenu.insert_separator(index=4)
        self.filemenu.insert_command(index=5, label="", command=lambda: self.quit())
        self.filemenu.insert_separator(index=6)
        self.filemenu.insert_command(index=7, label="", command=lambda: self.quit())
        self.menubar.insert_cascade(index=0, label="", menu=self.filemenu)

        self.infomenu = tk.Menu(self.menubar, tearoff=False)
        self.infomenu.insert_command(index=0, label="")
        self.infomenu.insert_command(index=1, label="")
        self.infomenu.insert_separator(index=2)
        self.infomenu.insert_command(index=3, label="")
        self.menubar.insert_cascade(index=1, label="", menu=self.infomenu)

        self.notebook = ttk.Notebook(self, takefocus=False, height=window_y, width=window_x)
        self.notebook.place(rely=0, relwidth=1)

        self.notebook_frames = []
        for win_frame in sim_windows:
            frame = win_frame(parent=self)
            frame.pack(expand=False)
            self.notebook.add(frame, text="")
            self.notebook_frames.append(frame)

        self.change_language(languages.language)

    def change_language(self, lang):
        languages.set_language(lang)
        for index, language in zip(range(len(languages.lang_list)), languages.lang_list):
            if language == lang:
                self.langmenu.entryconfigure(index=index, state=tk.DISABLED)
            else:
                self.langmenu.entryconfigure(index=index, state=tk.ACTIVE)
        self.update_widgets()

    def update_widgets(self):
        self.title(languages.get_text('simtitle'))
        self.menubar.entryconfigure(index=0, label=languages.get_text('filemenu'))
        self.menubar.entryconfigure(index=1, label=languages.get_text('infomenu'))
        self.filemenu.entryconfigure(index=0, label=languages.get_text('openfilemenu'),
                                     command=lambda: filedialog.askopenfile(title=languages.get_text('openfile')))
        self.filemenu.entryconfigure(index=1, label=languages.get_text('savefilemenu'),
                                     command=lambda: filedialog.asksaveasfile(title=languages.get_text('savefile')))
        self.filemenu.entryconfigure(index=2, label=languages.get_text('exportfilemenu'),
                                     command=lambda: filedialog.asksaveasfile(title=languages.get_text('exportfile')))
        self.filemenu.entryconfigure(index=3, label=languages.get_text('languagefilemenu'))
        self.filemenu.entryconfigure(index=5, label=languages.get_text('settingsfilemenu'))
        self.filemenu.entryconfigure(index=7, label=languages.get_text('exitfilemenu'))
        self.infomenu.entryconfigure(index=0, label=languages.get_text('versioninfomenu'),
                                     command=lambda: messagebox.showinfo(title=languages.get_text('versioninfomenu'),
                                                                         message=f"{languages.get_text('simversion').format(sim_version)}\n{languages.get_text('simrelease').format(sim_release_date)}"))
        self.infomenu.entryconfigure(index=1, label=languages.get_text('developerinfomenu'),
                                     command=lambda: messagebox.showinfo(title=languages.get_text('developerinfomenu'),
                                                                         message=languages.get_text('simdev')))
        self.infomenu.entryconfigure(index=3, label=languages.get_text('helpinfomenu'), command=lambda: self.show_help(self))
        for id, tab in zip(range(len(self.notebook_frames)), self.notebook_frames):
            self.notebook.tab(tab_id=id, text=languages.get_text(tab.long_name.lower()))
            tab.content_update()

    @staticmethod
    def show_help(self):
        messagebox.showinfo(title=languages.get_text('helpinfomenu'), message="Test")


class StartWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Start"
        self.long_name = "StartWindow"
        self.parent = parent
        label = ttk.Label(self, text="Tab 0")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass


class InputsWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Inputs"
        self.long_name = "InputsWindow"
        self.parent = parent
        label = ttk.Label(self, text="Tab 1")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass


class ControllersWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Controllers"
        self.long_name = "ControllersWindow"
        self.parent = parent
        label = ttk.Label(self, text="Tab 2")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass


class OutputWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Output"
        self.long_name = "OutputWindow"
        self.parent = parent
        label = ttk.Label(self, text="Tab 3")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass


class ChartsWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Charts"
        self.long_name = "ChartsWindow"
        self.parent = parent
        label = ttk.Label(self, text="Tab 4")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass


sim_windows = (StartWindow, InputsWindow, ControllersWindow, OutputWindow, ChartsWindow)

if __name__ == "__main__":
    main = MainContainer()
    main.mainloop()
