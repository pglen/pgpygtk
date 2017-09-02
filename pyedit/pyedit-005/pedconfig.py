#!/usr/bin/env python

# Global configuration for pyedit.
# Also a place we share globals to the rest of the files
# like the main window statusbar is acessable from the key handler
# or the key handler is acessable from the main window ... etc

import signal, os, time, sys
import keyhand
    
class pedconfig():  

    full_screen = False
    keyh = keyhand.KeyHand()
    pedwin = None
            
    def __init__(self): 
        pass

