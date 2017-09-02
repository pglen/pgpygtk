#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import random, math

import trans, tenticle

#random.seed()

verbose = 0

# Help identify a neuron by serial number

gl_serial = 0
    
# Deliver a random member of an array

def randmemb(var):
    rnd = random.randint(0, len(var)-1)
    #print "randmemb", rnd, "of", len(var)-1
    return var[rnd];

# ------------------------------------------------------------------------
# The basic building block  

class neuron():

    def __init__(self, inputs, level, num):

        global gl_serial
        
        self.verbose = 0
        # These are helpers
        self.num = num; self.level = level
        self.serial = gl_serial; gl_serial += 1; 
        self.transf = trans.tfunc
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
    
        sum = 0.0; xlen = len(self.tentarr)
        for aa in range(xlen):
            diff = self.tentarr[aa].fire(self)
            
            #diff = math.pow(diff, 3)
            '''if aa % 2 == 0:
                sum += diff
            else:
                sum -= diff'''
            sum += diff 
                
        #sum /= len(self.tentarr)
        #sum += self.bias
        
        self.output = self.transf(sum) 
        #self.output = trans.tfunc(sum) 
        #self.output = trans.tfunc2(sum) 
        #self.output = trans.tfunc3(sum) 
        #self.output = sum
         
        #print "%+0.3f" % self.output,
        
        if pgdebug > 2:
            print "     Neuron:", self.level, self.num 
            for dd in self.tentarr:
                print " [i=%0.3f" % dd.input, "w=%0.3f" % dd.weight, "b=%0.3f] " % dd.bias,
                #print "[%0.3f]" % dd.input,
            print
            print "     Out: %0.3f" % self.output

    def randtip(self, net):
        randmemb(self.tentarr).randtip(net, self)
        if self.verbose:
            print "randtip", self.level, self.num
    
    
    
    
    
    
    












