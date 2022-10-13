import re
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from os import listdir, path, remove
from atexit import register as register_exit

from lang_support import LangSupport
from version_supervisor import DataLogger

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

languages = LangSupport("SimLanguages", ignore_file_error=True, ignore_key_error=True, ignore_dict_error=True)

dl = DataLogger(__name__, 'logs')
dl.config_logger(do_log=False)  # remove in future

exit_tasks = {}


class Cons:
    sim_background_color = "#AAAAAA"
    button_background_color = "#999999"
    checkbox_background_color = "#BBBBBB"
    list_background_color = "#999999"
    window_x = 800
    window_y = 500


class MainContainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.notebook_frames = None
        self.notebook = None
        self.infomenu = None
        self.langmenu = None
        self.filemenu = None
        self.menubar = None
        self.create_window()
        self.change_language(languages.language)

    def create_window(self):
        self.title(languages.get_text('simtitle'))
        center_x = int(self.winfo_screenwidth() / 2 - Cons.window_x / 2)
        center_y = int(self.winfo_screenheight() / 2 - Cons.window_y / 2)
        self.geometry(f"{Cons.window_x}x{Cons.window_y}+{center_x}+{center_y}")
        self.resizable(False, False)
        self.configure(bg=Cons.sim_background_color)

        self.menubar = tk.Menu(self, tearoff=False)
        self.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.filemenu.add_command()  # Open File menu File
        self.filemenu.add_command()  # Save File menu File
        self.filemenu.add_command()  # Export menu File
        self.langmenu = tk.Menu(self.filemenu, tearoff=False)
        for lang in languages.lang_list:
            self.langmenu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        self.filemenu.add_cascade(menu=self.langmenu)  # Language menu File
        self.filemenu.add_separator()
        self.filemenu.add_command(command=self.opensettings)  # Settings menu File
        self.filemenu.add_command(command=self.clearlogs)
        self.filemenu.add_separator()  # Clear logs menu File
        self.filemenu.add_command(command=self.quit)  # Exit menu File
        self.menubar.add_cascade(menu=self.filemenu)  # menu File tab

        self.infomenu = tk.Menu(self.menubar, tearoff=False)
        self.infomenu.add_command()  # Version menu Info
        self.infomenu.add_command()  # Developer menu Info
        self.infomenu.add_separator()
        self.infomenu.add_command()  # Help menu Info
        self.menubar.add_cascade(menu=self.infomenu)  # menu Info tab

        self.notebook = ttk.Notebook(self, takefocus=False, height=Cons.window_y, width=Cons.window_x)
        self.notebook.place(rely=0, relwidth=1)

        self.notebook_frames = []
        for win_frame in sim_windows:
            frame = win_frame(parent=self)
            frame.pack(expand=False)
            self.notebook.add(frame)
            self.notebook_frames.append(frame)

    def change_language(self, lang):
        languages.set_language(lang)
        for index, language in enumerate(languages.lang_list):
            if language == lang:
                self.langmenu.entryconfigure(index=index, state=tk.DISABLED)
            else:
                self.langmenu.entryconfigure(index=index, state=tk.NORMAL)
        self.update_widgets()

    def update_widgets(self):
        self.title(languages.get_text('simtitle'))
        for index, tab in enumerate(['filemenu', 'infomenu']):
            self.menubar.entryconfigure(index, label=languages.get_text(tab))
        self.filemenu.entryconfigure(index=0, label=languages.get_text('openfilemenu'),
                                     command=lambda: filedialog.askopenfile(title=languages.get_text('openfile')))
        self.filemenu.entryconfigure(index=1, label=languages.get_text('savefilemenu'),
                                     command=lambda: filedialog.asksaveasfile(title=languages.get_text('savefile')))
        self.filemenu.entryconfigure(index=2, label=languages.get_text('exportfilemenu'),
                                     command=lambda: filedialog.asksaveasfile(title=languages.get_text('exportfile')))
        self.filemenu.entryconfigure(index=3, label=languages.get_text('languagefilemenu'))
        self.filemenu.entryconfigure(index=5, label=languages.get_text('settingsfilemenu'))
        self.filemenu.entryconfigure(index=6, label=languages.get_text('clearlogsfilemenu'))
        self.filemenu.entryconfigure(index=8, label=languages.get_text('exitfilemenu'))
        self.infomenu.entryconfigure(index=0, label=languages.get_text('versioninfomenu'), command=lambda:
        messagebox.showinfo(title=languages.get_text('versioninfomenu'),
                            message=f"{languages.get_text('simversion').format(sim_version)}\n"
                                    f"{languages.get_text('simrelease').format(sim_release_date)}"))
        self.infomenu.entryconfigure(index=1, label=languages.get_text('developerinfomenu'), command=lambda:
        messagebox.showinfo(title=languages.get_text('developerinfomenu'),
                            message=languages.get_text('simdev')))
        self.infomenu.entryconfigure(index=3, label=languages.get_text('helpinfomenu'),
                                     command=lambda: self.show_help())
        for tab_id, tab in enumerate(self.notebook_frames):
            self.notebook.tab(tab_id, text=languages.get_text(tab.long_name.lower()))
            tab.content_update()

    def show_help(self):
        window = tk.Toplevel(self)
        window.wm_title(languages.get_text('helppage'))
        window_x = 300
        window_y = 200
        center_x = int(self.winfo_screenwidth() / 2 - window_x / 2)
        center_y = int(self.winfo_screenheight() / 2 - window_y / 2)
        window.wm_geometry(f"{window_x}x{window_y}+{center_x}+{center_y}")
        label = tk.Label(window, text="under construction")
        label.pack(expand=True)

    def clearlogs(self):
        def select_dir(event):
            sel_dir = dir_list.get(dir_list.curselection())
            if path.isdir(path.abspath(sel_dir)):
                dir_path.append(sel_dir)
                logs = load_dirs(sel_dir)
                if len(logs):
                    button_clear.configure(state=tk.ACTIVE, command=lambda: clear_logs(logs))

        def prev_dir(event):
            if len(dir_path):
                dir_path.pop()
                load_dirs(dir_path[-1] if len(dir_path) else None)

        def clear_logs(logs):
            for log in logs:
                # if path.isfile(path.abspath(log)) and re.match('.*\.log', str(dir)):
                file = str('\\'.join(dir_path) + '\\' + log)
                exit_tasks[file] = 'remove-file'
            button_clear.configure(state=tk.DISABLED)
            messagebox.showinfo(title=languages.get_text('infomenu'),
                                message=languages.get_text('logsclearinfo'))
            window.destroy()

        def load_dirs(search):
            dirs = listdir(search)
            dir_search = []
            logs = []
            for dir in dirs:
                if path.isdir(path.abspath(dir)) and re.match('^[\.]', str(dir)) is None:
                    dir_search.append(dir)
                elif re.match(f'.*\.{dl.logextension}', str(dir)) \
                        and str('\\'.join(dir_path) + '\\' + dir) not in list(exit_tasks.keys()):
                    dir_search.append(dir)
                    logs.append(dir)
            dir_var = tk.Variable(value=dir_search)
            dir_list.configure(listvariable=dir_var, state=tk.NORMAL if len(dir_search) else tk.DISABLED)
            return logs

        window = tk.Toplevel(self)
        window.wm_title(languages.get_text('clearlogsfilemenu'))
        window_x = 300
        window_y = 200
        center_x = int(self.winfo_screenwidth() / 2 - window_x / 2)
        center_y = int(self.winfo_screenheight() / 2 - window_y / 2)
        window.wm_geometry(f"{window_x}x{window_y}+{center_x}+{center_y}")
        window.resizable(False, False)

        window.columnconfigure(index=0, weight=1)
        window.columnconfigure(index=1, weight=1)
        window.rowconfigure(index=0, weight=1)
        window.rowconfigure(index=1, weight=1)

        dir_var = tk.Variable(value=None)
        dir_list = tk.Listbox(window, listvariable=dir_var, height=6, width=30, selectmode=tk.SINGLE)
        dir_list.grid(column=0, row=0, columnspan=2)
        button_back = ttk.Button(window, text=languages.get_text('backbutton'))
        button_back.grid(column=0, row=1)
        button_clear = ttk.Button(window, text=languages.get_text('clearbutton'), state=tk.DISABLED)
        button_clear.grid(column=1, row=1)
        load_dirs(None)
        dir_path = []
        dir_list.bind('<<ListboxSelect>>', select_dir)
        button_back.bind('<Button-1>', prev_dir)
        window.grab_set()

    def opensettings(self):
        window = tk.Toplevel(self)
        window.wm_title(languages.get_text('settingsfilemenu'))
        window_x = 300
        window_y = 200
        center_x = int(self.winfo_screenwidth() / 2 - window_x / 2)
        center_y = int(self.winfo_screenheight() / 2 - window_y / 2)
        window.wm_geometry(f"{window_x}x{window_y}+{center_x}+{center_y}")
        label = tk.Label(window, text="under construction")
        label.pack(expand=True)


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


def at_exit():
    for file, task in exit_tasks.items():
        if task == 'remove-file':
            remove(file)


sim_windows = (StartWindow, InputsWindow, ControllersWindow, OutputWindow, ChartsWindow)

if __name__ == "__main__":
    register_exit(at_exit)
    main = MainContainer()
    main.mainloop()
    for inst in DataLogger.instances:
        del inst
