import os


class FSUtils:
    @staticmethod
    def get_all_files_recursively(sdir) -> list:
        found = []

        for subdir, dirs, files in os.walk(sdir):
            for file in files:
               found.append(os.path.join(subdir, file))

        return found 