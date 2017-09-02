#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, math

import neunet, trans

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

def test_tfunc():

    mw = MainWin()
    cnt = 0.
    for aa in xrange(-100, 100):
        val =  float(aa) / 100 
        val2 = trans.tfunc(val)
        val3 = trans.tfunc3(val)
        mw.coords.append((cnt , val3,  1))
        mw.coords2.append((cnt , val2, 1))
        mw.coords3.append((cnt , val,  1))
        cnt += 1
        if cnt % 10 == 0:
            print "%+0.3f=%+0.3f/%+0.3f     " % (val, val2, val3),
    gtk.main()
    
# ------------------------------------------------------------------------

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -v        - Verbose"
    print "            -n        - Nogui"
    print "            -m        - Dump network"
    print "            -x        - eXtra test"
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
    ["x",   "xtra",     0,      None],      \
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
        test_tfunc(); 
        sys.exit()
    
    levels = 3; neurons = 3; inputs = 3
    print "Constructing net with:", levels, "levels", "inputs", inputs
    neu = neunet.neunet(levels, neurons, inputs)
    #neu.verbose = conf.verbose
    neu.fire()
    
    if conf.dump:
        print "\nDumping neural net:\n"
        neu.dump()
        #neu.showin()
        #neu.showout()
        sys.exit()
    
    if conf.xtra:
        neu.setinput(0x1)
        #print "in"; neu.showin()
        neu.fire(); print "out";   neu.showout()
        neu.setinput(0x10)
        #print "in"; neu.showin()
        neu.fire(); print "out";   neu.showout()
        sys.exit()
    
    expect_a = (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, ); 
    expect_b = (1.0, 0.0, 0.8, 0.0, 0.0, 1.0, 0.0, 0.0, ); 
    expect_z = (0.0, 0.1, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, ); 
    
    val_a = (0x1, 0x0, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9)
    val_b = (0x6, 0x2, 0x3, 0x0, 0x5, 0x6, 0x7, 0x8, 0x9)
    val_c = (0x1, 0x2, 0x0, 0x4, 0x5, 0x6, 0x7, 0x0, 0x9)
    
    cnt = 0
    
    for aa in range(3):
        neu.setinput(val_a)
        cnt += neu.trainone(expect_a)
        print expect_a, ; neu.showout()
    
        neu.setinput(val_b)
        cnt += neu.trainone(expect_b)
        print expect_b, ; neu.showout()
    
        neu.setinput(val_c)
        cnt += neu.trainone(expect_z)
        print expect_z, ; neu.showout()
        
    print "count:", cnt
        
    # Test the two trained values:
    print "expect a ", 
    for aa in expect_a:
        print "%+0.3f" % aa,
    print  
    
    print "expect b ", 
    for aa in expect_b:
        print "%+0.3f" % aa,
    print
    
    print "expect z ", 
    for aa in expect_z:
        print "%+0.3f" % aa,
    print
    
    neu.setinput(val_a)
    neu.showin()
    neu.fire()
    print "final  a ",
    neu.showout()
    
    neu.setinput(val_b)
    neu.showin()
    neu.fire()
    print "final  b ",
    neu.showout()
    
    neu.setinput(val_c)
    neu.showin()
    neu.fire()
    print "final  c ",
    neu.showout()
    
    #neu.dump()
    
    if conf.nogui:
       sys.exit(0)
    
    mw = MainWin()
    gtk.main()
    sys.exit(0)












