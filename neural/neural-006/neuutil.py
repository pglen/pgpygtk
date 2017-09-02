#!/usr/bin/env python

import random, exceptions

# ------------------------------------------------------------------------

# Deliver a random member of an array

def randmemb(var):
    if type(var) != type( () ) and type(var) != type([]) :
        raise exceptions.ValueError("Must be a list / array")
    rnd = random.randint(0, len(var)-1)
    #print "randmemb", rnd, "of", len(var)-1
    return var[rnd];


# ------------------------------------------------------------------------
# Deliver a random number in range of 0 to +1 

def neurand():
    #ret = random.random() * 2 - 1;
    ret = random.random();
    #print "%+0.3f " % ret,
    return ret




