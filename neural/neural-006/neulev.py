#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network level

from neuron import  * 
from neuutil import  * 

# ------------------------------------------------------------------------
# One level:

class neulev():

    def __init__(self, net, inputs, neus, outs):
        
        # Back reference 
        self.net = net;
        self.curr = net.curr
        
        self.membarr = []
        for aa in range(neus):
            neu = neuron(inputs, self.net.curr, aa)
            self.membarr.append(neu)
            
    def fire(self):
        #print "firing level", self.level
        for aa in range(len(self.membarr)):
            #print " firing member ", aa
            self.membarr[aa].fire()

    # Tip a random neuron
    def randtip(self):
        randmemb(self.membarr).randtip(self.net)
        




