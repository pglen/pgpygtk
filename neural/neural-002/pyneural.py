#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, math

import neunet
from pgutil import  *
from mainwin import  *

# ------------------------------------------------------------------------
# Globals

version     = "0.00"

# Test for random in random out (with conveging on 0)

def test2(levels, neurons, inputs):

    cnt2 = 1; levels = 3;  neurons = 4
    sum = 0.0; count = 100
    for aaa in range(count):
        neu = neunet.neunet(levels, neurons)
        neu.fire()
        arr = neu.levarr[len(neu.levarr) - 1]
        for aa in arr.membarr:
            '''print "%+0.3f\t" % aa.output,
            if cnt2 % 9 == 0:
                print'''
            cnt2 += 1
            sum += aa.output
    #print
    print "Sum", sum / count

# ------------------------------------------------------------------------

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -v        - Verbose"
    print "            -n        - Nogui"
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
    ["v",   "verbose",  0,      None],      \
    ["n",   "nogui",    0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["t",   "test",     "x",    None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \

        
conf = Config(optarr)

if __name__ == '__main__':

    global mw, verbose
    
    args = conf.comline(sys.argv[1:])
    
    mw = MainWin()
    
    levels = 3;  neurons = 8
    print "Constructing net with:", levels, "levels", neurons,  "neurons"
    neu = neunet.neunet(levels, neurons)
    neunet.verbose = conf.verbose
    
    neu.showin()
    cnt = 0
    for aa in range(10):
        neu.setinput(ord('a'))
        expect1 = (.5, .5, .5, .5, .5, .5, .5, .5)
        cnt += neu.trainone(expect1)
       
        neu.setinput(ord('z'))
        expect2 = (.1, .2, .3, .4, .5, .6, .7, .8)
        cnt += neu.trainone(expect2)
        
    print "count:", cnt,
        
    # Test the two trained values:
    print "expect 1", 
    for aa in expect1: print "%+0.3f" % aa, 
    print
    
    print "expect 2", 
    for aa in expect2: print "%+0.3f" % aa, 
    print
    
    neu.setinput(ord('a'))
    neu.fire()
    print "final  a ", neu.showout()
    
    neu.setinput(ord('z'))
    neu.fire()
    print "final  z ", neu.showout()
    
    #for aa in range(-20, 20):
    #   print float(aa) / 10, neunet.tfunc(float(aa) / 10)
        
    #neu.dump()
    
    if conf.nogui:
       sys.exit(0)
    
    gtk.main()
    sys.exit(0)








