#!/usr/bin/env python

# ------------------------------------------------------------------------
# Voice recognition

import os, sys, getopt, signal, select, socket, time, struct
import random, stat

from vrutil import  *
from mainwin import  *
from pyrand import  *

# ------------------------------------------------------------------------
# Globals 

version = "0.01"

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

# Generate a random color string 

def randcolstr():
    col = "#%02x%02x%02x" % \
                (random.random() * 0xff, \
                    random.random() * 0xff, \
                        random.random() * 0xff)
    return col

# Globals
                                
ttt = time.clock()

# ------------------------------------------------------------------------
# Work is done here:

def app_tick():

    global mw, cnt2, ttt, ttt3
    ttt3 = 0; cnt2 = 0; cnt = 10; xx = 0
    while 1:
        try:
            ww, hh = mw.plot.window.get_size()
            #mw.plot.plotcolor(randcolstr())
            for aa in range(cnt):
                #yy = int(random.random() * hh)
                yy = math.sin(math.radians(xx)) * hh / 3 + hh/2
                mw.plot.plotline2(yy)
                xx += 1
                
                '''mw.plot.plotpoint(int(random.random() * ww), \
                            int(random.random() * hh))'''
                '''mw.plot.plotpoint(int(rrr.rand() * ww), \
                            int(rrr.rand() * hh))'''
                '''mw.plot.plotline(   int(random.random() * ww),  \
                                    int(random.random() * hh),  \
                                    int(random.random() * ww),  \
                                    int(random.random() * hh)) '''
                '''self.plotcirc(  int(random.random() * ww),  \
                                int(random.random() * hh),  \
                                int(random.random() * ww/3),  \
                                int(random.random() * hh/3), True)'''
                '''self.plotrect(  int(random.random() * ww),  \
                                int(random.random() * hh),  \
                                int(random.random() * ww/3),  \
                                int(random.random() * hh/3), True)'''
            cnt2 += cnt            
            if vrutil.usleep(1):
                break
                
        except: 
            vrutil.print_exception("app_tick")
            break
        
        ttt2 = time.clock() - ttt
        if int(ttt2) != int(ttt3):
            mw.prog.set_text("%d ops/sec" % (cnt2 / ttt2) )
            ttt3 = ttt2
        
        #print "\b\b\b\b\b\b\b\b\b\b\b\b\b\b", cnt2 / ttt2, "ops/sec",     
        #sys.stdout.flush()
        #break
    #gobject.timeout_add(0, app_tick)

if __name__ == '__main__':

    global mw
    
    args = conf.comline(sys.argv[1:])
    mw = MainWin()
    gobject.timeout_add(100, app_tick)
    gtk.main()
    sys.exit(0)













