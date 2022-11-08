import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from lang_support import LangSupport
from os import mkdir, path

languages = LangSupport(path.join("Tools", "DrawLanguages"), ignore_file_error=True, ignore_key_error=True, ignore_dict_error=True)


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
        self.langmenu = None
        self.infomenu = None
        self.menubar = None
        self.filemenu = None
        self.create_root()

    def create_root(self):
        self.title(languages.get_text('drawtitle'))
        self.geometry(f"{Cons.window_x}x{Cons.window_y}+"
                      f"{get_center(self, 'x', Cons.window_x)}+{get_center(self, 'y', Cons.window_y)}")
        self.resizable(False, False)
        self.configure(bg=Cons.sim_background_color)

        self.menubar = tk.Menu(self, tearoff=False)
        self.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.filemenu.add_command()  # Open File menu File
        self.filemenu.add_command()  # Save File menu File
        self.filemenu.add_command()  # Export menu File
        for lang in languages.lang_list:
            self.langmenu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        self.filemenu.add_cascade(menu=self.langmenu)  # Language menu File
        self.filemenu.add_separator()
        self.filemenu.add_command(command=self.opensettings_page)  # Settings menu File
        self.filemenu.add_separator()
        self.filemenu.add_command(command=self.quit)  # Exit menu File
        self.menubar.add_cascade(menu=self.filemenu)  # menu File tab

        self.infomenu = tk.Menu(self.menubar, tearoff=False)

    def change_language(self, lang):
        languages.set_language(lang)
        for index, language in enumerate(languages.lang_list):
            if language == lang:
                self.langmenu.entryconfigure(index=index, state=tk.DISABLED)
            else:
                self.langmenu.entryconfigure(index=index, state=tk.NORMAL)
        self.update_widgets()

    def update_widgets(self):
        pass

    def opensettings_page(self):
        window = tk.Toplevel(self)
        window.wm_title(languages.get_text('settingsfilemenu'))
        window.wm_geometry(f"{300}x{200}+"
                           f"{get_center(self, 'x', 300)}+{get_center(self, 'y', 200)}")
        window.resizable(False, False)

        label = tk.Label(window, text="under construction")
        label.pack(expand=True)

        window.grab_set()


def get_center(parent, axis, val):
    assert axis in ['x', 'y']
    ax = {"x": parent.winfo_screenwidth(), "y": parent.winfo_screenheight()}
    return int(ax[axis] / 2 - val / 2)


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()
