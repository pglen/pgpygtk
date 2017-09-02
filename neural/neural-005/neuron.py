#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import random, math, trans

random.seed()

verbose = 0

# Help identify a neuron by serial number

gl_serial = 0
    
# Deliver a random number in range of 0 to +1 

def neurand():
    ret = random.random() * 2 - 1;
    #ret = random.random();
    #print "%+0.3f " % ret,
    return ret
    
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

        if verbose:
            print "neuron init ", "%2d" % self.level, "%2d" % self.num, "    ",
        
        # Tenticles are where the magic happens 
        self.tentarr = []
        for aa in range(inputs):
            self.tentarr.append(self.tenticle(self, aa, self.num))

        if verbose:
            print 
        
        self.bias = neurand()    
        
        # Output(s)
        self.output =  neurand()
        

    # Fire one neuron by calling every tenticle's fire method and avarage it
    def fire(self):
        sum = .0; xlen = len(self.tentarr)
        for aa in range(xlen):
            diff = self.tentarr[aa].fire(self)
            sum += diff 
        sum /= len(self.tentarr)
        #sum += self.bias
        #self.output = trans.tfunc(sum)
        #self.output = trans.tfunc2(sum)
        self.output = trans.tfunc3(sum)
        self.output += self.bias
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
    
            # Ins and outs
            self.input   = neurand()
            self.output  = neurand()
            
            self.tent    = tent
            self.curr    = curr
            self.parent  = parent
            
            if verbose:
                print self.tent,
            
        # Calculate output
        def fire(self, parent):
        
            res =  (self.input) * (self.weight) 
            #res =   (self.input) * (self.weight + self.bias)
            #res =   self.input * (self.multi * self.bias2)
            #res =  (self.input + self.bias) * (self.weight) 
            #res =  (self.input) * (self.weight + self.bias) 
            #res =  (self.input) * (self.weight + self.bias) + (self.multi * self.bias2) 
            #res = (self.input + self.bias - self.post) * (self.weight) 
            #res = (self.input + self.bias) * (self.input + self.post) * self.weight 
            
            #res = (self.input + self.bias) * (self.weight) /  (self.input  + self.post) * (self.multi)
            #res =  ((self.input + self.bias) *  (self.weight + self.post)) * (self.multi + self.post)
            #res =  ((self.input + self.bias) *  (self.weight + self.post)) + (self.bias2) * (self.multi)
            
            #res =  (self.input) * (1. + self.weight) + self.bias
            
            #print parent.level, parent.num, self.curr, \
            #        "input", self.input, "weight", self.weight, "bias", self.bias, "res", res
            
            #return trans.tfunc(res)
            return res 
    
        def getstr(self):
            return " [in: %0.3f" % self.input, "w: %0.3f" % self.weight, \
                        "b: %0.3f ]" % self.bias, \
                        "p: %0.3f  ]" % self.post,
    
        def randtip(self, net, neu):
            net.last_neuron = self
            net.last_weight = self.weight
            net.last_bias   = self.bias
            net.last_post   = self.post
            net.last_multi  = self.multi
            net.last_bias2  = self.parent.bias
            
            rr = random.randint(0, 4)
            if rr == 0:
                self.weight         += neurand() 
            elif rr == 1:
                self.bias           += neurand()  
            elif rr == 2:
                self.post           += neurand()  
            elif rr == 3:
                self.multi          += neurand()  
            elif rr == 4:
                self.parent.bias    += neurand()  
            else:
                print "bad random index"
            
    
    
    
    
    
    

