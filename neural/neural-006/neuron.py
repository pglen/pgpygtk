#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import random, math

import trans, tenticle, neuutil

#random.seed()

verbose = 0

# Help identify a neuron by serial number

gl_serial = 0

# ------------------------------------------------------------------------
# The basic building block  

class neuron():

    def __init__(self, inputs, level, num):

        global gl_serial
        
        self.verbose = 0
        # These are helpers
        self.num = num; self.level = level
        self.serial = gl_serial; gl_serial += 1; 

        if verbose:
            print "neuron init ", "%2d" % self.level, "%2d" % self.num, "    ",
        
        # Tenticles are where the magic happens 
        self.tentarr = []
        for aa in range(inputs):
            self.tentarr.append(tenticle.tenticle(self, aa, self.num))

        if verbose:
            print 
        
        self.bias = tenticle.neurand()    
        
        # Output(s)
        self.output =  tenticle.neurand()

    # --------------------------------------------------------------------
    # Fire one neuron.Call every tenticle's fire method and avarage it
    
    def fire(self):
    
        sum = 0.; sum2 = 0xff; xlen = len(self.tentarr)
        for aa in range(xlen):
            diff = self.tentarr[aa].fire(self)
            if aa % 2 == 0:
                sum += diff
            else:
                sum -= diff
                
            #print "%06x %06f - " % (sum2, diff),
            #sum2 ^= int(diff * 1000000)         
                
        #sum = float(sum2) / 1000000
        #sum += self.bias
        sum /= len(self.tentarr)
        
        self.output = trans.tfunc2(sum) 
        #self.output = sum 
        #print "out: %+0.3f" % self.output,
        
        if pgdebug > 2:
            print "     Neuron:", self.level, self.num 
            for dd in self.tentarr:
                print " [i=%0.3f" % dd.input, "w=%0.3f" % dd.weight, "b=%0.3f] " % dd.bias,
                #print "[%0.3f]" % dd.input,
            print
            print "     Out: %0.3f" % self.output

    def randtip(self, net):
        neuutil.randmemb(self.tentarr).randtip(net, self)
        if self.verbose:
            print "randtip", self.level, self.num
    
    
    
    
    
    
    







