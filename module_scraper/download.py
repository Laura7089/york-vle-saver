import datetime
import os


class Saver:

    def __init__(self, data, paths):
        for (path_type, path) in paths.items():
            self.data = data
            self.paths = paths

    def save(self, module_name, path_type, source):
        module_path = os.path.join(self.data, module_name.lower())
        if not os.path.exists(module_path):
            os.mkdir(module_path)

        date = datetime.datetime.now().time()
        path = os.path.join(
            module_path, self.paths[path_type].format(date=date,
                                                      module=module_name))
        with open(path, "wt") as source_file:
            source_file.write(source)
