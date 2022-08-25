from os import listdir, abort
from re import match


class LangSupport:
    def __init__(self):
        super().__init__()
        self.lang_list = []
        self.language = "EN_us"  # default language
        self.dictionary = {}  # language dictionary

        self.get_languages()  # initialise available languages
        self.set_language(self.language)

    def get_languages(self):
        files = listdir("Languages")
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
                print(f"Warning! {lang} language not found.")
            else:
                self.language = lang
        else:
            print("Fatal error! Languages not indexed!")
            abort()
        try:
            with open(f"Languages\{self.language}", "r", encoding="utf-8") as lang_data:
                self.dictionary = {}
                for line in lang_data:
                    if not line.startswith(".."):  # double-dotted lines are not interpreted comment lines
                        split_line = line.strip().split("#", 1)  # separate parameters from values
                        # and remove escaping
                        self.dictionary[split_line[0]] = split_line[1]  # enter values by keys into dictionary
        except FileNotFoundError:
            print("Fatal error! File not found!")
            abort()
        finally:
            lang_data.close()

    def get_text(self, dict_key):
        text = ""
        if len(self.dictionary):  # specify if any language is loaded into dictionary
            if dict_key in self.dictionary:
                return str(self.dictionary[dict_key])  # return text value based on key value
            else:
                print(f"Fatal error! {dict_key} key not found in {self.language} language file.")
                abort()  # abort or not? // add missing parameters tracker //
        else:
            print(f"Fatal error! Language: {self.language} not loaded!")
            abort()


if __name__ == "__main__":
    print("Fatal error! This file could not be ran standalone")
    abort()

# example usage
# l = LangSupport()
# print(l.get_languages())
# print(l.dictionary)
# print(l.get_text('siminfo2').format("Alfa 0.0"))
