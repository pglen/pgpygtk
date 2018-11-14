#!/usr/bin/env python

from __future__ import print_function
import sys
import bluepy

if __name__ == '__main__':

    #print bluepy.__dict__

    print( "Version:   ", bluepy.version())
    print( "Builddate: ",  bluepy.builddate())
    #print( "Const:     ", bluepy.OPEN)
    #print( "Const:     ", bluepy.author)
    #print( bluepy.__dict__)

    '''for aa in bluepy.__dict__.keys():
        print( aa)
        print( bluepy.__dict__[aa].__doc__)
        print( )

    print( bluepy.destroy.__doc__)'''

    buff = "Hello, this is a test string ";
    passw = "1234"

    if  len(sys.argv) > 1:
        buff = sys.argv[1]
    if  len(sys.argv) > 2:
        passw = sys.argv[2]
    
    print( "'" + "org" + "'", "'" + buff + "'")
    enc = bluepy.encrypt(buff, passw)
    print( "'" + "enc"+ "'", enc)
    hex = bluepy.tohex(enc)
    print( "hex", hex)
    uex = bluepy.fromhex(hex)
    print( "uex", uex)
    dec = bluepy.decrypt(enc, passw)
    print( "'" + "dec"+ "'", "'" + dec + "'")
    bluepy.destroy(enc)
    print( "enc", "'" + enc + "'")







