#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, 3D Font. Pain in the !@$$
# 
# Just call the dict's (array's) draw method like this:
#
#     FontDict['a'].draw()  to draw an 'a'
#     ... update 3d coord by hand ...
#     FontDict['b'].draw()  to draw a 'b' 
#       ... etc
#
# How it works: We create pylons from rectangles. (rects then are created 
# from triangs) The pylon is added to a pylon array, and the pylonarr is 
# added to a font dict.
#

import math, sys, rand

import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *
from pyfmshape import *
from upper import *

inited = False 
# ------------------------------------------------------------------------
# Print a 3D String. Return the width of the string in 3D coord.

def print3Dstr(xstr):

    global inited
    
    if not inited:
        inited = True 
        #scalefont(0.4)
    increment = 0
    for chh in xstr:
        dist = print3Dchar(chh)
        glTranslatef (dist, 0, 0)
        increment += dist
    return increment        

def extent3Dstr(xstr):
    increment = 0
    for chh in xstr:
        dist = getCharWidth(chh) + chargap 
        increment += dist
    return increment        

# ------------------------------------------------------------------------
# Get the character width by searching fot rightmost pylon

def print3Dchar(chh):

    global FontDict, chargap
    
    if chh not in FontDict:
        print "No character face defined for '" + chh  + "'"
        return 0
        
    arr = FontDict[chh];
    curr = ord(chh)
    
    # Create list, in not already there
    if not glIsList(curr):
        glNewList(curr, GL_COMPILE); 
        arr.draw(); 
        glEndList()
        
    glCallList(curr)
    #dist = FontSizeDict[chh] * 1.1
    dist = FontSizeDict[chh] + chargap
    return dist

# ------------------------------------------------------------------------
# Scale the font

def scalefont(ss):

    global FontDict, chargap
    chargap *= ss
    for aa in FontDict:
        for bb in FontDict[aa].arr:
            try:
                bb.scalepylon(ss, ss, ss)
            except:
                print "Exception in scalefont:", sys.exc_info()
                return
            FontSizeDict[aa] = CharWidth(FontDict[aa])
        
# ------------------------------------------------------------------------
# Get the character width by searching for the rightmost pylon

def getCharWidth(chh):
    
    ret = 0
    try:
        arr = FontDict[chh];
        ret = CharWidth(arr)
    except:
        #print "Invalid Character", chh
        # Return a mean in case it is not a good char
        ret =  1
    return ret

# ------------------------------------------------------------------------
# Get the character height

def getCharHeight(chh = 'A'):

    ret = 0
    try:
        arr = FontDict[chh];
        ret = CharHeight(arr)
    except:
        #print "Invalid Character", chh
        # Return a mean in case it is not a good char
        ret =  1
    return ret


