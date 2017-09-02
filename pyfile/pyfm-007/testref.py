#!/usr/bin/env python

# Test vertex references

import math, sys, rand

class Vertex():
    def __init__(self, x, y, z):
        self._x = x; self._y = y; self._z = z
        #self._x = copy(x); self._y = copy(y); self._z = copy(z)
        #self._x = float(x); self._y =  float(y); self._z =  float(z)
        #arr = []; cp = []
        #arr.append(x); arr.append(y); arr.append(z);
        #cp = arr[:]
        #self._x = cp[0]; self._y = cp[1]; self._z = cp[2]
    
if __name__ == '__main__':

    xx = .10; yy = .20; zz = .30
    
    v1 = Vertex(xx, yy, zz)
    #print v1
    print v1._x, v1._y, v1._z
    
    xx /= 2; yy /= 2; zz /= 2
    
    v2 = Vertex(xx, yy, zz)
    #print v2
    print v2._x, v2._y, v2._z
    
    #print v1
    print v1._x, v1._y, v1._z
    
    print xx,yy,zz

