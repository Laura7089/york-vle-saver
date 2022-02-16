#!/usr/bin/env python3
import argparse
import sys
from os import path

import toml
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from module_scraper.download import Saver
from module_scraper.vle import VLEWrapper

DEFAULT_CONFIG = "./config.toml"

parser = argparse.ArgumentParser(
    description="Download course content from the Yorkshare VLE and Panopto")
parser.add_argument("-c",
                    "--config-file",
                    type=str,
                    help="Config file path; see upstream for an example",
                    default=DEFAULT_CONFIG)
parser.add_argument("-H",
                    "--headless",
                    action="store_true",
                    help="Use headless mode")

if __name__ == "__main__":
    args = parser.parse_args()

    # Try to load config file
    try:
        app_options = toml.load(args.config_file)
    except FileNotFoundError:
        error = f"""
Specified config file doesn't exist.
If you didn't give a config file argument, the script will look at '{DEFAULT_CONFIG}'."""
        print(error)
        sys.exit(1)

    # Check data directory exists
    if not path.exists(app_options["paths"]["data"]):
        print("The data path specified does not exist")
        sys.exit(1)

    # Setup selenium
    sel_options = FirefoxOptions()
    sel_options.headless = args.headless
    vle = VLEWrapper(webdriver.Firefox(options=sel_options))

    vle.login(**app_options["vle"]["login"])

    saver = Saver(app_options["paths"]["data"], app_options["paths"])
    for module in app_options["modules"]:
        vle.goto_module(module["name"])
        saver.save(module["name"], "announcements", vle.driver.page_source)
