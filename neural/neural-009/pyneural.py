#!/usr/bin/env python 

# ------------------------------------------------------------------------
# Neural network test

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, math

import neunet, trans, neuron, lattice

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

# Print an array of floats. Print sign and 3 digits for uniform print
def printarr(arr):
    for aa in arr:
        print "%+0.3f" % aa,
    print 

def test_formula():
    mw = MainWin()
    cnt = 0.
    for aa in xrange(-390, 390):
        val2 = 0.
        val1 =  float(aa) / 100 
        try:
            val2 = math.gamma(val1)
        except:
            print "error at %f" % val1
            
        mw.coords.append((cnt,  val1,  1))
        mw.coords2.append((cnt, val2, 1))
        cnt += 1
        if cnt % 10 == 0:
            print "%+0.3f=%+0.3f     " % (val1, val2),
    gtk.main()
    
# ------------------------------------------------------------------------

def test_tfunc():

    mw = MainWin()
    cnt = 0.
    for aa in xrange(-190, 190):
        val =  float(aa) / 100 
        val1 = trans.tfunc(val)
        val2 = trans.tfunc2(val)
        val3 = trans.tfunc3(val)
        mw.coords.append((cnt , val1,  1))
        mw.coords2.append((cnt , val2, 1))
        mw.coords3.append((cnt , val3,  1))
        cnt += 1
        if cnt % 10 == 0:
            print "%+0.3f=%+0.3f/%+0.3f     " % (val, val2, val3),
    gtk.main()
    
def distance(arr1, arr2):
    if len(arr1) != len(arr2):   
        raise exceptions.ValueError("Arrays must be the same size")
        
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
    print "            -g        - gui"
    print "            -m        - Dump network"
    print "            -x        - eXtra test"
    print "            -f        - Formula test"
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
    ["f",   "formula",  0,      None],      \
    ["g",   "gui",      0,      None],      \
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

    if conf.formula:
        print "\nTesting formula:\n"
        test_formula(); 
        sys.exit()

    # Verbosa and debug levels    
    neuron.verbose = conf.verbose;  neuron.pgdebug = conf.pgdebug
    
    # Spec of the network to create. Layer spec is read from output to input. 
    # Layer definition:  in, neurons, outputs, ...
    #neumap = ((8,8,8), (8,8,8), (1,8,8))
    neumap = ((8,16,16), (1,8,8))
    #neumap = ((1,8,8),)
    neu = neunet.neunet(neumap)
    neu.verbose = conf.verbose
    neu.fire()
    #neu.dump()
    
    '''lat = lattice.lattice(2, 2)
    lat.verbose = conf.verbose
    lat.dump()
    lat.fire()
    lat.dump()'''
    
    #sys.exit()
    
    if conf.dump:
        print "\nDumping neural net:\n"
        neu.dump()
        sys.exit()
    
    if conf.xtra:
        arr1 = []; arr2 = []
        neu.setinput((0.10,0.10,0.10,0.10,0.10,0.10,0.10,0.10))
        print "in1:", ;neu.showin()
        neu.fire(); 
        arr1 = neu.getout()
        
        neu.setinput((0.10,0.10,0.30,0.10,0.10,0.10,0.10,0.10))
        print "in2:", ; neu.showin()
        neu.fire(); 
        arr2 = neu.getout()
        
        print "out1", ;   printarr(arr1)
        print "out2", ;   printarr(arr2)
        
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
    for aa in range(5):
        neu.setinput(value_a)
        cnt += neu.trainone(expect_a)
        printarr(expect_a) ; neu.showout()
    
        neu.setinput(value_b)
        cnt += neu.trainone(expect_b)
        printarr(expect_b) ; neu.showout()
    
        neu.setinput(value_c)
        cnt += neu.trainone(expect_c)
        printarr(expect_c) ; neu.showout()
        
    print "count:", cnt
    
    print "value  a ", ;  printarr(value_a)
    print "value  b ", ;  printarr(value_b)
    print "value  c ", ;  printarr(value_c)
    print
    
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
    print "actual a ", ;  neu.showout()
    arr1 = neu.getout()
    
    neu.setinput(value_b)
    #neu.showin()
    neu.fire()
    print "actual b ",  ; neu.showout()
    arr2 = neu.getout()
    
    neu.setinput(value_c)
    #neu.showin()
    neu.fire()
    print "actual c ", ;  neu.showout()
    arr3 = neu.getout()

    print
    print "Diff a-a = %0.3f     b-b = %0.3f     c-c = %0.3f " % \
        (distance(expect_a, arr1), distance(expect_b, arr2), distance(expect_c, arr3))
    #neu.dump()
    
    if not conf.gui:
       sys.exit(0)
    
    mw = MainWin()
    gtk.main()
    sys.exit(0)























