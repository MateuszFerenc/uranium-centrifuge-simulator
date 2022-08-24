import sys
from os import system, abort
from datetime import datetime

if __name__ == "__main__":
    if sys.argv[1].endswith(".py"):
        system(sys.argv[1])
    else:
        print("No python file specified!")
        abort()

    usr_input = input("Does this version of project work? (if yes, update project version with specified type)")
    if usr_input.lower() in ("y", "yes", "yeah", "yep"):
        data = {}
        try:
            with open("version_status", "r") as version_data:
                for line in version_data:
                    split_line = line.strip().split("#", 1)
                    data[split_line[0]] = split_line[1]
                version_data.close()
        except FileNotFoundError:
            pass
        stable, beta, alfa = 0, 0, 0  # change all to 0, when you figure out how to display them
        stable_max, beta_max, alfa_max = 9, 99, 999
        if len(data) > 0:
            usr_input = ''
            while usr_input not in ('s', 'b', 'a'):
                usr_input = input("Select release type (s - stable, b - beta, a - alfa) [abort for cancellation]")
                if usr_input == 'abort':
                    abort()
            split_line = data['version'].strip().split(".")
            stable, beta, alfa = int(split_line[0].replace('V', '')), int(split_line[1]), int(split_line[2])
            if usr_input == 'a':
                if alfa < alfa_max:
                    alfa += 1
                else:
                    alfa = 0
                    usr_input = 'b'
            if usr_input == 'b':
                if beta < beta_max:
                    beta += 1
                    alfa = 0
                else:
                    beta = 0
                    usr_input = 's'
            if usr_input == 's':
                if stable < stable_max:
                    stable += 1
                    alfa, beta = 0, 0
                else:
                    print("Reached maximal version!")
                    stable, beta, alfa = 0, 0, 0
        version_data = open("version_status", "w")
        version_data.write(f"version#V{stable:1n}.{beta:02n}.{alfa:003n}\n")
        now = datetime.now()
        version_data.write("release_date#{}/{}/{}".format(now.strftime("%d"),
                                                          now.strftime("%m"), now.strftime("%Y")))
        version_data.close()
