#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, 3D Font. Pain in the !@$$
#
# Just call the dict's (array's) draw method like this:
#
#     FontDict['a'].draw()  to draw an 'a'
#     ... update 3d coord by hand ...
#     FontDict['b'].draw()  to draw a 'b'
#       ... etc ... or use
#
#       print3Dstr(self, str_to_print)
#
# How it works:
#
# We create pylons from rectangles. (rects are created from triangs)
# The pylon is added to a pylon array, and the pylonarr is added to the font
# dict. The dict can draw the font at current location with the draw() function.
#

import math, sys
from copy import copy, deepcopy
import gtk.gtkgl

from OpenGL.GL import *
from OpenGL.GLU import *
from pyfmshape import *

from upper import *
from lower import *
from numpunc import *

# ------------------------------------------------------------------------
# GL Font. Costructed out of straight lines. made to be simple and fast.
#
# Use:
#       newfont =  GlFont(scale, component_1, ... component_N)
#
#       Where component is a set of pylon definitions. (see: upper.py)
#
# Example:
#
#       self.font2  = GlFont(.5, UpperCase(), LowerCase())

# The initial size is in 3d Coord. is 1.2 x 1.0 the 1/2 1/4 1/8 point
# sizes are perfect for 3D apps

# Maintain a global for the font list base.
# Note: GlList base maintained in GlListMaint class (see later)

_GlFont__LastListBase = 1024

class GlFont():

    def initvars(self):
        self.FontDict = {}; self.FontSizeDict = {};   self.FontHeight = 0

        # Merge all font components into a common one.
        # Later definitions overwrite earlier ones.
        for font in self.myfonts:
            for aa in font.FontDict:
                self.FontDict[aa] = font.FontDict[aa]
                self.FontHeight = max(self.FontHeight,
                            font.FontDict[aa].getShapeHeight())

            for aa in font.FontSizeDict:
                self.FontSizeDict[aa] = font.FontSizeDict[aa]

        # This is a gap between characters. Scaling will scale the gap too.
        self.chargap = 0.1; self.linegap = 0.1
        self.spacegap = 0.4

    # --------------------------------------------------------------------
    # Add list of fonts as needed. Last definitions override.

    def __init__(self, scale, *fonts):

        global __LastListBase
        self.lastlist = __LastListBase; __LastListBase += 512
        self.myfonts = fonts

        self.col = None; self.col2 = None
        self.initvars()

        self.scale = scale
        # Only call if we need it
        if self.scale != 1:
            self.scalefont(scale)

    # ------------------------------------------------------------------------
    # Restore initial font parameters.

    def resetfont(self):

        self.scale = 1.
        for font in self.myfonts:
            font.__init__()

        self.initvars()
        self.setfontcolor(self.col); self.setsidecolor(self.col2)

    # ------------------------------------------------------------------------
    # Set font color

    def setfontcolor(self, col):
        for kk in self.FontDict:
            for qq in self.FontDict[kk].arr:
                if self.col == None:
                    self.col = qq.ambient
                qq.ambient =  col

    # ------------------------------------------------------------------------
    # Set side color

    def setsidecolor(self, col):
        for kk in self.FontDict:
            for qq in self.FontDict[kk].arr:
                if self.col2 == None:
                    self.col2 = qq.ambient2
                qq.ambient2 =  col

    # ------------------------------------------------------------------------
    # Set 3D depth

    def setdepth(self, depth):
        for kk in self.FontDict:
            for qq in self.FontDict[kk].arr:
                qq.setdepth(depth)

    # We assume letter 'a' exists
    def getdepth(self):
        return self.FontDict['a'].arr[0].getdepth()

    # ------------------------------------------------------------------------
    # Print a 3D String. Return the width of the string in 3D space.

    def print3Dstr(self, xstr, name = 0):
        increment = 0
        for chh in xstr:
            dist = self.print3Dchar(chh, name)
            glTranslatef (dist, 0, 0)
            increment += dist
        return increment

    # ------------------------------------------------------------------------
    # Get the extent of a 3D String. Return the width, height

    def extent3Dstr(self, xstr):
        incr = 0
        for chh in xstr:
            try:
                if chh == " ":
                    dist =  self.spacegap
                else:
                    dist = self.FontSizeDict[chh] + self.chargap
                incr += dist
            except:
                  print "extent not in dict"
        return incr, self.FontHeight

    # ------------------------------------------------------------------------
    # Print One character, return advancement needed

    def print3Dchar(self, chh, name = 0):

        if chh not in self.FontDict:
            #print "print3Dchar: No character face defined for '" + chh  + "'"
            #return 1 * self.scale
            # Do not mess up our printing continuity
            return 0

        if chh == " ":
            return self.spacegap + self.chargap

        arr = self.FontDict[chh];
        curr = ord(chh)

        # Create list, in not already there
        currlist = curr + self.lastlist
        if not glIsList(currlist):
            glNewList(currlist, GL_COMPILE);
            glLoadName(name)
            arr.draw();
            glEndList()

        glCallList(currlist)
        dist = self.FontSizeDict[chh] + self.chargap
        return dist

    # ------------------------------------------------------------------------
    # Fatten / skinny the font.

    def fatfont(self, ss):
        for aa in self.FontDict:
            for bb in self.FontDict[aa].arr:
                try:
                    bb.fatpylon(ss)
                except:
                    print "Exception in skewfont:", sys.exc_info()
                    return
            self.FontSizeDict[aa] = self.FontDict[aa].getShapeWidth()

    # ------------------------------------------------------------------------
    # Scew the font

    def skewfont(self, ss):
        ss *= self.scale
        for aa in self.FontDict:
            for bb in self.FontDict[aa].arr:
                try:
                    bb.skewpylon(self.FontHeight, ss)
                except:
                    print "Exception in skewfont:", sys.exc_info()
                    return

            # We do not recalulate the font dimentions, so the skewed
            # letters fit well. Leave a space if you want between italic
            # and regular.
            #self.FontSizeDict[aa] = self.FontDict[aa].getShapeWidth()

    # ------------------------------------------------------------------------
    # Scale the font

    def scalefont(self, ss):
        # Scale these too
        self.chargap *= ss
        self.linegap *= ss
        self.spacegap *= ss

        self.FontHeight *= ss
        for aa in self.FontDict:
            for bb in self.FontDict[aa].arr:
                try:
                    bb.scalepylon(ss, ss, ss)
                except:
                    print "Exception in scalefont:", sys.exc_info()
                    return

            self.FontSizeDict[aa] = self.FontDict[aa].getShapeWidth()

# ------------------------------------------------------------------------
# Create a system font from the initial definitions
# GL Font. Costructed out of straight lines. made to be simple and fast.
#
# Use:
#       newfont =  GlSysFont(scale)
#
        
class GlSysFont(GlFont):

    def __init__(self, scale):
        GlFont.__init__(self, scale, UpperCase(), LowerCase(), NumPunc())








