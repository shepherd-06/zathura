import os
import sys
from datetime import datetime
from .utility import Utility
from git import Repo

def create_app():
    debug = True  #  TODO: for testing purpose only.
    # It should be hardcode False on production
    known_commands = ('v',)
    if len(sys.argv) > 1:
        if debug:
            # DO THIS IN DEBUG MODE
            pass
        if 'v' in sys.argv:
            repo = Repo(os.getcwd())
            if repo.tags is not None:
                tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
                print(tags[-1])
            else:
                print("ERROR! version name not found.")
        else:
            print("unknown command")