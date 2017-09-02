#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network tenticle.

import trans

verbose = 0

import random, math, trans

random.seed()

# ------------------------------------------------------------------------
# Deliver a random number in range of -1. to +1.0

def neurand2():
    ret = 2 * random.random() - 1;
    #ret = random.random();
    #print "%+0.3f " % ret,
    return ret

def neurand3():
    ret = random.random();
    #ret = random.random();
    #print "%+0.3f " % ret,
    return ret

# ------------------------------------------------------------------------
# Basic building block of the neuron's input:

class tenticle():

    def __init__(self, parent, tent, curr):

        # Additions
        self.bias    = neurand3()
        self.post    = neurand3()

        # Multiplications
        self.weight  = neurand3()
        self.multi   = neurand3()

        # Ins and outs
        self.input   = neurand2()
        self.output  = neurand2()

        self.tent    = tent
        self.curr    = curr
        self.parent  = parent

        if verbose:
            print self.tent,

    # Calculate output
    def fire(self, parent):
        
        try:
            #res = self.weight / abs(self.input - self.bias) 
            res = 1. / (self.weight - self.input) + self.bias
        except:                
            print "ex"
            res = 10 
            
        #res =  self.input * self.weight
        #res =  (self.input * self.weight) + self.bias
        #res =   self.input * (self.weight + self.bias)
        #res =  (self.input + self.bias) * (self.weight)
        #res = (self.input + self.bias - self.post) * (self.weight)
        #res = (self.input + self.bias) * (self.input + self.post) * self.weight

        #res = (self.input + self.bias) * (self.weight) /  (self.input  + self.post) * (self.multi)
        #res =  ((self.input + self.bias) *  (self.weight + self.post)) * (self.multi + self.post)
        #res =  ((self.input + self.bias) *  (self.weight + self.post)) + (self.bias2) * (self.multi)

        #res =  (self.input) * (1. + self.weight) + self.bias

        #print parent.level, parent.num, self.curr, \
        #        "input", self.input, "weight", self.weight, "bias", self.bias, "res", res

        #return trans.tfunc(res)
        #return trans.tfunc2(res)
        #return trans.tfunc3(res)
        #print res, 
        return res

    def getstr(self):
        return " [in: %0.3f" % self.input, "w: %0.3f" % self.weight, \
                    "b: %0.3f ]" % self.bias, \
                    "p: %0.3f  ]" % self.post,

    # Tip a tenticle by a random amount
    def randtip(self, net, neu):
        net.last_tent   = self
        net.last_weight = self.weight
        net.last_bias   = self.bias
        net.last_post   = self.post
        net.last_multi  = self.multi
        net.last_bias2  = self.parent.bias

        tip = neurand2() / 8  # * net.last_error
        rr = random.randint(0, 1) 
        #print rr, tip
        if rr == 0:                                           
            self.weight         += tip
        elif rr == 1:
            self.bias           += tip
        elif rr == 2:
            self.parent.bias    += tip
        elif rr == 3:
            self.post           += tip
        elif rr == 4:
            self.multi          += tip  
        else:
            print "bad random index"
        

















