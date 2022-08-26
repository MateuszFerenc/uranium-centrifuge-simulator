import sys
from os import system, abort
from datetime import datetime
from tkinter import Tk, Label, Button, Frame


class VersionSupervisor:
    def __init__(self):
        super().__init__()
        self.data = None
        self.stable, self.beta, self.alfa = 0, 0, 0
        self.stable_max, self.beta_max, self.alfa_max = 9, 99, 999

    def run_cli(self, script):
        system("py " + script)
        usr_input = input("Does this version of project work? (if yes, update project version with specified type)")
        if usr_input.lower() in ("y", "yes", "yeah", "yep"):
            self.read_version()
            usr_input = ''
            if len(self.data) > 0:
                while usr_input not in ('s', 'b', 'a'):
                    usr_input = input("Select release type (s - stable, b - beta, a - alfa) [abort for cancellation]")
                    if usr_input == 'abort':
                        abort()
            self.count_version(usr_input)
            self.update_version()

    def run_gui(self, script):
        vs = GUI()
        system("py " + script)
        vs.run()

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
                    self.alfa, self.beta = 0
                    user_selection = 's'
            if user_selection == 's':
                if self.stable < self.stable_max:
                    self.stable += 1
                    self.alfa, self.beta = 0, 0
                else:
                    print("Reached maximal version!")
                    self.stable, self.beta, self.alfa = 0, 0, 0

    def update_version(self):
        version_data = open("version_status", "w")
        version_data.write(f"version#{self.stable:1n}.{self.beta:02n}.{self.alfa:003n}\n")
        now = datetime.now()
        version_data.write("release_date#{}/{}/{}".format(now.strftime("%d"),
                                                          now.strftime("%m"), now.strftime("%Y")))
        version_data.close()


class GUI(object):
    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.root.title("Python project version supervisor")
        self.root.geometry("100x50")
        self.root.resizable(False, False)
        self.root.configure(bg="#999999")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.frame = Frame(self.root)
        self.root.label0 = Label(self.frame, text="Does this version of project work?")
        self.root.button0 = Button(self.frame, text="Yes")
        self.root.button1 = Button(self.frame, text="No")
        self.root.label1 = Label(self.frame, text="Select release type:")
        self.root.button2 = Button(self.frame, text="Stable")
        self.root.button3 = Button(self.frame, text="Beta")
        self.root.button4 = Button(self.frame, text="Alfa")
        self.root.label0.grid(row=0)
        self.root.button0.grid(row=1, column=0)
        self.root.button1.grid(row=1, column=1)
        self.root.button0.config(command=lambda: self.version_check(self, True))
        self.root.button1.config(command=lambda: self.version_check(self, False))
        self.root.label1.grid(row=2)
        self.root.button2.grid(row=3, column=0)
        self.root.button3.grid(row=3, column=1)
        self.root.button4.grid(row=3, column=2)
        self.root.button2.config(command=lambda: self.incr_version("s"), state="disabled")
        self.root.button3.config(command=lambda: self.incr_version("b"), state="disabled")
        self.root.button4.config(command=lambda: sself.incr_version("a"), state="disabled")

    def run(self):
        self.root.mainloop()

    def version_check(self, root, selection):
        root.button0.config(state="disable")
        root.button1.config(state="disable")

    def incr_version(self, version):
        pass


def help_cli():
    print("Format:\n{} -hc <script.py>")
    print("...")


if __name__ == "__main__":
    vs = VersionSupervisor()
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            help_cli()
        elif sys.argv[1].endswith(".py"):
            vs.run_gui(sys.argv[1])
        else:
            print("Wrong argument: {}".format(sys.argv[1]))
    elif len(sys.argv) == 3:
        if '-h' in (sys.argv[1], sys.argv[2]):
            help_cli()
        elif '-c' in (sys.argv[1], sys.argv[2]):
            for arg in (sys.argv[1], sys.argv[2]):
                if arg.endswith(".py"):
                    vs.run_cli(arg)
        else:
            print("Wrong arguments: {} {}".format(sys.argv[1], sys.argv[2]))
    else:
        print("Too {} arguments! Try running with -h switch".format("few" if len(sys.argv) < 2 else "many"))
