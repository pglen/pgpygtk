#!/usr/bin/env python

# ------------------------------------------------------------------------
# Test client for the pyserv project. Initial user add.

import os, sys, getopt, signal, select, socket, time, struct
import random, stat

import pyserv.pydata, pyserv.pyservsup
from pyserv.pyclisup import *

# ------------------------------------------------------------------------
# Globals 

version = 1.0

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -p        - Port to use (default: 9999)"
    print "            -v        - Verbose"
    print "            -q        - Quiet"
    print "            -h        - Help"
    print
    sys.exit(0)

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

# ------------------------------------------------------------------------

if __name__ == '__main__':

    args = conf.comline(sys.argv[1:])
    
    pyserv.pyclisup.verbose = conf.verbose
    pyserv.pyclisup.pgdebug = conf.pgdebug

    if len(args) == 0:
        ip = '127.0.0.1' 
    else:
        ip = args[0]
    
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    init_handler(s1)

    try:
        s1.connect((ip, conf.port))
    except:
        print "Cannot connect to:", ip + ":" + str(conf.port), sys.exc_info()[1]
        sys.exit(1)

    client(s1, "ver")
    client(s1, "uini peter 1234")
    client(s1, "quit")
    s1.close();
    
    sys.exit(0)

















