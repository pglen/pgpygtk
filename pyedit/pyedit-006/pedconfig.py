#!/usr/bin/env python

# Global configuration for pyedit.
# Also a place we share globals to the rest of the files
# like the main window statusbar is acessable from the key handler
# or the key handler is acessable from the main window ... etc

import signal, os, time, sys
import keyhand, acthand
    
class conf():  

    IDLE_TIMEOUT = 5            # Time for a new save
    SYNCIDLE_TIMEOUT = 2        # Time for syncing windows
    UNTITLED = "untitled.txt"   # New (empty) file name

    full_screen = False
    keyh = keyhand.KeyHand()
    pedwin = None

    # Count down variables
    idle = 0
    syncidle = 0                    
    statuscount = 0

    # Where things are stored (backups, orgs, macros)
    config_dir = os.path.expanduser("~/.pyedit")
    config_file = "defaults"

    # Where things are stored (UI x/y pane pos.)
    config_reg = "/apps/pyedit"
            
    def __init__(self): 
        pass

