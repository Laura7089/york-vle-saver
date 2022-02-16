#!/usr/bin/env python3
import argparse
import time

import toml
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from module_scraper.vle import VLEWrapper

parser = argparse.ArgumentParser(
    description="Download course content from the Yorkshare VLE and Panopto")
parser.add_argument("--config-file",
                    type=str,
                    help="Config file path",
                    default="./config.toml")

if __name__ == "__main__":
    args = parser.parse_args()

    app_options = toml.load(args.config_file)
    vle = VLEWrapper(webdriver.Firefox(options=FirefoxOptions()))
    vle.login(**app_options["vle"]["login"])
    for module in app_options["modules"]:
        vle.goto_module(module["name"])
        time.sleep(5)
