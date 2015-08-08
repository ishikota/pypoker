"""

    To run this script, you need to add root path of this project
    to your PYTHONPATH.

    If you put this root project to /Users/YourName/poker 
    then run below two command on your terminal.

    PYTHONPATH=/Users/YourName/poker:$PYTHONPATH
    export PYTHONPATH

"""
import sys, os, subprocess
import user_interface
from engine.ui.table import Table
from engine.ui.config import Config

# Display logo
subprocess.call('clear')
user_interface.logo()

# read game config
C = Config()
path_to_config = os.path.abspath(__file__)[:-len("main.py")]
C.read(path_to_config+"config.txt")

# set up the game
p = C.getPlayers()
t = Table()
t.setup(p, C.getSBChip())
t.AUTO = C.getIfAuto()

# start the game !!
t.start_game(C.getRoundNum())
