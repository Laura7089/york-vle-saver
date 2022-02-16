#!/usr/bin/env python3
import argparse
import logging
import sys
from os import path

import toml
from selenium import webdriver

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
parser.add_argument(
    "-b",
    "--browser",
    help="The browser driver to use, see the selenium docs",
    choices=["firefox", "chrome", "ie", "edge", "safari"],
    default="firefox")
parser.add_argument("-l", "--log-level", choices=["debug", "info", "critical", "error", "warning"], default="warning", help="The logging level to use")

if __name__ == "__main__":
    args = parser.parse_args()
    logger = logging.getLogger("vle_getter")
    logger.setLevel(args.log_level.upper())

    # Try to load config file
    try:
        app_options = toml.load(args.config_file)
    except FileNotFoundError:
        logger.critical(f"""
Specified config file doesn't exist.
If you didn't give a config file argument, the script will look at '{DEFAULT_CONFIG}'.""")
        sys.exit(1)

    # Check data directory exists
    if not path.exists(app_options["paths"]["data"]):
        logger.critical("Data path '%s' does not exist", app_options["paths"]["data"])
        sys.exit(1)

    # Select a browser and setup selenium
    driver = None
    match args.browser:
        case "firefox":
            sel_options = webdriver.firefox.options.Options()
            sel_options.headless = args.headless
            driver = webdriver.Firefox(options=sel_options)
        case "chrome":
            sel_options = webdriver.chrome.options.Options()
            sel_options.headless = args.headless
            driver = webdriver.Chrome(options=sel_options)
        case "edge":
            sel_options = webdriver.edge.options.Options()
            sel_options.headless = args.headless
            driver = webdriver.Edge(options=sel_options)
        case "ie":
            sel_options = webdriver.ie.options.Options()
            sel_options.headless = args.headless
            driver = webdriver.Ie(options=sel_options)
        case "safari":
            sel_options = webdriver.safari.options.Options()
            sel_options.headless = args.headless
            driver = webdriver.Safari(options=sel_options)

    # Setup the VLE infra
    vle = VLEWrapper(driver)
    vle.login(**app_options["vle"]["login"])
    saver = Saver(app_options["paths"]["data"])

    # Get content
    for module in app_options["modules"]:
        for target in module["targets"]:
            logging.info("Getting page {} from {}...", target["name"], module["name"])
            try:
                vle.goto_module_sidebar_link(module["name"], target["name"])
            except ValueError:
                continue
            saver.save(module["name"], target["name"], vle.driver.page_source)
