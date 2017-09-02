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

# Random in random out (with conveging on 0)

def test2(levels, neurons, inputs):

    cnt2 = 1
    levels = 3;   neurons = 4;  inputs = 4;
    
    sum = 0.0; count = 100
    for aaa in range(count):
        neu = neunet.neunet(levels, neurons, inputs)
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
    
    
    # Define neural network from front to back.  num inputs / num neurons
    netdef = ((1,8), (8, 8), (8, 1))
    
    #test2(levels, neurons, inputs)    
    sys.exit()
    
    levels = 3;  neurons = 1;  inputs = 8;
    print "Constructing net with:", levels, "levels", neurons,  "neurons", inputs, "inputs"
    neu = neunet.neunet(levels, neurons, inputs)
    neunet.verbose = conf.verbose
    
    neu.fire()
    neu.showout()
    
    neu.setinput(ord('a'))
    neu.fire()
    neu.showout()
    
    neu.setinput(ord('b'))
    neu.fire()
    neu.showout()

    '''for aa in range(10):
        neu.randtip()
        neu.fire()
        neu.showout()'''
        
    '''for aa in range(-20, 20):
       print float(aa) / 10, tfunc(float(aa) / 10)'''
        
    #neu.dump()
    
    if conf.nogui:
       sys.exit(0)
    
    gtk.main()
    sys.exit(0)



