import sys
import os

rootDirectory = os.path.abspath(os.curdir)
SETUP_DIR = sys.path.append(rootDirectory + "/sourcecode")

from setup import setup

def setupNeedleMan():
    setup()


