import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from lang_support.lang_support import LangSupportDL
from os import mkdir, path
from PIL import Image, ImageDraw


languages = LangSupportDL(path.basename(__file__).split(".")[0],
                        ignore_file_error=True, ignore_key_error=True, ignore_dict_error=True)


class Cons:
    sim_background_color = "#AAAAAA"
    button_background_color = "#999999"
    checkbox_background_color = "#BBBBBB"
    list_background_color = "#999999"
    window_x = 800
    window_y = 500
    drawing_default_width = 400
    drawing_default_height = 800
    drawing_default_fragment_width = 200
    drawing_default_fragment_height = 100
    undo_max = 10
    redo_max = 10


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.drawing_width = Cons.drawing_default_width
        self.drawing_height = Cons.drawing_default_height
        self.fragment_width = Cons.drawing_default_fragment_width
        self.fragment_height = Cons.drawing_default_fragment_height
        self.langmenu = None
        self.infomenu = None
        self.menubar = None
        self.filemenu = None
        self.create_root()
        self.update_widgets()

    def create_root(self):
        self.title("")
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
        self.langmenu = tk.Menu(self.filemenu, tearoff=False)
        for lang in languages.lang_list:
            self.langmenu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        self.filemenu.add_cascade(menu=self.langmenu)  # Language menu File
        self.filemenu.add_separator()
        self.filemenu.add_command(command=self.opensettings_page)  # Settings menu File
        self.filemenu.add_separator()
        self.filemenu.add_command(command=self.quit)  # Exit menu File
        self.menubar.add_cascade(menu=self.filemenu)  # menu File tab

        self.infomenu = tk.Menu(self.menubar, tearoff=False)
        self.infomenu.add_command()  # Version menu Info
        self.infomenu.add_command()  # Developer menu Info
        self.infomenu.add_separator()
        self.infomenu.add_command(command=self.show_help_page)  # Help menu Info
        self.menubar.add_cascade(menu=self.infomenu)  # menu Info tab

        # self.canvas = tk.Canvas(self, width=600, height=300)
        # self.canvas.pack()

        # self.button1 = tk.Button(self, text="square", command=self.draw_square)
        # self.button1.pack()
        # self.button2 = tk.Button(self, text="circle", command=self.draw_circle)
        # self.button2.pack()
        # self.button3 = tk.Button(self, text="line", command=self.draw_line)
        # self.button3.pack()
        # self.button4 = tk.Button(self, text="Zoom-in", command=self.zoom_in)
        # self.button4.pack()
        # self.button5 = tk.Button(self, text="Zoom-out", command=self.zoom_out)
        # self.button5.pack()

        # self.bind("<Button-1>", self.start_draw)
        # self.bind("<B1-Motion>", self.draw)
        # self.bind("<ButtonRelease-1>", self.stop_draw)

    # def draw_square(self):
    #     self.shape = "square"

    # def draw_circle(self):
    #     self.shape = "circle"

    # def draw_line(self):
    #     self.shape = "line"

    # def start_draw(self, event):
        #     self.start_x = event.x
    #     self.start_y = event.y

    # def draw(self, event):
    #     pass

    # def stop_draw(self, event):
        #     if self.shape == "line":
        #          self.canvas.create_line(self.start_x, self.start_y, event.x, event.y)
        #      elif self.shape == "square":
        #         self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y)
        #     elif self.shape == "circle":
        #         self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y)
        #     self.start_x = None
    #     self.start_y = None

    # def zoom_in(self):
    #     self.canvas.scale("all", 0, 0, 1.1, 1.1)

    # def zoom_out(self):
    #     self.canvas.scale("all", 0, 0, 0.9, 0.9)

    def change_language(self, lang):
        languages.set_language(lang)
        for index, language in enumerate(languages.lang_list):
            if language == lang:
                self.langmenu.entryconfigure(index=index, state=tk.DISABLED)
            else:
                self.langmenu.entryconfigure(index=index, state=tk.NORMAL)
        self.update_widgets()

    def update_widgets(self):
        self.title(languages.get_text('drawtitle'))
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
        self.filemenu.entryconfigure(index=8, label=languages.get_text('exitfilemenu'))
        self.infomenu.entryconfigure(index=0, label=languages.get_text('versioninfomenu'), command=lambda:
        messagebox.showinfo(title=languages.get_text('versioninfomenu'),
                            message=f"{languages.get_text('simversion').format(sim_version)}\n"
                                    f"{languages.get_text('simrelease').format(sim_release_date)}"))
        self.infomenu.entryconfigure(index=1, label=languages.get_text('developerinfomenu'), command=lambda:
        messagebox.showinfo(title=languages.get_text('developerinfomenu'),
                            message=languages.get_text('simdev')))
        self.infomenu.entryconfigure(index=3, label=languages.get_text('helpinfomenu'))

    def opensettings_page(self):
        window = tk.Toplevel(self)
        window.wm_title(languages.get_text('settingsfilemenu'))
        window.wm_geometry(f"{300}x{200}+"
                           f"{get_center(self, 'x', 300)}+{get_center(self, 'y', 200)}")
        window.resizable(False, False)

        label = tk.Label(window, text="under construction")
        label.pack(expand=True)

        window.grab_set()

    def show_help_page(self):
        pass

    def create_drawing_zone(self):
        for x in range(int(self.drawing_width / self.fragment_width)):
            for y in range(int(self.drawing_height / self.fragment_height)):
                pass

    def delete_drawing_zone(self):
        pass

    def update_drawing_zone(self):
        self.drawing_width = 0
        self.drawing_height = 0
        self.fragment_width = 0
        self.fragment_height = 0
        self.delete_drawing_zone()
        self.create_drawing_zone()
        self.render_drawing()

    def render_drawing(self):
        pass


def get_center(parent, axis, val):
    assert axis in ['x', 'y']
    ax = {"x": parent.winfo_screenwidth(), "y": parent.winfo_screenheight()}
    return int(ax[axis] / 2 - val / 2)


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()
