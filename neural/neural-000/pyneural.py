#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, getopt, signal, select, socket, time, struct
import random, stat

from pgutil import  *
from mainwin import  *

# ------------------------------------------------------------------------
# Globals

version     = "0.00"
verbose     = 0

gl_level    = 0
gl_num      = 0
gl_serial   = 0

# Deliver a -1 +1 random number

def rand():

    return random.random() * 2 -1;

# ------------------------------------------------------------------------
# Basic building block:

class tenticle():

    def __init__(self):

        self.input   = rand()
        self.weight  = rand()
        self.bias    = rand()

    # Calculate output
    def fire(self):
        res = self.input * self.weight + self.bias
        return max(min(res, 1), -1)

    def getstr(self):
        return " [%0.3f" % self.input, "%0.3f" % self.weight, "%0.3f] " % self.bias,

class neuron():

    def __init__(self, inputs):

        global gl_num, gl_level, gl_serial
        #print "neron init"
        self.transfer = "";
        self.output = 0.0

        # These are helpers
        self.num = gl_num; self.serial = gl_serial; self.level = gl_level
        gl_serial += 1; gl_num += 1

        self.tentarr = []
        for aa in range(inputs):
            self.tentarr.append(tenticle())

    def fire(self):
        sum = 0.0
        xlen = len(self.tentarr)
        for aa in range(xlen):
            sum += self.tentarr[aa].fire()
        self.output = sum / len(self.tentarr)
        #print "     ", self.level, self.num ,

        #for dd in self.tentarr:
        #    print " [%0.3f" % dd.input, "%0.3f" % dd.weight, "%0.3f] " % dd.bias,

        #print "Out: %0.3f" % self.output

# ------------------------------------------------------------------------
# One level:

class neunetlevel():

    def __init__(self, members, inputs):

        global gl_level, gl_num

        self.membarr = []
        for aa in range(members):
            self.membarr.append(neuron(inputs));

        self.level = gl_level
        gl_level += 1; gl_num = 0

    def fire(self):
        #print "firing level", self.level
        for aa in range(len(self.membarr)):
            self.membarr[aa].fire()

# ------------------------------------------------------------------------
# The whole net:

class neunet():

    def __init__(self, levels, members, inputs):
        self.levarr = []
        for aa in range(levels):
            self.levarr.append(neunetlevel(members, inputs))

    # Display the whole net
    def dump(self):
        print self
        for bb in self.levarr:
            print "  ", bb, bb.level
            for cc in bb.membarr:
                print "     ", cc, cc.level, cc.num, cc.serial
                print "           Inputs: ",
                for dd in cc.tentarr:
                    print " [%0.3f" % dd.input, "%0.3f" % dd.weight, "%0.3f] " % dd.bias,
                    pass
                print "Out: ", "%0.3f" % cc.output

    # Recalculate whole net
    def fire(self):
        xlen = len(self.levarr)
        for bb in range(xlen):
            self.levarr[bb].fire()
            try:
                xnext = self.levarr[bb + 1]
                self.transfer(self.levarr[bb], xnext, bb)
            except IndexError:
                pass
            except:
                raise

    def transfer(self, src, targ, inp):
        #print "transfer", src, targ, inp
        xlen = len(src.membarr)
        for aa in range(xlen):
            targ.membarr[aa].tentarr[inp].input = src.membarr[inp].output

    def showout(self):
        print "NeuNet output:",
        try:
            arr = self.levarr[len(self.levarr) - 1]
            for aa in arr.membarr:
                print "%0.3f" % aa.output,
        except:
            pass
        print

# Random in random out (with conveging on 0)

def test2(levels, neurons, inputs):

    cnt2 = 1
    levels = 3;   neurons = 4;  inputs = 4;
    
    sum = 0.0; count = 100
    for aaa in range(count):
        neu = neunet(levels, neurons, inputs)
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

    global mw
    args = conf.comline(sys.argv[1:])
    mw = MainWin()
    levels = 3;   neurons = 8;  inputs = 1;
    print "Constructing net with:", levels, "levels", neurons,  "neurons", inputs, "inputs"
    neu = neunet(levels, neurons, inputs)
    neu.fire()
        
    #test2(levels, neurons, inputs)    

    #neu.dump()
    neu.showout()

    if conf.nogui:
       sys.exit(0)
    
    gtk.main()
    sys.exit(0)


