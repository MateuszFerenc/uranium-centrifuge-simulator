import sys
from os import system, abort
from re import match
from datetime import datetime

if __name__ == "__main__":
    if match(".py$", sys.argv[1]):
        system(sys.argv[1])
    else:
        print("No python file specified!")
        abort()

    usr_input = input("Does this version of project work? (if yes, automatically update project version")
    if usr_input.lower() in ("y", "yes", "yeah", "yep"):
        data = {}
        file_exists = False
        try:
            with open("version_status", "r") as version_data:
                file_exists = True
                for line in version_data:
                    split_line = line.strip().split("#", 1)
                    data[split_line[0]] = split_line[1]
        except FileNotFoundError:
            pass
        finally:
            version_data.close()
        if file_exists:
            pass
        version_data = open("version_status", "w")
        version_data.write("version#V0.00.000")
        version_data.write("release_date#00/00/00".format(datetime.strftime("%d"),
                                                          datetime.strftime("%m"), datetime.strftime("%Y")))
        version_data.close()
