import datetime
import os

from . import util


class Saver:

    def __init__(self, data, paths):
        for (path_type, path) in paths.items():
            self.data = data
            self.paths = paths

    def save(self, module_name, target_name, source):
        # Create directories
        module_path = os.path.join(self.data, util.to_key(module_name))
        if not os.path.exists(module_path):
            os.mkdir(module_path)
        target_path = os.path.join(module_path, util.to_key(module_name))
        if not os.path.exists(target_path):
            os.mkdir(target_path)

        date = datetime.datetime.now().time()
        path = os.path.join(target_path, f"{date}.html")

        with open(path, "wt") as source_file:
            source_file.write(source)
