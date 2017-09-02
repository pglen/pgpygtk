#!/usr/bin/env python

# ------------------------------------------------------------------------
# Python Alarm

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, subprocess

from pgutil import  *
from mainwin import  *

# ------------------------------------------------------------------------
# Globals 

version = "0.00"

# ------------------------------------------------------------------------
# Resolve path name

def respath(fname):
    ppp = string.split(os.environ['PATH'], os.pathsep)
    for aa in ppp:
        ttt = aa + os.sep + fname
        #print ttt
        if os.path.isfile(ttt):
            return ttt

def alarm(fname):
    ppp = respath("python")    
    threefile = "c" + fname[1:]
    try:
        os.rename(ala_dir + "/" + fname, ala_dir + "/" + threefile)
    except:
        print "Cannot rename alarm file"
        print sys.exc_info()
    try:
        # Pass full path, so the popup app does not need to know internals
        subprocess.Popen([ppp, "pyalapop.py", ala_dir + "/" + threefile])
    except:    
        print "Cannot execute alarm subprocess"
        print sys.exc_info()
    # Refresh
    gobject.timeout_add(interval, app_tick)

def app_tick():
    
    global interval, startx, ala_dir
    
    now = time.time()
    print "now", time.asctime(time.localtime(now))
    dirlist = os.listdir(ala_dir)
    ff = []
    for onefile in dirlist:
        # Filter alarm files
        if onefile[0] == "a":
            sss = os.lstat(ala_dir + "/" + onefile)
            if stat.S_ISREG(sss[stat.ST_MODE]):
                # Decode name:
                try:
                    ttt = (int(onefile[1:5]), int(onefile[5:7]), \
                        int(onefile[7:9]), int(onefile[9:11]), int(onefile[11:13]) \
                            , 0, -1, -1, -1)
                    tt = time.mktime(ttt)
                    
                    #print "asctime", time.asctime(time.localtime(tt))
                except:
                    print "Cannot convert time"    
                    print sys.exc_info()
                    continue
              
                if tt < now:
                    print "Warning: alarm file in past, removing", onefile
                    os.remove(ala_dir + "/" + onefile)
                    continue
                    
                twofile = "b" + onefile[1:]
                os.rename(ala_dir + "/" + onefile, ala_dir + "/" + twofile)
                delay = tt - now
                #print "ddd", delay
                gobject.timeout_add(int(delay * 1000), alarm, twofile)
                
# ------------------------------------------------------------------------

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -p        - Port to use (default: 9999)"
    print "            -v        - Verbose"
    print "            -V        - Version"
    print "            -q        - Quiet"
    print "            -h        - Help"
    print
    sys.exit(0)

# ------------------------------------------------------------------------
def pversion():
    print os.path.basename(sys.argv[0]), "Version", version
    sys.exit(0)
    
    # option, var_name, initial_val, function
optarr = \
    ["d:",  "pgdebug",  0,      None],      \
    ["p:",  "port",     9999,   None],      \
    ["v",   "verbose",  0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["t",   "test",     "x",    None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \
    
conf = Config(optarr)

if __name__ == '__main__':

    global mw, interval, startx, ala_dir

    ala_dir = os.path.expanduser("~/.pyala")
    interval = 1000
    startx = time.time()

    if not os.path.isdir(ala_dir):
        os.mkdir(ala_dir)

    if not os.path.isdir(ala_dir):
        print "Cannot access local storage"
        sys_exit(1)
        
    args = conf.comline(sys.argv[1:])
    mw = MainWin(); mw.app_tick = app_tick; mw.ala_dir = ala_dir
    gobject.timeout_add(interval, app_tick)
 
    gtk.main()
    sys.exit(0)















