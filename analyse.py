import os
import re
import sys
import json
import argparse
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
            return match.group(0)
        return None

    def _write_to_file(self, filename):
        """
        Creates a function that writes to the specified file.
        
        Args:
            filename (str): Path to the output file
        
        Returns:
            function: A function that writes a single line to the file
        """
        def write_line(line):
            with open(filename, 'a', encoding="utf-8") as f:
                f.write(str(line) + '\n')
        return write_line
        
    def display_results(self, results:dict, output_file=None):
        # Determine output method (console or file)
        output_func = print if output_file is None else self._write_to_file(output_file)
        
        for file in results:
            output_func("📄" + file)
            counter = 1
            for routine in results[file]:
                output_func(f"\t {counter}) {routine}")
                counter += 1
            output_func("\n")
        
        if (len(self.__ERRORS) > 0):
            output_func(f"UNABLE TO READ {len(self.__ERRORS)} files due to errors")
            for error in self.__ERRORS:
                output_func(error)


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
    # Use argparse for more robust command-line argument handling
    parser = argparse.ArgumentParser(description='Code Analyser')
    parser.add_argument('mode', help='Analysis mode')
    parser.add_argument('directory_path', help='Directory to analyze')
    parser.add_argument('-o', '--output', help='Output file path', default=None)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create analyser
    analyser = CodeAnalyser()
    analyser.set_log_mode("quiet")
    
    # Check mode support
    if not analyser.support_exists(args.mode):
        print("Support not exists for the mode")
        sys.exit(1)
    
    # Add mode and get files
    analyser.add_mode(args.mode)
    fullpath_files = FSUtils.get_all_files_recursively(args.directory_path)
    
    # Analyze files
    results = analyser.multi_file_analyze(files=fullpath_files)
    
    # Display results
    analyser.display_results(results, output_file=args.output)