import os
import re
import sys
import json
from pathlib import Path
from FileSystemUtils import FSUtils

class CodeAnalyser:
    SETTINGS_FILE = os.path.join(os.path.dirname(Path(__file__).absolute()),"config.json")
    __CURRENT_MODE = [] 
    __LOG_MODE = "debug"

    __MODES_BY_FILETYPE_CACHE = {}
    __ERRORS = []

    def __init__(self) -> None:
        self.settings = json.load(open(self.SETTINGS_FILE, "r"))

    def support_exists(self, ftype) -> bool:
        return ftype in self.settings

    def set_log_mode(self, mode):
        if mode in ["quiet", "info", "debug"]:
           self.__LOG_MODE = mode 

    def add_mode(self, ftype) -> None:
        self.__CURRENT_MODE.append(ftype)


    def __detect_mode(self, extension):
        for mode in self.__CURRENT_MODE:
            # first check if available in cache
            if extension in self.__MODES_BY_FILETYPE_CACHE:
                return self.__MODES_BY_FILETYPE_CACHE[extension]

            if mode in self.settings and "extensions" in self.settings[mode] and extension in self.settings[mode]["extensions"]:
                self.__MODES_BY_FILETYPE_CACHE[extension] = mode
                return mode

        return None
            
    def extract_routine(self, line, pattern):
        match = re.search(pattern, line)
        if match:
            return match.group(1)
        return None
        
    def display_results(self, results:dict):
        for file in results:
            print("📄" + file)

            counter = 1

            for routine in results[file]:
                print(f"\t {counter}) ", routine)
                counter += 1
            print("\n")
        
        if (len(self.__ERRORS) > 0):
            print(f"UNABLE TO READ {len(self.__ERRORS)} files due to errors")
            for error in self.__ERRORS:
                print(error)

    def multi_file_analyze(self, files: list):
        results = {}

        for filepath in files:
            chopped_paths = filepath.split(".")

            # if there was no extension on file then skip
            if len(chopped_paths) < 2:
                continue

            # Now extract the extension and check if it matches the current mode, if not then skip
            extension = chopped_paths[-1]

            mode = self.__detect_mode(extension)

            # if does not matches any known modes then skip
            if (mode == None) or (mode not in self.settings) or ("routine" not in self.settings[mode]) or (self.settings[mode]["routine"] == None):
                continue
                
            routines_in_file = self.analyze(filepath, self.settings[mode]["routine"])

            if (len(routines_in_file) > 0):
                # if routines exists in file then add them to result
                results[filepath] = routines_in_file

        return results


    def analyze(self, filename: str, pattern: str) -> list:

        routines = []
        fp = None
        encodings = [None, 'utf-8', 'latin-1', 'iso-8859-1']

        for enc in encodings:
            try:
                if (enc):
                    fp = open(filename, "r", encoding=enc)
                else:
                    fp = open(filename, "r")

                while ((line := fp.readline()) != ""):
                    line = line.strip()
                    match = self.extract_routine(line, pattern)

                    if match != None:
                        routines.append(match)
                break

            except Exception as e:
                if (self.__LOG_MODE == "debug"):
                    print(e.with_traceback())
                    print("\n\n")

                if (self.__LOG_MODE in ["info", "debug"]):
                    print("Error while reading ", filename)
                    print("retrying with a different encoding")
                    print("\n\n")

                self.__ERRORS.append(filename)

            finally:
                fp.close()

        return routines


if __name__ == "__main__":
    mode = sys.argv[1] 
    directory_path = sys.argv[2] 

    analyser = CodeAnalyser()
    analyser.set_log_mode("quiet")

    if not analyser.support_exists(mode):
        print("Support not exists for the mode")
        sys.exit(1)

    analyser.add_mode(mode)

    fullpath_files = FSUtils.get_all_files_recursively(directory_path)

    results = analyser.multi_file_analyze(files=fullpath_files)
    analyser.display_results(results)