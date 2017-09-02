#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network level

from neuron import  * 

# ------------------------------------------------------------------------
# One level:

class neulev():

    def __init__(self, net, members, inputs, level):
        
        self.net = net; self.level = level
        
        self.membarr = []
        for aa in range(members):
            neu = neuron(inputs, self.level, aa)
            self.membarr.append(neu)
            
    def fire(self):
        #print "firing level", self.level
        for aa in range(len(self.membarr)):
            #print " firing member ", aa
            self.membarr[aa].fire()

    # Tip a random neuron
    def randtip(self):
        randmemb(self.membarr).randtip(self.net)
        


