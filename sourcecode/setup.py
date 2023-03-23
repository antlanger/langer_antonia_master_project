import sys
import os

def setup():
    rootDirectory = os.path.abspath(os.curdir)
    HELPERS_DIR = rootDirectory + "/sourcecode/helpers"
    WEBSCRAPER_DIR = rootDirectory + "/sourcecode/webscraper"
    NEEDLEMAN_WUNSCH_DIR = rootDirectory + "/sourcecode/needleman_wunsch"

    sys.path.append(HELPERS_DIR)
    sys.path.append(WEBSCRAPER_DIR)
    sys.path.append(NEEDLEMAN_WUNSCH_DIR)