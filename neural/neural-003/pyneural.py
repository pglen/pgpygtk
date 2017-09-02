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

def test3():
    for aa in range(-40, 41):
       val =  float(aa) / 20
       print "%+0.3f=%+0.3f  " % (val, neunet.tfunc(val)),
    
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
    ["m",   "dump",     0,      None],      \
    ["v",   "verbose",  0,      None],      \
    ["n",   "nogui",    0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["t",   "test",     0,      None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \
        
conf = Config(optarr)

if __name__ == '__main__':

    global mw, verbose
    
    args = conf.comline(sys.argv[1:])
    if args == ():
        sys.exit(2)
    
    if conf.test:
        print "\nTesting trans function:\n"
        test3(); 
        sys.exit()
    
    levels = 3
    print "Constructing net with:", levels, "levels"
    neu = neunet.neunet(levels)
    neunet.verbose = conf.verbose
    
    if conf.dump:
        print "\nDumping neural net:\n"
        neu.dump()
        sys.exit()
    
    '''#neu.dump()
    neu.showin()
    neu.fire()
    neu.showout()
    neu.setinput(ord('a'))
    neu.showin()
    neu.fire()
    neu.showout()
    #neu.dump()
    sys.exit()
    neu.showin()'''
    
    expect1 = .1; expect2 = .5; cnt = 0
    
    for aa in range(3):
        neu.setinput(0x10)
        cnt += neu.trainone(expect1)
        print expect1, ; neu.showout()
    
        neu.setinput(0x1000)
        cnt += neu.trainone(expect2)
        print expect2, ; neu.showout()
        
    print "count:", cnt
        
    # Test the two trained values:
    print "expect 1 ", 
    print "%+0.3f" % expect1 
    
    print "expect 2 ", 
    print "%+0.3f" % expect2
    
    neu.setinput(ord('a'))
    neu.fire()
    print "final  a ",
    neu.showout()
    
    neu.setinput(ord('z'))
    neu.fire()
    print "final  z ",
    neu.showout()
    
    #neu.dump()
    
    if conf.nogui:
       sys.exit(0)
    
    mw = MainWin()
    gtk.main()
    sys.exit(0)




