#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network lattice

import sys
import neuron

# ------------------------------------------------------------------------
# Globals

verbose = 0
pgdebug = 0

def pn(num):
    return "%+0.3f" % num

class lattice():

    # --------------------------------------------------------------------
    # Create a lattice of neurons
        
    def __init__(self, ins, outs):
    
        # Undo related
        self.last_neuron = None
        self.last_bias   = self.last_bias2  = None
        self.last_weight = None
        self.last_post   = None
        
        # Store a copy of the parameters
        self.ins = ins; self.outs = outs
        self.curr = 0               # Current Neuron in creation progress
        
        # Create lattice
        self.cont = []; cnt = 0
        for aa in range(ins):
            self.cont.append([])
            for bb in range(outs):  
                self.cont[aa].append(neuron.neuron(self.ins, cnt, self.curr))
                self.curr += 1
            cnt += 1       
    
    # Diagnostic dump
    def dump(self):
        #print self
        print "Lattice:"
        cnt = 0; cnt2 = 0
        for aa in self.cont:
            print "row", cnt 
            for bb in aa:
                print "  neu", cnt2, 
                for dd in bb.tentarr:
                    print "[i=%0.3f" % dd.input, "w=%0.3f" % dd.weight, "b=%0.3f]" % dd.bias,
                print "o=%0.3f" % bb.output
                cnt2 += 1
            cnt2 = 0 ; cnt += 1
                   
    # Reverse the last poke        
    def undo(self):
        if  self.last_tent != None:
            self.last_tent.parent.bias = self.last_bias2
            self.last_tent.weight = self.last_weight
            
            self.last_tent.bias = self.last_bias
            self.last_tent.post = self.last_post
            self.last_tent.multi = self.last_multi
            self.last_tent.mularr = self.last_mularr[:]
            self.last_tent = None
        else:
            print "duplicate undo"
    
    # Recalculate whole net
    def fire(self):
        cnt = 0; cnt2 = 0
        for aa in self.cont:
            for bb in aa:
                print "fire neu", cnt2, "row", bb.level, "cnt", bb.num
                bb.fire()
                cnt2 += 1
            cnt2 = 0 ; cnt += 1
                
            
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
        
    def randtip(self, val):
        randmemb(self.levarr).randtip(val)
    
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

    def setinput(self, val, ignore = False):
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
    def trainone(self, val, passes = 100):
        #print "origin:", ; neu.showout()
        cnt = 0; cnt2 = 0
        diff = 0.; old_sum = -100.    
        print "diff:",
        for aa in range(passes):
            self.randtip(diff)
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













