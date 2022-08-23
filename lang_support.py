from os import listdir, abort
from re import match
# from contextlib import ExitStack


class LangSupport:
    def __init__(self):
        super().__init__()
        self.lang_list = []
        self.language = "EN_us"  # default language
        self.dictionary = {}     # language dictionary

        self.get_languages()     # initialise available languages
        self.set_language(self.language)

    def get_languages(self):
        files = listdir("Languages")
        self.lang_list = []
        for Lang in files:
            if match('[A-Z]{2}_[a-z]{2}', str(Lang)) is not None:   # add only files in name format 'XX_yy'
                self.lang_list.append(Lang)
        if self.language not in self.lang_list:
            self.language = self.lang_list[0]   # selects any available language if primary language is unreachable
        return self.lang_list

    def set_language(self, lang):
        if lang not in self.lang_list:
            if self.lang_list is not None:
                self.language = self.lang_list[0]   # selects any available language if selected language is unreachable
            else:
                print("Fatal error! Could not load any language!")
                abort()
        try:
            with open("Languages\{}".format(lang), "r") as lang_data:
                for line in lang_data:
                    if not line.startswith(".."):
                        split_line = line.strip().split("#", 1)
                        self.dictionary[split_line[0]] = split_line[1]
        except FileNotFoundError:
            print("Fatal error! File not found!")
            abort()
        finally:
            lang_data.close()

    def get_text(self, dict_key):
        text = ""
        if len(self.dictionary) > 0:
            try:
                text = str(self.dictionary[dict_key])
            except IndexError:
                print("Fatal error! {0} key not found in {1}".format(dict_key, self.language))
                abort()     # abort or not? // add missing parameters tracker //
            finally:
                return text
        else:
            print("Fatal error! LangSupport not initialised!")

    # created for debug purpose, it should check lang files for parameters existence
    """def validate_lang_files(self):
        if len(self.get_languages()) < 1:
            print("Fatal error! No files to validate!")
            return 3
        elif len(self.lang_list) == 1:
            print("Warning! One file found, could not validate due to impossibility of one file compare.")
            return 0
        else:
            files = []
            for lang in self.lang_list:
                file = [str(lang) + "_lang"]
                try:
                    with open("Languages\{}".format(lang), "r") as file :
                        files.append(file)
                except FileNotFoundError:
                    print("Fatal error! File not found!")
                    abort()
            for file in files:
                for line in file:
                    if not line.startswith(".."):
                        split_line = line.strip().split("#", 1)
                        files.remove(split_line[0])
                        for file_file in files:
                            found = False
                            for file_line in file_file:
                                if not line.startswith(".."):
                                    split_line1 = line.strip().split("#", 1)
                                    if split_line1[0] == split_line[0]:
                                        found = True
                            if not found:
                                print("{} not found in {}".format(split_line[0], str(file_file)))"""


if __name__ == "__main__":
    print("Fatal error! This file could not be ran standalone")
    abort()

# ezample usage
# l = LangSupport()
# print(l.get_languages())
# print(l.dictionary)
# print(l.get_text('siminfo2').format("Alfa 0.0"))
