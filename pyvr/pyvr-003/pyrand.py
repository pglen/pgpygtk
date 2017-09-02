#!/usr/bin/env python

import random

# Create a cookie cutter random genrator. 
# Optimized for speed for GL testing by pre creating a pool of 
# random numbers.

class XRand():

    def __init__(self, poolsize = 30000):
    
        self.__idx = 0
        self.__rand = []
        
        # Generate a pool of numbers
        for aa in range(poolsize):
            self.__rand.append(frand(1))
            
        # Also tried:
        #frand(1)
        #random.SystemRandom()
        #os.urandom(1)
        #( float(ord(os.urandom(1))) / 256)
          
    # Return next random number
    def rand(self, ):
        rrr = self.__rand[self.__idx]; self.__idx += 1
        if self.__idx >= len(self.__rand) - 1:
            self.__idx = 0
        return rrr
        
    # Return mid symmetric +- devi random number
    def s3(self, mid, devi):
        return  mid + self.s2(devi)
        
    # Return zero symmetric +- random number
    def s2(self, devi):
        return  devi * 2 * self.rand() - devi

     # Return random number from 0-num
    def srand(self, num):
        return  num * self.rand()

# Aliases for rand calls. See range descriptions.

# Range 0 ... num
def frand(num):
    return  num * random.random()
    #return  random.gauss(0, num)

# Range -num ... 0 ... num
def frand2(num):
    return  2 * num * random.random() - num

# Range base-dev ... base+devi 
def frand3(base, devi):
    return  base + 2 * devi * random.random() - devi

# Range xfrom ... to  
def frand4(xfrom, to):
    return  xfrom + random.random() * (to-xfrom)








