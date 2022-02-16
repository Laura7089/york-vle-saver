import datetime
import logging
import os

from . import util


class Saver:

    def __init__(self, data):
        self.data = data
        self.logger = logging.getLogger("vle_getter.download")

    def save(self, module_name, target_name, source):
        # Create directories
        module_path = os.path.join(self.data, util.to_key(module_name))
        if not os.path.exists(module_path):
            self.logger.warn("Path '%s' does not exist, creating...",
                             module_path)
            os.mkdir(module_path)
        target_path = os.path.join(module_path, util.to_key(target_name))
        if not os.path.exists(target_path):
            self.logger.warn("Path '%s' does not exist, creating...",
                             target_path)
            os.mkdir(target_path)

        date = datetime.datetime.now().time()
        path = os.path.join(target_path, f"{date}.html")

        with open(path, "wt") as source_file:
            self.logger.debug("Writing to '%s'...", path)
            source_file.write(source)
