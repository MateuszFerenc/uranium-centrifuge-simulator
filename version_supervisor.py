from sys import exit, argv
from os import system
from datetime import datetime
from tkinter import Tk, Label, Button, Frame


class VersionSupervisor:
    def __init__(self):
        super().__init__()
        self.data = None
        self.stable, self.beta, self.alfa = 0, 0, 0
        self.stable_max, self.beta_max, self.alfa_max = 9, 99, 999

    def run_cli(self, script):
        if system("py " + script) != 0:
            exit()
        usr_input = input("Does this version of project work? (if yes, update project version with specified type)\n?")
        if usr_input.lower() in ("y", "yes", "yeah", "yep"):
            self.read_version()
            usr_input = ''
            if len(self.data) > 0:
                while usr_input not in ('s', 'b', 'a'):
                    usr_input = input("Select release type (s - stable, b - beta, a - alfa) [abort for cancellation]\n?")
                    if usr_input == 'abort':
                        exit()
            self.count_version(usr_input)
            self.update_version()

    def run_gui(self, script):
        vsgui = GUI()
        if system("py " + script) == 0:
            vsgui.run(self)
        exit()

    @staticmethod
    def help_cli():
        print("Format:\n{} -hc <script.py>")
        print("Simple version update supervisor, when parsed script ends executions, "
              "script asks about decision about version.")
        print("Options:\n"
              "     -c : run in CLI mode, if not specified run in GUI mode\n"
              "     -h : print this help\n"
              "     <script.py> : python (only) script to execute and supervise version\n"
              "Copyright (2022) Mateusz Ferenc")

    def read_version(self):
        self.data = {}
        try:
            with open("version_status", "r") as version_data:
                for line in version_data:
                    split_line = line.strip().split("#", 1)
                    self.data[split_line[0]] = split_line[1]
                version_data.close()
        except FileNotFoundError:
            pass

    def count_version(self, user_selection):
        if user_selection in ('s', 'b', 'a'):
            split_line = self.data['version'].strip().split(".")
            self.stable, self.beta, self.alfa = int(split_line[0]), int(split_line[1]), int(split_line[2])
            if user_selection == 'a':
                if self.alfa < self.alfa_max:
                    self.alfa += 1
                else:
                    self.alfa = 0
                    user_selection = 'b'
            if user_selection == 'b':
                if self.beta < self.beta_max:
                    self.beta += 1
                    self.alfa = 0
                else:
                    self.alfa, self.beta = 0, 0
                    user_selection = 's'
            if user_selection == 's':
                if self.stable < self.stable_max:
                    self.stable += 1
                    self.alfa, self.beta = 0, 0
                else:
                    print("Reached max version!")
                    self.stable, self.beta, self.alfa = 0, 0, 0

    def update_version(self):
        version_data = open("version_status", "w")
        version_data.write(f"version#{self.stable:1n}.{self.beta:02n}.{self.alfa:003n}\n")
        now = datetime.now()
        version_data.write(f"release_date#{now:%d}/{now:%m}/{now:%Y}")
        version_data.close()


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.parent = None
        self.title("Python project version supervisor")
        window_x = 350
        window_y = 200
        center_x = int(self.winfo_screenwidth() / 2 - window_x / 2)
        center_y = int(self.winfo_screenheight() / 2 - window_y / 2)
        self.geometry(f"{window_x}x{window_y}+{center_x}+{center_y}")
        self.resizable(False, False)
        self.configure(bg="#999999")
        self.attributes("-topmost", 1)

        self.frame = Frame(self)
        self.frame.label0 = Label(self, text="Does this version of project work?",
                                  bg="#999999", fg="#FFFFFF", font=("Helvetica", 12))
        self.frame.button0 = Button(self, text="Yes", bg="#AAAAAA", command=lambda: self.version_check('yes'),
                                    width=5, relief="ridge", cursor='heart', fg="#FFFFFF", font=("Helvetica", 10))
        self.frame.button1 = Button(self, text="No", bg="#AAAAAA", command=lambda: self.version_check('no'),
                                    width=5, relief="ridge", cursor='pirate', fg="#FFFFFF", font=("Helvetica", 10))
        self.frame.label1 = Label(self, text="Current version data:", bg="#999999", fg="#FFFFFF",
                                  font=("Helvetica", 10))
        self.frame.label2 = Label(self, text="", bg="#999999", fg="#FFFFFF", font=("Helvetica", 10))
        self.frame.label3 = Label(self, text="Select release type:", bg="#999999", fg="#FFFFFF",
                                  font=("Helvetica", 10))
        self.frame.button2 = Button(self, text="Stable", bg="#AAAAAA", command=lambda: self.incr_version("s"),
                                    state="disabled", width=5, relief="sunken", fg="#FFFFFF", font=("Helvetica", 10))
        self.frame.button3 = Button(self, text="Beta", bg="#AAAAAA", command=lambda: self.incr_version("b"),
                                    state="disabled", width=5, relief="sunken", fg="#FFFFFF", font=("Helvetica", 10))
        self.frame.button4 = Button(self, text="Alfa", bg="#AAAAAA", command=lambda: self.incr_version("a"),
                                    state="disabled", width=5, relief="sunken", fg="#FFFFFF", font=("Helvetica", 10))
        self.frame.label0.place(relx=0, rely=0, relwidth=1)
        self.frame.button0.place(relx=0.1, rely=0.15, relwidth=0.3)
        self.frame.button1.place(relx=0.6, rely=0.15, relwidth=0.3)
        self.frame.label1.place(relx=0, rely=0.3, relwidth=1)
        self.frame.label2.place(relx=0, rely=0.4, relwidth=1)
        self.frame.label3.place(relx=0, rely=0.6, relwidth=1)
        self.frame.button2.place(relx=0.1, rely=0.75, relwidth=0.2)
        self.frame.button3.place(relx=0.4, rely=0.75, relwidth=0.2)
        self.frame.button4.place(relx=0.7, rely=0.75, relwidth=0.2)

    def run(self, parent):
        self.parent = parent
        self.parent.read_version()
        self.frame.label2.config(text=f"version : {self.parent.data['version']}\n"
                                      f"release date : {self.parent.data['release_date']}")
        self.mainloop()

    def version_check(self, selection):
        if selection == 'yes':
            self.frame.button0.config(state="disabled")
            # self.frame.button1.config(state="disabled") could be useful if accidentally clicked yes
            self.frame.button2.config(state="normal")
            self.frame.button3.config(state="normal")
            self.frame.button4.config(state="normal")
        else:
            self.destroy()
            exit()

    def incr_version(self, v):
        self.frame.button2.config(state="disabled")
        self.frame.button3.config(state="disabled")
        self.frame.button4.config(state="disabled")
        self.parent.count_version(v)
        self.parent.update_version()
        self.destroy()
        exit()


if __name__ == "__main__":
    version = VersionSupervisor()
    if len(argv) == 2:
        if argv[1] == '-h':
            version.help_cli()
        elif argv[1].endswith(".py"):
            version.run_gui(argv[1])
        else:
            print("Wrong argument: {}".format(argv[1]))
    elif len(argv) == 3:
        if '-h' in (argv[1], argv[2]):
            version.help_cli()
        elif '-c' in (argv[1], argv[2]):
            for arg in (argv[1], argv[2]):
                if arg.endswith(".py"):
                    version.run_cli(arg)
        else:
            print("Wrong arguments: {} {}".format(argv[1], argv[2]))
    else:
        print("Too {} arguments! Try running with -h switch".format("few" if len(argv) < 2 else "many"))
