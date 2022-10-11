from os import listdir, abort
from re import match
from version_supervisor import DataLogger

dl = DataLogger(__name__, 'logs')


class LangSupport:
    def __init__(self, directory=None):
        if directory is None:
            exit(3)
        super().__init__()
        self.name = self.__class__.__name__
        self.lang_list = []
        self.language = "EN_us"  # default language
        self.dictionary = {}  # language dictionary
        self.directory = directory

        self.get_languages()  # initialise available languages
        self.set_language(self.language)

    def get_languages(self):
        files = None
        try:
            files = listdir(self.directory)
        except FileNotFoundError:
            dl.log(f"Fatal error! Directory {self.directory} does not exist")
            exit(3)
        self.lang_list = []
        for Lang in files:
            if match('[A-Z]{2}_[a-z]{2}', str(Lang)) is not None:  # add only files in name format 'XX_yy'
                self.lang_list.append(Lang)
        if self.language not in self.lang_list:
            self.language = self.lang_list[0]  # selects any available language if primary language is unreachable
        return self.lang_list

    def set_language(self, lang):
        if len(self.lang_list):
            if lang not in self.lang_list:
                self.language = self.lang_list[0]  # selects any available language if selected language is unreachable
                dl.log(f"Warning! {lang} language not found.")
            else:
                self.language = lang
        else:
            dl.log(f"Fatal error! Languages not indexed!")
            exit(3)
        try:
            with open(f"{self.directory}\{self.language}", "r", encoding="utf-8") as lang_data:
                self.dictionary = {}
                for line in lang_data:
                    if not line.startswith(".."):  # double-dotted lines are not interpreted comment lines
                        split_line = line.strip().split("#", 1)  # separate parameters from values
                        # and remove escaping
                        self.dictionary[split_line[0]] = split_line[1]  # enter values by keys into dictionary
        except FileNotFoundError:
            dl.log(f"Fatal error! File not found!")
            exit(3)
        finally:
            lang_data.close()

    def get_text(self, dict_key, *args):
        text = None
        try:
            text = str(self.dictionary[dict_key])  # get text value based on key
        except KeyError:
            if len(self.dictionary):
                dl.log(f"Fatal error! {dict_key} key not found in {self.language} language file.")
            else:
                dl.log(f"Fatal error! Language: {self.language} not loaded!")
            exit(3)
        try:
            text = text.format(*args)   # try to format text with arguments, if any specified
        except IndexError:
            pass
        return text


if __name__ == "__main__":
    dl.log("Fatal error! This file could not be ran standalone")
    exit(3)

# example usage
# l = LangSupport()
# print(l.get_languages())
# print(l.dictionary)
# print(l.get_text('siminfo2').format("Alfa 0.0"))
