#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, math

from pgutil import  *
from mainwin import  *

# ------------------------------------------------------------------------
# Globals

gl_level        = 0
gl_num          = 0
gl_serial       = 0

# ------------------------------------------------------------------------
# Old values for the undo
gl_old_bias     = 0
gl_old_weight   = 0
gl_old_post     = 0
gl_last_neuron  = None

# ------------------------------------------------------------------------

verbose         = 0

# Deliver a random number in range of -1 to +1 

def neurand():

    ret = random.random() * 2 - 1;
    #print "%+0.3f " % ret,
    return ret
    
# Deliver a random member of an array

def randmemb(var):
    rnd = random.randint(0, len(var)-1)
    #print "randmemb", rnd, "of", len(var)-1
    return var[rnd];

# ------------------------------------------------------------------------
# Transfer function for neunet. 
# Calculate logaritmic taper, preserve sign

def tfunc(val):
    ret = 0.
    try:
        cc = float(val)
        ll = math.log(1 +  1 * abs(cc))
        ret = 1 * ll
    except ValueError:
        print sys.exc_info()
        pass
    except:
        pass
    if val < 0:
        ret = -ret;
    return ret

# ------------------------------------------------------------------------
# Basic building block of the neuron's input:

class tenticle():

    def __init__(self, curr):
    
        self.input   = neurand()
        self.weight  = neurand()
        self.bias    = neurand()
        self.post    = neurand()
        self.curr    = curr
        
    # Calculate output
    def fire(self, parent):
    
        #res = (self.input + self.bias)
        #res = (self.input + self.bias + self.post)  
        #res = (self.input + self.bias - self.post) * (1 + self.weight / 4 ) 
        #res = (self.input + self.bias) * (self.input + self.post) #* self.weight 
        res = (self.input) * (self.weight + self.bias)
        #res =  (self.input) * (1. + self.weight) + self.bias
        
        #print parent.level, parent.num, self.curr, \
        #        "input", self.input, "weight", self.weight, "bias", self.bias, "res", res
        
        #return tfunc(res)
        #return max(min(res, 2), -2)
        return res 

    def getstr(self):
        return " [inp: %0.3f" % self.input, "weigh: %0.3f" % self.weight, \
                    "bias: %0.3f ]" % self.bias, \
                    "post: %0.3f  ]" % self.post,

    def randtip(self):
        global gl_old_bias, gl_old_bias, gl_last_neuron, gl_old_post
        gl_last_neuron = self
        gl_old_weight = self.weight
        gl_old_bias = self.bias
        gl_old_post = self.post
        
        rr = random.randint(0, 2)
        if rr == 0:
            self.weight += neurand() 
        elif rr == 1:
            self.bias   += neurand()  
        elif rr == 2:
            self.post   += neurand()  
        else:
            print "bad random index"
        
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
            self.tentarr.append(tenticle(aa))

    # Fire one neuron by calling every tenticle's fire and avarage it
    def fire(self):
        global verbose
        sum = .0; xlen = len(self.tentarr)
        for aa in range(xlen):
            diff = self.tentarr[aa].fire(self)
            #print "    firing neron tent ", aa, diff 
            sum += diff
            
        #sum = math.sqrt(abs(sum))
        #if sum < 0: self.output = -self.output
        #self.output = tfunc(self.output)
        sum /= len(self.tentarr)
        #self.output = sum
        self.output = tfunc(sum)
        
        if verbose:
            print "     ", self.level, self.num ,
            for dd in self.tentarr:
                #print " [%0.3f" % dd.input, "%0.3f" % dd.weight, "%0.3f] " % dd.bias,
                print "[%0.3f]" % dd.input,
            print "Out: %0.3f" % self.output

    def randtip(self):
        randmemb(self.tentarr).randtip()
        if verbose:
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
            #print " firing member ", aa
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

    def __init__(self, levels):
    
        self.levels = levels; #self.members = members
        self.levarr = []
        exp = 1
        for aa in range(levels):
            self.levarr.append(neunetlevel(exp, 2))
            exp *= 2

    # Diagnostic dump
    def dump(self):
        print self
        for bb in self.levarr:
            print "  ", bb, bb.level
            for cc in bb.membarr:
                print "     ", cc, cc.level, cc.num, cc.serial
                print "           Inputs: ",
                for dd in cc.tentarr:
                    print " [%0.3f] " % dd.input,
                    #print " [%0.3f" % dd.input, "%0.3f" % dd.weight, "%0.3f] " % dd.bias,
                    pass
                print
                print "      ", dd.getstr()    
                print "Out: ", "%0.3f" % cc.output
        
    # Reverse the last poke        
    def undo(self):
    
        global gl_old_bias, gl_old_bias, gl_last_neuron, gl_old_post
        
        if gl_last_neuron != None:
            gl_last_neuron.bias = gl_old_bias
            gl_last_neuron.weight = gl_old_weight
            gl_last_neuron.post = gl_old_post
            gl_last_neuron = None
        else:
            print "double undo"
    
    # Recalculate whole net
    def fire(self):
        xlen = len(self.levarr)
        for bb in range(xlen-1, -1, -1):
            #print "neu", bb,
            self.levarr[bb].fire()
            if bb > 0:
                self.transfer(self.levarr[bb], self.levarr[bb - 1])
            #print
            
    # Propagate down the net
    def transfer(self, src, targ):
        #print "transfer", src, targ
        xlen = len(src.membarr)
        neu = 0; tent = 0
        for aa in range(xlen):
            #print "nn", neu, tent,
            targ.membarr[neu].tentarr[tent].input = src.membarr[aa].output
            tent += 1
            if tent >= len(targ.membarr[neu].tentarr):
                tent = 0; neu += 1  

    def showin(self):
        #print "NeuNet output:",
        arr = self.levarr[len(self.levarr) - 1]
        for aa in arr.membarr:
            for bb in aa.tentarr:
                print "%+0.3f" % bb.input,
        print
        
    def showout(self):
        #print "NeuNet input:",
        arr = self.levarr[0]
        for aa in arr.membarr:
            print "%+0.3f" % aa.output,
        print 
        
    def sum(self):
        xsum = 0. 
        arr = self.levarr[len(self.levarr) - 1]
        for aa in arr.membarr:
            xsum += aa.output  
        return xsum
        
    def randtip(self):
        randmemb(self.levarr).randtip()
    
    # --------------------------------------------------------------------
    # Set input value on the basis of the data coming in
    
    def setinput(self, val):
    
        #if self.members < 8:
        #    raise(ValueError("Not enough inputs for supplied data"))
        
        myarr = self.levarr[len(self.levarr)-1]; 
        xlen = len(myarr.membarr); xshift = 1
        #print "xlen", xlen
        neu = 0; tent = 0
        for aa in range(8):
            #print "Input", aa, xshift, val & xshift, "neu", neu, "tent", tent
            try:
                if val & xshift != 0:
                    #print "bit", aa, 1,
                    myarr.membarr[neu].tentarr[tent].input =  1.
                else:
                    #print "bit", aa, 0,
                    myarr.membarr[neu].tentarr[tent].input = -0.
            except:
                print "overflow on input", sys.exc_info()
                pass
                           
            xshift <<= 1; tent += 1
            if tent >= len(myarr.membarr[neu].tentarr):
                neu += 1; tent = 0
                
        #print

    # Compare outputs with expected data
    def cmp(self, val):
        endarr = self.levarr[0]
        diff = abs(val - endarr.membarr[0].output)
        return diff
    
    # Train this particular input to expected output
    def trainone(self, val, passes = 1000):
        #print "origin:", ; neu.showout()
        cnt = 0; cnt2 = 0
        diff = 0.; old_sum = -100.    
        for aa in range(passes):
            self.randtip()
            self.fire()
            diff = self.cmp(val)    
            if abs(diff) >= abs(old_sum):
                #print sum    
                self.undo()
                #self.fire()
                #print "undone:",
            else:
                print " ", "%+0.3f " % diff,
                cnt += 1
                #neu.showout()
                old_sum = diff
            #if diff < 0.01:
            #    break
            cnt2 += 1     
        print          
        return cnt





