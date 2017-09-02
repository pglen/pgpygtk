#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network 

import sys
from neulev import  *

# ------------------------------------------------------------------------
# Globals

verbose = 0
pgdebug = 0

def pn(num):
    return "%+0.3f" % num

# ------------------------------------------------------------------------
# The whole net:
#     __             __
#  --|  |    /------|  |
#    |  |---x       |  |-----
#  --|__|    \ /----|__|     
#     __      /      __
#  --|  |    / \----|  |
#    |  |---x       |  |-----
#  --|__|    \------|__|     
#

class neunet():

    # --------------------------------------------------------------------
    # neumap = Spec of the network to create. Layer description in
    # tuple in the form of  inputs, neurons, outputs
    # Generally the number of outputs and neurons match as a neuron is 
    # defined as a neuron with one output
    
    def __init__(self, neumap):
    
        # Undo related
        self.last_neuron = None
        self.last_bias   = self.last_bias2  = None
        self.last_weight = None
        self.last_post   = None
        
        # Store a copy of the parameters
        self.neumap      = neumap[:]
        self.curr        = 0        # Current Neuron in creation progress
        
        # Create neurons
        self.levarr = []
        for ins, neus, outs in neumap:
            if verbose:
                print "creating level", self.curr
            lev = neulev(self, ins, neus, outs)
            self.levarr.append(lev)
            self.curr += 1
    
    # Diagnostic dump
    def dump(self):
        #print self
        for bb in self.levarr:
            print "Level  ", self.curr
            for cc in bb.membarr:
                print "  Neu:", self.curr, cc.num
                for dd in cc.tentarr:
                    print "     Tent:", 
                    print " [ in:", pn(dd.input), "w:", pn(dd.weight), "m:", pn(dd.multi), \
                            "b:", pn(dd.bias), "b2:", pn(dd.bias2), "p:", pn(dd.post), "]"
                print 
                print "    ",
                print "%+0.3f " % cc.output,
                print
                
    # Reverse the last poke        
    def undo(self):
        if  self.last_neuron != None:
            self.last_neuron.bias = self.last_bias
            self.last_neuron.parent.bias = self.last_bias2
            
            self.last_neuron.weight = self.last_weight
            self.last_neuron.post = self.last_post
            self.last_neuron.multi = self.last_multi
            self.last_neuron = None
        else:
            print "duplicate undo"
    
    # Recalculate whole net
    def fire(self):
        xlen = len(self.levarr)
        for bb in range(xlen-1, -1, -1):
            if verbose:
                print "firing level", bb
            self.levarr[bb].fire()
            if bb > 0:
                self._transfer(self.levarr[bb], self.levarr[bb - 1])
            #print
            
    # Propagate down the net
    def _transfer(self, src, targ):
        if verbose:
            print "transfer src", src.curr, "targ", targ.curr
        nlen = len(src.membarr); tlen = len(targ.membarr[0].tentarr)
        for aa in range(tlen):              # tenticle loop
            for bb in range(nlen):          # neuron loop
                if pgdebug > 3:
                    print "  transfer ", "tent", aa, "neu", bb, "src", bb, src.membarr[bb].output
                try:
                    targ.membarr[bb].tentarr[aa].input = src.membarr[aa].output
                except:
                    print sys.exc_info()
    
    def showin(self):
        #print "NeuNet input:",
        arr = self.levarr[len(self.levarr) - 1]
        for aa in arr.membarr:
            for bb in aa.tentarr:
                print "%+0.3f" % bb.input,
        print
        
    def showout(self):
        #print "NeuNet output:",
        arr = self.levarr[0]
        for aa in arr.membarr:
            print "%+0.3f" % aa.output,
        print 
    
    def getout(self):
        ret = []; arr = self.levarr[0]
        for aa in arr.membarr:
            ret.append(aa.output)
        return ret 
        
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
    
    def setinputbits(self, val):
        #print "setinput", val, type(val)
        inparr = self.levarr[len(self.levarr)-1]; 
        xlen = len(inparr.membarr); 
        xshift = 1; xx = 0.
        #print "xlen", xlen
        for aa in range(xlen):
            if val & xshift != 0:   xx = 1.
            else:                   xx = 0.
            print "bit", aa, ":",  xx, "  xshift ", xshift
            for bb in range(xlen):
                inparr.membarr[aa].tentarr[bb].input =  xx
            xshift <<= 1
        print

    def setinput(self, val, ignore = True):
        #print "setinput", val, type(val)
        inparr = self.levarr[len(self.levarr)-1]; 
        xlen = len(inparr.membarr)
        ylen = len(inparr.membarr[0].tentarr)
        #print xlen, ylen, len(val)
        if not ignore:
            if xlen * ylen != len(val):
                msg = "Input size must match network size of %d " % (xlen * ylen)
                raise ValueError(msg)
        cnt = 0
        for aa in range(xlen):
            for bb in range(ylen):
                inparr.membarr[aa].tentarr[bb].input =  val[cnt]
                cnt += 1

    # Compare outputs with expected data
    def cmp(self, val):
        diff = 0; outarr = self.levarr[0].membarr
        xlen = len(outarr)
        for aa in range(xlen):   
            diff += abs(val[aa] - outarr[aa].output)
        return diff / xlen
    
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






