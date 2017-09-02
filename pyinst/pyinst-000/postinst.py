#!/usr/bin/env python

import os, sys, getopt, signal, select, time 
import subprocess

verbose = False 

# ------------------------------------------------------------------------
def exec_program2(fname, arg1, arg2, arg3):
    global verbose
    
    try:
        if verbose:
            print "Started", fname
        
        pp = subprocess.Popen([fname, arg1, arg2, arg3])
        ret = os.waitpid(pp.pid, 0)
        if ret[1] != 0:
            print "Warninig: ", fname, "returned with", ret[1]
            
        if verbose:
            print "Ended ", fname
    except:
        print "Cannot execute script", fname, sys.exc_info()
        raise  
        return True

# ------------------------------------------------------------------------

if __name__ == '__main__':

    #print "In install.py"
    #time.sleep(1)
    pass

    # Create menus for your app. 
    # Edit entry.desktop to taste
    exec_program2("xdg-desktop-menu", "install", "--novendor", "entry.desktop")
