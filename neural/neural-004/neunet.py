#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network 

from neulev import  *

# ------------------------------------------------------------------------
# Globals

#gl_level        = 0
#gl_num          = 0
#gl_serial       = 0

# ------------------------------------------------------------------------
# Old values for the undo

#gl_old_bias     = 0
#gl_old_weight   = 0
#gl_old_post     = 0
#gl_last_neuron  = None

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

    def __init__(self, levels, neurons, inputs):
    
        # Undo related
        self.last_neuron = None
        self.last_bias   = None
        self.last_bias2  = None
        self.last_weight = None
        self.last_post   = None
        
        self.levels      = levels;
        self.neurons     = neurons;
        self.inputs      = inputs;
        self.verbose     = 0
        
        self.levarr = []
        for aa in range(levels):
            lev = neulev(self, neurons, inputs, aa)
            self.levarr.append(lev)
    
    
    # Diagnostic dump
    def dump(self):
        #print self
        for bb in self.levarr:
            print "Level  ", bb.level
            for cc in bb.membarr:
                print "  Neu:", cc.level, cc.num #, cc.serial
                for dd in cc.tentarr:
                    print "     Tent:", 
                    print "    [ in:", pn(dd.input), "w:", pn(dd.weight), \
                            "b:", pn(dd.bias), "p:", pn(dd.post), "]"
                print 
                print "    ",
                for dd in cc.outarr:
                    print "%+0.3f " % dd,
                print
                
    # Reverse the last poke        
    def undo(self):
    
        #global gl_old_bias, gl_old_bias, gl_last_neuron, gl_old_post
        
        if  self.last_neuron != None:
            self.last_neuron.bias = self.last_bias
            self.last_neuron.bias2 = self.last_bias2
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
            #print "firing", bb,
            self.levarr[bb].fire()
            if bb > 0:
                self.transfer2(self.levarr[bb], self.levarr[bb - 1])
            #print
            
    # Propagate down the net
    def transfer(self, src, targ):
        #print "transfer src", src, "targ", targ
        xlen = len(src.membarr)
        ylen = len(targ.membarr[0].tentarr)
        for aa in range(xlen):
            for bb in range(ylen):
                #print "    transfer ", "tent", aa, "neu", bb, "src", bb
                targ.membarr[aa].tentarr[bb].input = src.membarr[aa].output
    
    def transfer2(self, src, targ):
        #print "transfer src", src, "targ", targ
        xlen = len(src.membarr)
        ylen = len(targ.membarr[0].tentarr)
        for aa in range(ylen):
            for bb in range(xlen):
                #print "    transfer ", "tent", aa, "neu", bb, "src", bb
                targ.membarr[bb].tentarr[aa].input = src.membarr[bb].output
    
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

    def setinput(self, val):
        #print "setinput", val, type(val)
        inparr = self.levarr[len(self.levarr)-1]; 
        xlen = len(inparr.membarr)
        ylen = len(inparr.membarr[0].tentarr)
        print xlen, ylen, len(val)
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
    def trainone(self, val, passes = 5000):
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



