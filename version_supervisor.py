from sys import exit
from os import environ, name
from os.path import join
from subprocess import run
import argparse
from datetime import datetime
from tkinter import Tk, Label, Button, Frame
import json


class VersionSupervisor:
    def __init__(self):
        self.configuration_data = {}
        self.stable, self.beta, self.alfa = 0, 0, 0
        self.stable_max, self.beta_max, self.alfa_max = 9, 99, 999

    def run_cli(self):
        usr_input = input("Does this version of project work? (if yes, update project version with specified type)\n?")
        if usr_input.lower() in ("y", "yes", "yeah", "yep"):
            self.read_version()
            usr_input = ''
            while usr_input not in ('s', 'b', 'a'):
                usr_input = input(
                    "Select release type (s - stable, b - beta, a - alfa) [abort for cancellation]\n?")
                if usr_input == "abort":
                    exit()
            self.count_version(usr_input)
            self.update_version()

    def run_gui(self):
        vsgui = GUI(self)
        vsgui.run()
        exit()

    def read_version(self):
        try:
            with open("config_data.json", "r") as version_data:
                try:
                    self.configuration_data = json.load(version_data)
                    if 'version' not in self.configuration_data:
                        self.configuration_data['version'] = f"0.00.000"
                    if 'release_date' not in self.configuration_data:
                        self.configuration_data['release_version'] = None
                except json.JSONDecodeError:
                    print("config_data.json is corrupted")
                    exit(3)
        except FileNotFoundError:
            pass

    def count_version(self, user_selection):
        if user_selection in ('s', 'b', 'a'):
            split_line = self.configuration_data['version'].strip().split('.')
            self.stable, self.beta, self.alfa = int(split_line[0]), int(split_line[1]), int(split_line[2])
            if user_selection == 'a':
                if self.alfa < self.alfa_max:
                    self.alfa += 1
                else:
                    self.alfa = 0
                    user_selection = 'b'
            elif user_selection == 'b':
                if self.beta < self.beta_max:
                    self.beta += 1
                    self.alfa = 0
                else:
                    self.alfa, self.beta = 0, 0
                    user_selection = 's'
            elif user_selection == 's':
                if self.stable < self.stable_max:
                    self.stable += 1
                    self.alfa, self.beta = 0, 0
                else:
                    print("Reached max version!")
                    self.stable, self.beta, self.alfa = 0, 0, 0

    def update_version(self):
        with open("config_data.json", 'w') as version_write:
            self.configuration_data['version'] = f"{self.stable:1n}.{self.beta:02n}.{self.alfa:003n}"
            now = datetime.now()
            self.configuration_data['release_date'] = f"{now.day}/{now.month:02n}/{now.year}"
            json.dump(self.configuration_data, version_write, indent=4)


class GUI(Tk):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.frame = None

    def create_root(self):
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
        self.frame.button0 = Button(self, text="Yes", bg="#AAAAAA", width=5, relief="ridge", cursor="heart",
                                    fg="#FFFFFF", font=("Helvetica", 10))
        self.frame.button1 = Button(self, text="No", bg="#AAAAAA", width=5, relief="ridge", cursor="pirate",
                                    fg="#FFFFFF", font=("Helvetica", 10))
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

        self.frame.button0.bind("<Button-1>", self.yes_button)
        self.frame.button1.bind("<Button-1>", self.no_button)

    def run(self):
        self.create_root()
        self.parent.read_version()
        self.frame.label2.config(text=f"version : {self.parent.configuration_data['version']}\n"
                                      f"release date : {self.parent.configuration_data['release_date']}")
        self.mainloop()

    def incr_version(self, v):
        self.parent.count_version(v)
        self.parent.update_version()
        self.destroy()
        exit()

    def yes_button(self, event):
        self.frame.button0.config(state="disabled")
        self.frame.button2.config(state="normal")
        self.frame.button3.config(state="normal")
        self.frame.button4.config(state="normal")

    def no_button(self, event):
        self.destroy()
        exit()


if __name__ == "__main__":
    version = VersionSupervisor()
    parser = argparse.ArgumentParser(description=f"Script version supervisor Copyright ({datetime.now().year}) Mateusz Ferenc")
    parser.add_argument("script", type=str,
                        help="python (only) script to execute and supervise version")
    parser.add_argument("-d", "--debug", help="Debug mode (Does not update version, no ask window)",
                        action="store_true")
    parser.add_argument("-c", "--cli", help="Command Line Interface mode, no GUI (Default GUI mode)",
                        action="store_true")
    args = parser.parse_args()

    py_exe = join(environ["VIRTUAL_ENV"], "Scripts" if name == "nt" else "bin", "python") if "VIRTUAL_ENV" in environ else "python"
    status = run([py_exe, args.script], text=True, capture_output=True)

    print(f"Stats:\n"\
          f"\treturn code: {status.returncode}\n")
    print(f"\tstdout: ", end='')
    if len(status.stdout):
        print()
        for line in status.stdout.splitlines():
            print('\t' + ' '*8 + line)
    else:
        print("None")
    print(f"\tstderr: ", end='')
    if len(status.stderr):
        print()
        for line in status.stderr.splitlines():
            print('\t' + ' '*8 + line)
    else:
        print("None")

    if not args.debug and status.returncode == 0:
        if args.cli:
            version.run_cli()
        else:
            version.run_gui()
