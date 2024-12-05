import os


class FSUtils:
    @staticmethod
    def get_all_files_recursively(sdir) -> list:
        files = []

        for subdir, dirs, files in os.walk(sdir):
            for file in files:
               files.append(os.path.join(subdir, file))

        return files