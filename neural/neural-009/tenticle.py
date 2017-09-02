#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network tenticle.

verbose = 0

import trans

from neuutil import *

# ------------------------------------------------------------------------
# Basic building block of the neuron's input:

class tenticle():

    def __init__(self, parent, tent, curr):
    
        # Additions
        self.bias    = neurand()
        self.post    = neurand()
        
        # Multiplications
        self.weight  = neurand()
        self.multi   = neurand()

        self.mularr  = []
        for aa in range(10):
            self.mularr.append(neurand())

        # Ins and outs
        self.input   = neurand()
        self.output  = neurand()
        
        self.tent    = tent
        self.curr    = curr
        self.parent  = parent
        
        if verbose:
            print self.tent,

    # --------------------------------------------------------------------        
    # Calculate output
    
    def fire(self, parent):
    
        #res =  (self.input) * (self.weight) 
        res =  (self.input + self.bias) * (self.weight) 
        
        '''res = self.input + self.bias
        for aa in range(10):
            if aa % 2 == 0:
                res += self.mularr[aa]
            else:
                res += self.mularr[aa]'''
        
        #res =  (self.input) * (self.weight + self.bias) 
        #res = (self.input + self.bias - self.post) * (self.weight) 
        #res = (self.input + self.bias) * (self.input + self.post) * self.weight 
        
        #res = (self.input + self.bias) * (self.weight) /  (self.input  + self.post) * (self.multi)
        #res =  ((self.input + self.bias) *  (self.weight + self.post)) * (self.multi + self.post)
        #res =  ((self.input + self.bias) *  (self.weight + self.post)) + (self.bias) * (self.multi)
        
        #res =  (self.input) * (1. + self.weight) + self.bias
        
        #print parent.level, parent.num, self.curr, \
        #        "input", self.input, "weight", self.weight, "bias", self.bias, "res", res
        
        #print "res", res,
        #return trans.tfunc(res)
        #return trans.tfunc2(res)
        return res 

    # Pretty print tenticle
    def getstr(self):
        return " [in: %0.3f" % self.input, "w: %0.3f" % self.weight, \
                    "b: %0.3f ]" % self.bias, \
                    "p: %0.3f  ]" % self.post,

    # Tip a tenticle by a random amount
    def randtip(self, net, neu, val):
    
        net.last_tent   = self
        net.last_weight = self.weight
        net.last_bias   = self.bias
        net.last_post   = self.post
        net.last_multi  = self.multi
        net.last_bias2  = self.parent.bias
        net.last_mularr = self.mularr[:]
        
        #rr = random.randint(0, 9)
        #self.mularr[rr] += neurand()
        
        rr = random.randint(0, 4)
        if rr == 0:
            self.weight         += neurand2()
            #self.weight         += val
        elif rr == 1:
            self.bias           += neurand2()
            #self.bias           += val  
        elif rr == 2:
            self.parent.bias    += neurand2()  
            #self.parent.bias    += val
        elif rr == 3:
            self.post           += neurand2()  
            #self.post           += val  
        elif rr == 4:
            self.multi          += neurand2()  
            #self.multi          += val
        else:
            print "bad random index"





