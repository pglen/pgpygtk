#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network tenticle.

verbose = 0

import random, math, trans

random.seed()

# ------------------------------------------------------------------------
# Deliver a random number in range of -1. to +1.0

def neurand():
    ret = 2 * random.random() - 1;
    #ret = random.random();
    #print "%+0.3f " % ret,
    return ret

# ------------------------------------------------------------------------
# Basic building block of the neuron's input:

class tenticle():

    def __init__(self, parent, tent, curr):

        # Additions
        self.bias    = random.random()
        self.post    = random.random()

        # Multiplications
        self.weight  = random.random()
        self.multi   = random.random()

        # Ins and outs
        self.input   = random.random()
        self.output  = random.random()

        self.tent    = tent
        self.curr    = curr
        self.parent  = parent

        if verbose:
            print self.tent,

    # Calculate output
    def fire(self, parent):
        ret = 0
        res =  self.input * self.weight
        # BAD res =  (self.input * self.weight) + self.bias
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
        #return trans.tfunc3(res)
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

        tip = neurand() #* net.old_sum
        rr = random.randint(0, 2)
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
        










