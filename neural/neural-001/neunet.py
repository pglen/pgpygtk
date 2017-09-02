#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, math

from pgutil import  *
from mainwin import  *

# ------------------------------------------------------------------------
# Globals

gl_level    = 0
gl_num      = 0
gl_serial   = 0

verbose     = 0

# Deliver a -1 +1 random number

def rand():

    return random.random() * 2 -1;

# Deliver a random member

def randmemb(var):

    rnd = random.randint(0, len(var)-1)
    return var[rnd];

# ------------------------------------------------------------------------
# Basic building block of the neuron's input:

class tenticle():

    def __init__(self):
        self.input   = rand()
        self.weight  = rand()
        self.bias    = rand()

    # Calculate output
    def fire(self):
        res = self.input * self.weight + self.bias
        #return tfunc(res)
        return max(min(res, 1), -1)

    def getstr(self):
        return " [%0.3f" % self.input, "%0.3f" % self.weight, "%0.3f] " % self.bias,

    def randtip(self):
        self.weight += rand()
        self.bias   += rand()
        
# ------------------------------------------------------------------------
# Transfer function for neunet. Calculate logaritmic taper, preserve sign

def tfunc(val):
    ret = 0.
    try:
        cc = float(val)
        ret = math.log(1 + 1.7 * abs(cc))
        
    except ValueError:
        #print sys.exc_info()
        pass
        
    if val < 0:
        ret = -ret;
    return ret
  
# ------------------------------------------------------------------------
# The basic building block  

class neuron():

    def __init__(self, inputs):

        global gl_level, gl_num, gl_serial
        #print "neuron init", gl_level, gl_num, gl_serial
        
        self.output = 0.0
        
        # These are helpers
        self.num = gl_num; self.serial = gl_serial; self.level = gl_level
        gl_serial += 1; gl_num += 1

        # Tenticles are where the magic happens (dentrites)
        self.tentarr = []
        for aa in range(inputs):
            self.tentarr.append(tenticle())

    # Fire one neuron by calling every tenticle's fire and avarage it
    def fire(self):
        global verbose
        sum = 0.0;   xlen = len(self.tentarr)
        for aa in range(xlen):
            sum += self.tentarr[aa].fire()
        self.output = sum / len(self.tentarr)
        
        if verbose:
            print "     ", self.level, self.num ,
            for dd in self.tentarr:
                print " [%0.3f" % dd.input, "%0.3f" % dd.weight, "%0.3f] " % dd.bias,
            print "Out: %0.3f" % self.output

    def randtip(self):
        randmemb(self.tentarr).randtip()
        print "randtip", self.level, self.num
        
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

    # Tip a random neuron
    def randtip(self):
        randmemb(self.membarr).randtip()
        
# ------------------------------------------------------------------------
# The whole net:
#
#    /--\           /--\     
#    |  |-----------|  |-----
#    |__|----\ /----|__|     
#             x
#    /--\    / \    /--\     
#    |  |---/   \---|  |-----
#    |__|-----------|__|     
#                              

class neunet():

    def __init__(self, levels, members, inputs):
        self.levels = levels; self.members = members; self.inputs = inputs
        self.total_inputs = members * inputs
        
        self.levarr = []
        for aa in range(levels):
            self.levarr.append(neunetlevel(members, inputs))

    # Diagnostic dump
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

    # Propagate down the net
    def transfer(self, src, targ, inp):
        #print "transfer", src, targ, inp
        xlen = len(src.membarr)
        for aa in range(xlen):
            for bb in range(len(targ.membarr[aa].tentarr)):
                targ.membarr[aa].tentarr[bb].input = src.membarr[aa].output

    def showout(self):
        print "NeuNet output:",
        try:
            arr = self.levarr[len(self.levarr) - 1]
            for aa in arr.membarr:
                print "%0.3f" % aa.output,
        except:
            pass
        #print
    
    def randtip(self):
        randmemb(self.levarr).randtip()
    
    # --------------------------------------------------------------------
    # Set input value on the basis of the data coming in
    
    def setinput(self, val):
    
        if self.total_inputs < 8:
            raise(ValueError("Not enough inputs for supplied data"))
        
        myarr = self.levarr[0]; xlen = len(myarr.membarr); xshift = 1
        #print "xlen", xlen
        neu = tent = 0; tentlim = len(myarr.membarr[0].tentarr)
        for aa in range(8):
            #print "Input", aa, xshift, val & xshift, "neu", neu, "tent", tent
            try:
                if val & xshift != 0:
                    #print "bit", aa, 
                    myarr.membarr[neu].tentarr[tent].input =  0.5
                else:
                    myarr.membarr[neu].tentarr[tent].input = -0.5
            except:
                print "overflow on input", sys.exc_info()
                           
            xshift <<= 1; tent += 1;
            if tent >= tentlim: 
                tent = 0; neu += 1
        print


