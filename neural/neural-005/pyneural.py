#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, math

import neunet, trans, neuron

from pgutil import  *
from mainwin import  *

# ------------------------------------------------------------------------
# Globals

version     = "0.00"

# Test for random in random out (with conveging on 0)

def test2(levels, neurons, inputs):

    cnt2 = 1; levels = 3;  neurons = 4; inputs = 2
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

def test_tfunc():

    mw = MainWin()
    cnt = 0.
    for aa in xrange(-190, 190):
        val =  float(aa) / 100 
        val1 = trans.tfunc(val)
        val2 = trans.tfunc2(val)
        val3 = trans.tfunc3(val)
        mw.coords.append((cnt , val3,  1))
        mw.coords2.append((cnt , val2, 1))
        mw.coords3.append((cnt , val1,  1))
        cnt += 1
        if cnt % 10 == 0:
            print "%+0.3f=%+0.3f/%+0.3f     " % (val, val2, val3),
    gtk.main()
    
def distance(arr1, arr2):
    if len(arr1) != len(arr2):   
        raise ValuError
        
    diff = 0.0      
    for aa in range(len(arr1)):        
        diff += abs(arr1[aa] - arr2[aa])
    return diff   
        

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
    
    '''print conf.__dict__
    if "pgdebug" in conf.__dict__:
        print "config", conf.pgdebug
    else:
        print "no config"'''
        
    if conf.pgdebug > 0:
        print "Debug level is:", conf.pgdebug
          
    if conf.test:
        print "\nTesting trans function:\n"
        test_tfunc(); 
        sys.exit()

    # Verbosa and debug levels    
    neuron.verbose = conf.verbose;  neuron.pgdebug = conf.pgdebug
    neunet.verbose = conf.verbose;  neunet.pgdebug = conf.pgdebug
    
    # Spec of the network to create from out to in. Layer definition:  in,neu,out, ...
    #neumap = ((8,8,8), (8,8,8),(8,8,8),(8,8,8),(8,8,8), (1,8,8))
    #neumap = ((8,8,8), (8,8,8), (8,8,8), (1,8,8))
    neumap = ((1,8,8),)
    neu = neunet.neunet(neumap)
    neu.verbose = conf.verbose
    #neu.fire()
    
    if conf.dump:
        print "\nDumping neural net:\n"
        neu.dump()
        sys.exit()
    
    if conf.xtra:
        arr1 = []; arr2 = []
        neu.setinput((0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10))
        print "in:", ;neu.showin()
        neu.fire(); print "out", ;   neu.showout()
        arr1 = neu.getout()
        
        neu.setinput((0.10,0.10,0.30,0.10,0.10,0.10,0.10,0.10))
        print "in:", ; neu.showin()
        neu.fire(); print "out", ;   neu.showout()
        arr2 = neu.getout()
        dd = distance(arr1, arr2)
        print "Distance", dd
        sys.exit()
    
    value_a = (0.1, 0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, )
    value_b = (0.6, 0.2, 0.3, 0.0, 0.5, 0.6, 0.7, 0.8, )
    value_c = (0.1, 0.2, 0.0, 0.4, 0.5, 0.6, 0.7, 0.0, )
    
    expect_a = (0.8, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, ); 
    expect_b = (0.8, 0.0, 0.8, 0.0, 0.0, 0.6, 0.0, 0.0, ); 
    expect_c = (0.0, 0.1, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, ); 
    
    cnt = 0
    for aa in range(3):
        neu.setinput(value_a)
        cnt += neu.trainone(expect_a)
        print expect_a, ; neu.showout()
    
        neu.setinput(value_b)
        cnt += neu.trainone(expect_b)
        print expect_b, ; neu.showout()
    
        neu.setinput(value_c)
        cnt += neu.trainone(expect_c)
        print expect_c, ; neu.showout()
        
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
    
    print "expect c ", 
    for aa in expect_c:
        print "%+0.3f" % aa,
    print
    
    neu.setinput(value_a)
    #neu.showin()
    neu.fire()
    print "final  a ",
    neu.showout()
    arr1 = neu.getout()
    
    neu.setinput(value_b)
    #neu.showin()
    neu.fire()
    print "final  b ",
    neu.showout()
    arr2 = neu.getout()
    
    neu.setinput(value_c)
    #neu.showin()
    neu.fire()
    print "final  c ",
    neu.showout()
    arr3 = neu.getout()

    print "Diff 1-1 = %0.3f     2-2 = %0.3f     3-3 = %0.3f " % \
        (distance(expect_a, arr1), distance(expect_b, arr2), distance(expect_c, arr3))
    #neu.dump()
    
    if conf.nogui:
       sys.exit(0)
    
    mw = MainWin()
    gtk.main()
    sys.exit(0)
















