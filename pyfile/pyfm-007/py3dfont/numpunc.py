#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, Lower Case ASCII letters.
# 

from pyfmshape import *

# This is a gap for the pylons. Define as 0 for continuos face, 0.01 for a 
# nice gap. The small gap helps see how the font is created.

#pygap = 0.01
pygap = 0.0

# ------------------------------------------------------------------------
# The Initial Low Power Requirement System 3D font. Nums and Puncs.
#
    
class NumPunc():

    def __init__(self):
        
        self.FontDict = {};  self.FontSizeDict = {}
        
        # ----------------------------------------------------------------
        # The Number and puctuation Fonts:
        #
        # Following is an individual definition of each character. A short synopsis
        # is maintained for visual. aA
        #
        
        # ------------------------------------------------------------------------
        #  /|
        #   |
        #   |
        
        chh = '1';  curr =  Shapearr(); 
        
        vb11 = Vertex( .1,  .0,  0)     
        vb12 = Vertex( .3,  .0,  0)
        vb13 = Vertex( .1,  1.2,  0)
        vb14 = Vertex( .3,  1.2,  0)
        pyl_1 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_1)
        
        vb11 = Vertex( .0,          .6,  0)     
        vb12 = Vertex( .1-pygap,    .8,  0)
        vb13 = Vertex( .0,          1.,  0)
        vb14 = Vertex( .1-pygap,    1.2,  0)
        pyl_1 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #  ---\
        #     |
        #  /--/
        #  |
        #  \---
        
        chh = '2';  curr =  Shapearr(); 
        
        vc1 = Vertex( .0,  1.,  0)
        vc2 = Vertex( .3,  1.,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .3,  1.2,  0)
        pyl_S1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_S1)
        
        vb11 = Vertex( .3 +  pygap,  1.2 - pygap , 0) # upper right
        vb12 = Vertex( .3 +  pygap,  1.2 - pygap,  0)
        vb13 = Vertex( .3,  1.,  0)
        vb14 = Vertex( .5,  1.,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vc11 = Vertex( .2,   .2+pygap,  0)
        vc12 = Vertex( .0,   .2+pygap,  0)
        vc13 = Vertex( .5,   1.-pygap,  0)
        vc14 = Vertex( .3,   1.-pygap,  0)
        pyl_S3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S3)
        
        vc11 = Vertex( .0,  .2,  0)
        vc12 = Vertex( .5,  .2,  0)
        vc13 = Vertex( .0,  .0,  0)
        vc14 = Vertex( .5,  .0,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #  ---\
        #     |
        #   --/
        #     |
        #  ---/
        
        chh = '3';  curr =  Shapearr(); 
        
        vc11 = Vertex( .0,  .2,  0)
        vc12 = Vertex( .3,  .2,  0)
        vc13 = Vertex( .0,  .0,  0)
        vc14 = Vertex( .3,  .0,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vb11 = Vertex( .3,  .2,  0)                 # right lower
        vb12 = Vertex( .5,  .2,  0)
        vb13 = Vertex( .3 +  pygap,  .0,  0)
        vb14 = Vertex( .3 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .3,  .2+pygap,  0)           # right mid-low
        vb12 = Vertex( .5,  .2+pygap,  0)
        vb13 = Vertex( .3,  .5-pygap,  0)
        vb14 = Vertex( .5,  .5-pygap,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .1,  .5,  0)                 # mid
        vb12 = Vertex( .5,  .5,  0)
        vb13 = Vertex( .1,  .7,  0)
        vb14 = Vertex( .5,  .7,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)

        vb11 = Vertex( .3,   1.-pygap,  0)              # right mid-upper
        vb12 = Vertex( .5,   1.-pygap,  0)
        vb13 = Vertex( .3,  .7 + pygap,  0)
        vb14 = Vertex( .5,  .7 + pygap,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)

        vb11 = Vertex( .3 +  pygap,  1.2 - pygap , 0)   # upper right
        vb12 = Vertex( .3 +  pygap,  1.2 - pygap,  0)
        vb13 = Vertex( .3,  1.,  0)
        vb14 = Vertex( .5,  1.,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vc11 = Vertex( .0,  1.2,  0)
        vc12 = Vertex( .3,  1.2,  0)
        vc13 = Vertex( .0,  1.,  0)
        vc14 = Vertex( .3,  1.,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #  |
        #  |   
        #  |
        #   ---|
        #      |
        
        chh = '4';  curr =  Shapearr(); 
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .4,  1.2,  0)
        vc13 = Vertex( .0,  .5+pygap,  0)
        vc14 = Vertex( .2,  .5+pygap,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vc11 = Vertex( .0,  .5,  0)
        vc12 = Vertex( .5,  .5,  0)
        vc13 = Vertex( .0,  .3,  0)
        vc14 = Vertex( .5,  .3,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vc11 = Vertex( .2,  .3-pygap,  0)
        vc12 = Vertex( .4,  .3-pygap,  0)
        vc13 = Vertex( .2,  .0,  0)
        vc14 = Vertex( .4,  .0,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #  -----
        #  |   
        #  \ ---\
        #       |
        #   ----/
        
        chh = '5';  curr =  Shapearr(); 
        
        vc11 = Vertex( .0,  1.2,  0)
        vc12 = Vertex( .5,  1.2,  0)
        vc13 = Vertex( .0,  1.,  0)
        vc14 = Vertex( .5,  1,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vc11 = Vertex( .0,  1.-pygap,  0)
        vc12 = Vertex( .2,  1.-pygap,  0)
        vc13 = Vertex( .0,  .6,  0)
        vc14 = Vertex( .2,  .6,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vb11 = Vertex( .2 + pygap,   .8 , 0)
        vb12 = Vertex( .3 ,   .8,  0)
        vb13 = Vertex( .2 + pygap,   .6,  0)
        vb14 = Vertex( .3,           .6,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vb11 = Vertex( .3 + pygap,  .8 - pygap , 0) # upper right
        vb12 = Vertex( .3 + pygap,  .8 - pygap,  0)
        vb13 = Vertex( .3 + pygap,   .6,  0)
        vb14 = Vertex( .5,  .6,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vb11 = Vertex( .3,  .6-pygap,  0)           # right middle
        vb12 = Vertex( .5,  .6-pygap,  0)
        vb13 = Vertex( .3,  .2 + pygap,  0)
        vb14 = Vertex( .5,  .2 + pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .3,  .2,  0)                 # right lower
        vb12 = Vertex( .5,  .2,  0)
        vb13 = Vertex( .3 +  pygap,  .0,  0)
        vb14 = Vertex( .3 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .0,  .2,  0)                 # lower mid
        vb12 = Vertex( .3,  .2,  0)
        vb13 = Vertex( .0 +  pygap,  .0,  0)
        vb14 = Vertex( .3 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #  /----
        #  |   
        #  | ---\
        #  |    |
        #  |----/
        
        chh = '6';  curr =  Shapearr(); 
        
        vc11 = Vertex( .2+pygap,  1.2,  0)
        vc12 = Vertex( .3,  1.2,  0)
        vc13 = Vertex( .2+pygap,  1.,  0)
        vc14 = Vertex( .3,  1,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vc11 = Vertex( .3+pygap,  1.2,  0)
        vc12 = Vertex( .5,  1.2,  0)
        vc13 = Vertex( .3+pygap,  1.,  0)
        vc14 = Vertex( .3+pygap,  1,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vc1 = Vertex( .0,  1. + pygap,  0)          # Top Left
        vc2 = Vertex( .2,  1. + pygap,  0)
        vc3 = Vertex( .2,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc5 = Vertex( .0,   .2,  0)                  # low left
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2,   .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)         # lower mid
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .4 - pygap,  .2,  0)
        vc14 = Vertex( .4 - pygap,  0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .2 + pygap,  .8,  0)          # upper mid
        vc12 = Vertex( .2 + pygap,  .6,  0)
        vc13 = Vertex( .4 - pygap,  .8,  0)
        vc14 = Vertex( .4 - pygap,  .6,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .4,  .6 - pygap,  0)         # right middle
        vb12 = Vertex( .6,  .6 - pygap,  0)
        vb13 = Vertex( .4,  .2 +   pygap,  0)
        vb14 = Vertex( .6,  .2 +   pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .4,  .2,  0)                 # right lower
        vb12 = Vertex( .6,          .2,  0)
        vb13 = Vertex( .4 ,  .0,  0)
        vb14 = Vertex( .4,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .4,  .8, 0)                  # upper right
        vb12 = Vertex( .4,  .8,  0)
        vb13 = Vertex( .4,  .6,  0)
        vb14 = Vertex( .6,  .6,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #  ----
        #     /
        #    /
        #   /
        #  
        
        chh = '7';  curr =  Shapearr(); 
        
        vc11 = Vertex( .0,  1.2,  0)
        vc12 = Vertex( .5,  1.2,  0)
        vc13 = Vertex( .0,  1.,  0)
        vc14 = Vertex( .5,  1,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vc11 = Vertex( .3,  1-pygap,  0)
        vc12 = Vertex( .5,  1-pygap,  0)
        vc13 = Vertex( .0,  0.,  0)
        vc14 = Vertex( .2,  0,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   /---\
        #   |   |
        #    ---  
        #   |   |
        #   \---/
        
        chh = '8';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  .5 - pygap,  0)
        vc4 = Vertex( .2,  .5 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc5 = Vertex( .0 + pygap,  .2,  0)          # low left
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)         # lower mid
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .5 - pygap,  .2,  0)
        vc14 = Vertex( .5 - pygap,  0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .2,  .5,  0)                 # left upper
        vc12 = Vertex( .0,  .5,  0)
        vc13 = Vertex( .2,  .5,  0)
        vc14 = Vertex( .2,  .7,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .2+ pygap,  .8,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .6,  0)
        vc13 = Vertex( .5,  .8,  0)
        vc14 = Vertex( .5,  .6,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .5,  .5-pygap,  0)           # right middle
        vb12 = Vertex( .7,  .5-pygap,  0)
        vb13 = Vertex( .5,  .2 +  pygap,  0)
        vb14 = Vertex( .7,  .2 + pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .5,  .2,  0)                 # right lower
        vb12 = Vertex( .7,  .2,  0)
        vb13 = Vertex( .5 +  pygap,  .0,  0)
        vb14 = Vertex( .5 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .5 +  pygap,  .7 - pygap , 0) # upper right
        vb12 = Vertex( .5 +  pygap,  .7 - pygap,  0)
        vb13 = Vertex( .5,  .5,  0)
        vb14 = Vertex( .7,  .5,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vb11 = Vertex( .5,  .9,  0)                 # right mid up
        vb12 = Vertex( .7,  .9,  0)
        vb13 = Vertex( .5 +  pygap,  .7,  0)
        vb14 = Vertex( .5 +  pygap,  .7,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 - pygap , 0) # upper upper right
        vb12 = Vertex( .5 +  pygap,  1.2 - pygap,  0)
        vb13 = Vertex( .5,  1.,  0)
        vb14 = Vertex( .7,  1.,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)

        vc11 = Vertex( .2+ pygap,  1.2,  0)          # upper up mid
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vc11 = Vertex( .2,  1.,  0)                 # left up upper
        vc12 = Vertex( .0,  1.,  0)
        vc13 = Vertex( .2,  1.,  0)
        vc14 = Vertex( .2,  1.2,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .5,  .9+pygap,  0)               
        vc12 = Vertex( .7,  .9+pygap,  0)
        vc13 = Vertex( .5,  1.-pygap,  0)
        vc14 = Vertex( .7,  1.-pygap,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc5 = Vertex( .0,   .9,  0)                  # low mileft
        vc6 = Vertex( .2,   .7,  0)
        vc7 = Vertex( .2,   .9,  0)
        vc8 = Vertex( .0,   .9,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)

        vc11 = Vertex( .0,  .9+pygap,  0)               
        vc12 = Vertex( .2,  .9+pygap,  0)
        vc13 = Vertex( .0,  1.-pygap,  0)
        vc14 = Vertex( .2,  1.-pygap,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   /---\
        #   |   |
        #   \---|  
        #       |
        #    ---/
        
        chh = '9';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .7+ pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .7 + pygap,  0)
        vc3 = Vertex( .0,  1. - pygap,  0)
        vc4 = Vertex( .2,  1. - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc5 = Vertex( .0 + pygap,  .7,  0)          # low left
        vc6 = Vertex( .2,           .5,  0)
        vc7 = Vertex( .2 + pygap,  .7,  0)
        vc8 = Vertex( .0,           .7,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)
        
        vc11 = Vertex( .2 + pygap,  .7,  0)         # lower mid
        vc12 = Vertex( .2 + pygap,  .5,  0)
        vc13 = Vertex( .5 - pygap,  .7,  0)
        vc14 = Vertex( .5 - pygap,  .5,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .2,  1.,  0)                 # left upper
        vc12 = Vertex( .0,  1.,  0)
        vc13 = Vertex( .2,  1.,  0)
        vc14 = Vertex( .2,  1.2,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5-pygap,  1.2,  0)
        vc14 = Vertex( .5-pygap,  1.,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vc11 = Vertex( .5,  1.,  0)                 # lower mid
        vc12 = Vertex( .7,  1.,  0)
        vc13 = Vertex( .5,  .2+pygap,  0)
        vc14 = Vertex( .7,  .2+pygap,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vb11 = Vertex( .5 +  pygap,  1.2 - pygap , 0) # upper right
        vb12 = Vertex( .5 +  pygap,  1.2 - pygap,  0)
        vb13 = Vertex( .5,  1.,  0)
        vb14 = Vertex( .7,  1.,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vb11 = Vertex( .5,  .2,  0)                 # right lower
        vb12 = Vertex( .7,  .2,  0)
        vb13 = Vertex( .5,  .0,  0)
        vb14 = Vertex( .5,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .3+pygap,  .2,  0)                 # buttom mid
        vb12 = Vertex( .5-pygap,  .2,  0)
        vb13 = Vertex( .3+pygap,  .0,  0)
        vb14 = Vertex( .5-pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
  
        vc5 = Vertex( .1,   .2,  0)          # low left
        vc6 = Vertex( .3,   .0,  0)
        vc7 = Vertex( .3,   .2,  0)
        vc8 = Vertex( .1,   .2,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)
          
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
      
        # ------------------------------------------------------------------------
        #   /---\
        #   |   |
        #   | | |  
        #   |   |
        #   \---/
        
        chh = '0';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .2 + pygap,  0)
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)
        
        vc5 = Vertex( .0 + pygap,  .2,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_O2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_O2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .5,  .2,  0)
        vc14 = Vertex( .5,  0,  0)
        pyl_O3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_O3)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_O4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_O4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_O5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_O5)
        
        vb11 = Vertex( .5,  1.,  0)
        vb12 = Vertex( .7,  1.,  0)
        vb13 = Vertex( .5,  .2 +  pygap,  0)
        vb14 = Vertex( .7,  .2 + pygap,  0)
        pyl_O4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_O4)
        
        vb11 = Vertex( .5,  .2,  0)
        vb12 = Vertex( .7,  .2,  0)
        vb13 = Vertex( .5 +  pygap,  .0,  0)
        vb14 = Vertex( .5 +  pygap,  .0,  0)
        pyl_O8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_O8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 , 0)
        vb12 = Vertex( .5 +  pygap,  1.2,  0)
        vb13 = Vertex( .5,  1.0,  0)
        vb14 = Vertex( .7,  1.0,  0)
        pyl_O9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_O9)
                  
        vb11 = Vertex( .3,  .8 , 0)
        vb12 = Vertex( .4,  .8,  0)
        vb13 = Vertex( .3,  .4,  0)
        vb14 = Vertex( .4,  .4,  0)
        pyl_O9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_O9)
                  
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   /\/
        
        chh = '~';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .5,  0)
        vc2 = Vertex( .15,  .6,  0)
        vc3 = Vertex( .0,  .7,  0)
        vc4 = Vertex( .15,  .8,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        vc1 = Vertex( .15+pygap,  .8,  0)
        vc2 = Vertex( .3,        .7,  0)
        vc3 = Vertex( .15+pygap,  .6,  0)
        vc4 = Vertex( .3,        .5,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)
        
        vc1 = Vertex( .3+pygap,  .5,  0)
        vc2 = Vertex( .45,  .6,  0)
        vc3 = Vertex( .3+pygap,  .7,  0)
        vc4 = Vertex( .45,  .8,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   |
        #   |
        #   .
        
        chh = '!';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .3,  0)
        vc2 = Vertex( .2,  .3,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  .2,  0)
        vc4 = Vertex( .2,  .2,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #  /----\
        #       |
        #  /----|
        #  |    |
        #  \----/
        
        chh = '@'
        curr = Shapearr()
        
        vc1 = Vertex( .0,  .2 + pygap,  0)
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  .5,  0)
        vc4 = Vertex( .2,  .5,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)
        
        vc11 = Vertex( .2,  .7,  0)
        vc12 = Vertex( .0,  .5,  0)
        vc13 = Vertex( .2,  .7 +  pygap,  0)
        vc14 = Vertex( .2,  .5 + pygap,  0)
        pyl_O4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_O4)

        vc11 = Vertex( .2+pygap,    .7,  0)
        vc12 = Vertex( .2+pygap,    .5,  0)
        vc13 = Vertex( .5-pygap,    .7 +  pygap,  0)
        vc14 = Vertex( .5-pygap,    .5 + pygap,  0)
        pyl_O4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_O4)

        vc5 = Vertex( .0 + pygap,  .2,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_O2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_O2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .5,  .2,  0)
        vc14 = Vertex( .5,  0,  0)
        pyl_O3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_O3)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_O4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_O4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_O5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_O5)
        
        vb11 = Vertex( .5,  1.,  0)
        vb12 = Vertex( .7,  1.,  0)
        vb13 = Vertex( .5,  .2 +  pygap,  0)
        vb14 = Vertex( .7,  .2 + pygap,  0)
        pyl_O4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_O4)
        
        vb11 = Vertex( .5,  .2,  0)
        vb12 = Vertex( .7,  .2,  0)
        vb13 = Vertex( .5 +  pygap,  .0,  0)
        vb14 = Vertex( .5 +  pygap,  .0,  0)
        pyl_O8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_O8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 , 0)
        vb12 = Vertex( .5 +  pygap,  1.2,  0)
        vb13 = Vertex( .5,  1.0,  0)
        vb14 = Vertex( .7,  1.0,  0)
        pyl_O9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_O9)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #
        #    | |
        #   -----
        #   -----
        #    | |
        #
        
        chh = '#'
        curr = Shapearr()
        
        vc1 = Vertex( .0,  .3,  0)
        vc2 = Vertex( .7,  .3,  0)
        vc3 = Vertex( .0,  .5,  0)
        vc4 = Vertex( .7,  .5,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        vc1 = Vertex( .0,  .7,  0)
        vc2 = Vertex( .7,  .7,  0)
        vc3 = Vertex( .0,  .9,  0)
        vc4 = Vertex( .7,  .9,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        vc1 = Vertex( .1,  .2,  0)
        vc2 = Vertex( .3,  .2,  0)
        vc3 = Vertex( .1,  1.,  0)
        vc4 = Vertex( .3,  1.,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        vc1 = Vertex( .4,  .2,  0)
        vc2 = Vertex( .6,  .2,  0)
        vc3 = Vertex( .4,  1.,  0)
        vc4 = Vertex( .6,  1.,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /-----
        #  |    
        #  \----\
        #       |
        #  -----/
        
        chh = '$'
        curr = Shapearr()
        
        vc1 = Vertex( .0,  .7,  0)
        vc2 = Vertex( .2,  .7,  0)
        vc3 = Vertex( .0,  .9- pygap,  0)
        vc4 = Vertex( .2,  .9- pygap,  0)
        pyl_S1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_S1)
        
        vc11 = Vertex( .0 + pygap,  .3,  0)
        vc12 = Vertex( .0 + pygap,  .1,  0)
        vc13 = Vertex( .4,  .3,  0)
        vc14 = Vertex( .4,  .1,  0)
        pyl_S3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S3)
        
        vc11 = Vertex( .2,  1.1,  0)
        vc12 = Vertex( .0,  .9,  0)
        vc13 = Vertex( .2 -  pygap,  1.1,  0)
        vc14 = Vertex( .2 -  pygap,  .9,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)
        
        vc11 = Vertex( .2,  1.1,  0)
        vc12 = Vertex( .2,  .9,  0)
        vc13 = Vertex( .6,  1.1,  0)
        vc14 = Vertex( .6,  .9,  0)
        pyl_S5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S5)
        
        vb11 = Vertex( .4,  .5-  pygap,  0)
        vb12 = Vertex( .6,  .5-  pygap,  0)
        vb13 = Vertex( .4,  .3+  pygap,  0)
        vb14 = Vertex( .6,  .3+  pygap,  0)
        pyl_S6 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_S6)
        
        vb11 = Vertex( .6,            .5,  0)
        vb12 = Vertex( .4 + pygap,    .7,  0)
        vb13 = Vertex( .4+  pygap,    .5,  0)
        vb14 = Vertex( .4+  pygap,    .7,  0)
        pyl_S7 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_S7)
        
        vb11 = Vertex( .4 + pygap,   .3,  0)
        vb12 = Vertex( .6,           .3,  0)
        vb13 = Vertex( .4 +  pygap,  .1,  0)
        vb14 = Vertex( .4 ,          .1,  0)
        pyl_S8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_S8)
        
        vb11 = Vertex( .2,    .5,  0)
        vb12 = Vertex( .2,    .5,  0)
        vb13 = Vertex( .0,    .7-  pygap,  0)
        vb14 = Vertex( .2,    .7-  pygap,  0)
        pyl_S9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_S9)
        
        vc11 = Vertex( .4,   .5,  0)
        vc12 = Vertex( .4 ,  .7,  0)
        vc13 = Vertex( .2 + pygap,  .5,  0)
        vc14 = Vertex( .2 + pygap,  .7,  0)
        pyl_S2 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S2)
        
        vc11 = Vertex( .25,   .0,   0)
        vc12 = Vertex( .25 ,  1.2,  0)
        vc13 = Vertex( .35,   .0,   0)
        vc14 = Vertex( .35,   1.2,  0)
        pyl_S2 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S2)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #       /
        #  --  /
        #     /  --
        #    /
                
        chh = '%'
        curr = Shapearr()
        
        vc1 = Vertex( .0,  .2,  0)
        vc2 = Vertex( .2,  .2,  0)
        vc3 = Vertex( .5,  1.,  0)
        vc4 = Vertex( .7,  1.,  0)
        pyl_S1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_S1)
        
        vc1 = Vertex( .0,  .7,  0)
        vc2 = Vertex( .2,  .7,  0)
        vc3 = Vertex( .0,  .9,  0)
        vc4 = Vertex( .2,  .9,  0)
        pyl_S1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_S1)

        vc1 = Vertex( .5,  .3,  0)
        vc2 = Vertex( .7,  .3,  0)
        vc3 = Vertex( .5,  .5,  0)
        vc4 = Vertex( .7,  .5,  0)
        pyl_S1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_S1)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   /\
        
        chh = '^';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .8,  0)
        vc2 = Vertex( .2,  .9,  0)
        vc3 = Vertex( .0,  1.1,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        vc1 = Vertex( .2+pygap,  1.2,  0)
        vc2 = Vertex( .4,        1.1,  0)
        vc3 = Vertex( .2+pygap,  .9,  0)
        vc4 = Vertex( .4,        .8,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_O1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   /---\
        #   |   |
        #    ---  
        #   |   |
        #   \---\
        
        chh = '&';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  .5 - pygap,  0)
        vc4 = Vertex( .2,  .5 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc5 = Vertex( .0 + pygap,  .2,  0)          # low left
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)         # lower mid
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .35 - pygap,  .2,  0)
        vc14 = Vertex( .55 - pygap,  0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .2,  .5,  0)                 # left upper
        vc12 = Vertex( .0,  .5,  0)
        vc13 = Vertex( .2,  .5,  0)
        vc14 = Vertex( .2,  .7,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .2+ pygap,  .8,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .6,  0)
        vc13 = Vertex( .5,  .8,  0)
        vc14 = Vertex( .5,  .6,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .5,  .5-pygap,  0)           # right middle
        vb12 = Vertex( .7,  .5-pygap,  0)
        vb13 = Vertex( .5,  .35 +  pygap,  0)
        vb14 = Vertex( .7,  .15 + pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .5 +  pygap,  .7 - pygap , 0) # upper right
        vb12 = Vertex( .5 +  pygap,  .7 - pygap,  0)
        vb13 = Vertex( .5,  .5,  0)
        vb14 = Vertex( .7,  .5,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vb11 = Vertex( .5,  .9,  0)                 # right mid up
        vb12 = Vertex( .7,  .9,  0)
        vb13 = Vertex( .5 +  pygap,  .7,  0)
        vb14 = Vertex( .5 +  pygap,  .7,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 - pygap , 0) # upper upper right
        vb12 = Vertex( .5 +  pygap,  1.2 - pygap,  0)
        vb13 = Vertex( .5,  1.,  0)
        vb14 = Vertex( .7,  1.,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)

        vc11 = Vertex( .2+ pygap,  1.2,  0)          # upper up mid
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vc11 = Vertex( .2,  1.,  0)                 # left up upper
        vc12 = Vertex( .0,  1.,  0)
        vc13 = Vertex( .2,  1.,  0)
        vc14 = Vertex( .2,  1.2,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .5,  .9+pygap,  0)               
        vc12 = Vertex( .7,  .9+pygap,  0)
        vc13 = Vertex( .5,  1.-pygap,  0)
        vc14 = Vertex( .7,  1.-pygap,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc5 = Vertex( .0,   .9,  0)                  # low mid left
        vc6 = Vertex( .2,   .7,  0)
        vc7 = Vertex( .2,   .9,  0)
        vc8 = Vertex( .0,   .9,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)

        vc11 = Vertex( .0,  .9+pygap,  0)               
        vc12 = Vertex( .2,  .9+pygap,  0)
        vc13 = Vertex( .0,  1.-pygap,  0)
        vc14 = Vertex( .2,  1.-pygap,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .3,  .3,  0)               
        vc12 = Vertex( .5,  .3,  0)
        vc13 = Vertex( .6,  .0,  0)
        vc14 = Vertex( .8,  .0,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   
        #   \|/
        #   -|-
        #   /|\
        #   
        
        chh = '*';  curr =  Shapearr(); 

        vc1 = Vertex( .3,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .5,  .2 + pygap,  0)
        vc3 = Vertex( .3,  1. - pygap,  0)
        vc4 = Vertex( .5,  1. - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
       
        vc1 = Vertex( .0,        .5,  0)          # Left middle
        vc2 = Vertex( .3-pygap,  .5,  0)
        vc3 = Vertex( .0,        .7,  0)
        vc4 = Vertex( .3-pygap,  .7,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
       
        vc1 = Vertex( .5+pygap,        .5,  0)          # Left middle
        vc2 = Vertex( .8,        .5,  0)
        vc3 = Vertex( .5+pygap,        .7,  0)
        vc4 = Vertex( .8,        .7,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .5,         .7+pygap,  0)     
        vc2 = Vertex( .7,         .7+pygap,  0)
        vc3 = Vertex( .6,         .9,  0)
        vc4 = Vertex( .8,         .9,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .5,         .5-pygap,  0)     
        vc2 = Vertex( .7,         .5-pygap,  0)
        vc3 = Vertex( .6,         .3,  0)
        vc4 = Vertex( .8,         .3,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .1,         .7+pygap,  0)     
        vc2 = Vertex( .3,         .7+pygap,  0)
        vc3 = Vertex( .0,         .9,  0)
        vc4 = Vertex( .2,         .9,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .1,         .5-pygap,  0)     
        vc2 = Vertex( .3,         .5-pygap,  0)
        vc3 = Vertex( .0,         .3,  0)
        vc4 = Vertex( .2,         .3,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   
        #    /
        #    |
        #    |
        #    \
        
        chh = '(';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  1. - pygap,  0)
        vc4 = Vertex( .2,  1. - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,  .0 + pygap,  0)          # Left middle
        vc2 = Vertex( .4,  .0 + pygap,  0)
        vc3 = Vertex( .0,  .2,  0)
        vc4 = Vertex( .2,  .2,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,  1.2 + pygap,  0)          # Left middle
        vc2 = Vertex( .4,  1.2 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   
        #    \
        #    |
        #    |
        #    /
        
        chh = ')';  curr =  Shapearr(); 

        vc1 = Vertex( .2,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .4,  .2 + pygap,  0)
        vc3 = Vertex( .2,  1. - pygap,  0)
        vc4 = Vertex( .4,  1. - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,  .0 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .0 + pygap,  0)
        vc3 = Vertex( .2,  .2,  0)
        vc4 = Vertex( .4,  .2,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,  1.2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  1.2 + pygap,  0)
        vc3 = Vertex( .2,  1.,  0)
        vc4 = Vertex( .4,  1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()


        # ------------------------------------------------------------------------
        #   
        #    |
        #   -|-
        #    |
        #   
        
        chh = '+';  curr =  Shapearr(); 

        vc1 = Vertex( .3,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .5,  .2 + pygap,  0)
        vc3 = Vertex( .3,  1. - pygap,  0)
        vc4 = Vertex( .5,  1. - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
       
        vc1 = Vertex( .0,        .5,  0)          # Left middle
        vc2 = Vertex( .3-pygap,  .5,  0)
        vc3 = Vertex( .0,        .7,  0)
        vc4 = Vertex( .3-pygap,  .7,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
       
        vc1 = Vertex( .5+pygap,        .5,  0)          # Left middle
        vc2 = Vertex( .8,        .5,  0)
        vc3 = Vertex( .5+pygap,        .7,  0)
        vc4 = Vertex( .8,        .7,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   
        #   ---
        #   
        
        chh = '-';  curr =  Shapearr(); 

        vc1 = Vertex( .0,        .5,  0)          # Left middle
        vc2 = Vertex( .6,        .5,  0)
        vc3 = Vertex( .0,        .7,  0)
        vc4 = Vertex( .6,        .7,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   
        #   ---
        #   ---
        
        chh = '=';  curr =  Shapearr(); 

        vc1 = Vertex( .0,        .6,  0)  
        vc2 = Vertex( .6,        .6,  0)
        vc3 = Vertex( .0,        .8,  0)
        vc4 = Vertex( .6,        .8,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,        .3,  0)  
        vc2 = Vertex( .6,        .3,  0)
        vc3 = Vertex( .0,        .5,  0)
        vc4 = Vertex( .6,        .5,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   
        #   ---
        #   
        
        chh = '_';  curr =  Shapearr(); 

        vc1 = Vertex( .0,        .0,  0)  
        vc2 = Vertex( .7,        .0,  0)
        vc3 = Vertex( .0,        .2,  0)
        vc4 = Vertex( .7,        .2,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   |       
        #   |
        #   
        #   |
        #   |
        
        chh = '|';  curr =  Shapearr(); 

        vc1 = Vertex( .0,        .1,  0)  
        vc2 = Vertex( .2,        .1,  0)
        vc3 = Vertex( .0,        .5,  0)
        vc4 = Vertex( .2,        .5,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,        .7,  0)  
        vc2 = Vertex( .2,        .7,  0)
        vc3 = Vertex( .0,        1.1,  0)
        vc4 = Vertex( .2,        1.1,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   \       
        #    \
        #     \
        
        chh = '\\';  curr =  Shapearr(); 

        vc1 = Vertex( .4,        .1,  0)  
        vc2 = Vertex( .6,        .1,  0)
        vc3 = Vertex( .0,        1.1,  0)
        vc4 = Vertex( .2,        1.1,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #   \       
        #    |
        #     \
        #     /
        #    |
        #   /
        
        chh = '}';  curr =  Shapearr(); 

        vc1 = Vertex( .0,        .0,  0)  
        vc2 = Vertex( .2,        .0,  0)
        vc3 = Vertex( .2,        .2,  0)
        vc4 = Vertex( .4,        .2,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,        .2,  0)  
        vc2 = Vertex( .4,        .2,  0)
        vc3 = Vertex( .2,        .4,  0)
        vc4 = Vertex( .4,        .4,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,        .4,  0)  
        vc2 = Vertex( .4,        .4,  0)
        vc3 = Vertex( .4,        .6,  0)
        vc4 = Vertex( .6,        .6,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,        .8,  0)  
        vc2 = Vertex( .4,        .8,  0)
        vc3 = Vertex( .4,        .6,  0)
        vc4 = Vertex( .6,        .6,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,        .8,  0)  
        vc2 = Vertex( .4,        .8,  0)
        vc3 = Vertex( .2,        1.,  0)
        vc4 = Vertex( .4,        1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc1 = Vertex( .0,        1.2,  0)  
        vc2 = Vertex( .2,        1.2,  0)
        vc3 = Vertex( .2,        1.,  0)
        vc4 = Vertex( .4,        1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    /       
        #    |
        #   / 
        #   \ 
        #    |
        #    \
        
        chh = '{';  curr =  Shapearr(); 

        vc1 = Vertex( .4,        .0,  0)  
        vc2 = Vertex( .6,        .0,  0)
        vc3 = Vertex( .2,        .2,  0)
        vc4 = Vertex( .4,        .2,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,        .2,  0)  
        vc2 = Vertex( .4,        .2,  0)
        vc3 = Vertex( .2,        .4,  0)
        vc4 = Vertex( .4,        .4,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,        .4,  0)  
        vc2 = Vertex( .4,        .4,  0)
        vc3 = Vertex( .0,        .6,  0)
        vc4 = Vertex( .2,        .6,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,        .8,  0)  
        vc2 = Vertex( .4,        .8,  0)
        vc3 = Vertex( .0,        .6,  0)
        vc4 = Vertex( .2,        .6,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .2,        .8,  0)  
        vc2 = Vertex( .4,        .8,  0)
        vc3 = Vertex( .2,        1.,  0)
        vc4 = Vertex( .4,        1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc1 = Vertex( .4,        1.2,  0)  
        vc2 = Vertex( .6,        1.2,  0)
        vc3 = Vertex( .2,        1.,  0)
        vc4 = Vertex( .4,        1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    |-
        #    |
        #    |-
        
        chh = '[';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .2 + pygap,  0)          
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  1. - pygap,  0)
        vc4 = Vertex( .2,  1. - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,  .0 + pygap,  0)          # Left middle
        vc2 = Vertex( .4,  .0 + pygap,  0)
        vc3 = Vertex( .0,  .2,  0)
        vc4 = Vertex( .4,  .2,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,  1.2 + pygap,  0)          # Left middle
        vc2 = Vertex( .4,  1.2 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .4,  1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    -|
        #     |
        #    -|
        
        chh = ']';  curr =  Shapearr(); 

        vc1 = Vertex( .2,  .2 + pygap,  0)          
        vc2 = Vertex( .4,  .2 + pygap,  0)
        vc3 = Vertex( .2,  1. - pygap,  0)
        vc4 = Vertex( .4,  1. - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,  .0 + pygap,  0)          # Left middle
        vc2 = Vertex( .4,  .0 + pygap,  0)
        vc3 = Vertex( .0,  .2,  0)
        vc4 = Vertex( .4,  .2,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,  1.2 + pygap,  0)          # Left middle
        vc2 = Vertex( .4,  1.2 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .4,  1.,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    |
        #    
        #    | 
        #    
        
        chh = ':';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .3 + pygap,  0)          
        vc2 = Vertex( .2,  .3 + pygap,  0)
        vc3 = Vertex( .0,  .5 - pygap,  0)
        vc4 = Vertex( .2,  .5 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,  .7 + pygap,  0)          
        vc2 = Vertex( .2,  .7 + pygap,  0)
        vc3 = Vertex( .0,  .9 - pygap,  0)
        vc4 = Vertex( .2,  .9 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    |
        #    
        #    | 
        #    |
        #
        
        chh = ';';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .1 + pygap,  0)          
        vc2 = Vertex( .2,  .1 + pygap,  0)
        vc3 = Vertex( .1,  .5 - pygap,  0)
        vc4 = Vertex( .3,  .5 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .1,  .7 + pygap,  0)          
        vc2 = Vertex( .3,  .7 + pygap,  0)
        vc3 = Vertex( .1,  .9 - pygap,  0)
        vc4 = Vertex( .3,  .9 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    / 
        #    |
        #
        
        chh = '\'';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .8 + pygap,  0)          
        vc2 = Vertex( .2,  .8 + pygap,  0)
        vc3 = Vertex( .1,  1.2 - pygap,  0)
        vc4 = Vertex( .3,  1.2 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    / 
        #    |
        #
        
        chh = '`';  curr =  Shapearr(); 

        vc1 = Vertex( .1,  .8 + pygap,  0)          
        vc2 = Vertex( .3,  .8 + pygap,  0)
        vc3 = Vertex( .0,  1.2 - pygap,  0)
        vc4 = Vertex( .2,  1.2 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    |  |
        #    |  |
        #    |  |
        #
        
        chh = '\"';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .8 + pygap,  0)          
        vc2 = Vertex( .2,  .8 + pygap,  0)
        vc3 = Vertex( .0,  1.2 - pygap,  0)
        vc4 = Vertex( .2,  1.2 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .3,  .8 + pygap,  0)          
        vc2 = Vertex( .5,  .8 + pygap,  0)
        vc3 = Vertex( .3,  1.2 - pygap,  0)
        vc4 = Vertex( .5,  1.2 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    |
        #    |
        
        chh = ',';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .0 + pygap,  0)          
        vc2 = Vertex( .2,  .0 + pygap,  0)
        vc3 = Vertex( .1,  .3 - pygap,  0)
        vc4 = Vertex( .3,  .3 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    -
        #    
        
        chh = '.';  curr =  Shapearr(); 

        vc1 = Vertex( .0,  .0 + pygap,  0)          
        vc2 = Vertex( .2,  .0 + pygap,  0)
        vc3 = Vertex( .0,  .2 - pygap,  0)
        vc4 = Vertex( .2,  .2 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()

        # ------------------------------------------------------------------------
        #    /
        #   /
        #  / 
        
        chh = '/';  curr =  Shapearr(); 

        vc1 = Vertex( .0,        .1,  0)  
        vc2 = Vertex( .2,        .1,  0)
        vc3 = Vertex( .4,        1.1,  0)
        vc4 = Vertex( .6,        1.1,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
   
        # ------------------------------------------------------------------------
        #    /
        #   /
        #   \ 
        #    \
        
        chh = '<';  curr =  Shapearr(); 

        vc1 = Vertex( .3,        .1,  0)  
        vc2 = Vertex( .5,        .1,  0)
        vc3 = Vertex( .0,        .6,  0)
        vc4 = Vertex( .2,        .6,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .0,        .6,  0)  
        vc2 = Vertex( .2,        .6,  0)
        vc3 = Vertex( .3,        1.1,  0)
        vc4 = Vertex( .5,        1.1,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
 
        # ------------------------------------------------------------------------
        #   \
        #    \
        #    /
        #   / 
        
        chh = '>';  curr =  Shapearr(); 
        vc1 = Vertex( .0,        .1,  0)  
        vc2 = Vertex( .2,        .1,  0)
        vc3 = Vertex( .3,        .6,  0)
        vc4 = Vertex( .5,        .6,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        vc1 = Vertex( .3,        .6,  0)  
        vc2 = Vertex( .5,        .6,  0)
        vc3 = Vertex( .0,        1.1,  0)
        vc4 = Vertex( .2,        1.1,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
   

 # ------------------------------------------------------------------------
        #  /----\
        #       |
        #    /--/
        #    |
        #
        #    |
        
        chh = '?'; curr = Shapearr()
        
        vc1 = Vertex( .2,  .3,  0)
        vc2 = Vertex( .4,  .3,  0)
        vc3 = Vertex( .2,  .4-pygap,  0)
        vc4 = Vertex( .4,  .4-pygap,  0)
        pyl_P1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_P1)
        
        vc1 = Vertex( .2,  .0,  0)
        vc2 = Vertex( .4,  .0,  0)
        vc3 = Vertex( .2,  .2-pygap,  0)
        vc4 = Vertex( .4,  .2-pygap,  0)
        pyl_P1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_P1)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_P4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_P4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_P5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_P5)
        
        vb11 = Vertex( .5,  1.,  0)
        vb12 = Vertex( .7,  1.,  0)
        vb13 = Vertex( .5,  .6 +  pygap,  0)
        vb14 = Vertex( .7,  .6 + pygap,  0)
        pyl_P6 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_P6)
        
        vb11 = Vertex( .5,  .6,  0)
        vb12 = Vertex( .7,  .6,  0)
        vb13 = Vertex( .5 +  pygap,  .4,  0)
        vb14 = Vertex( .5 +  pygap,  .4,  0)
        pyl_P8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_P8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 , 0)
        vb12 = Vertex( .5 +  pygap,  1.2,  0)
        vb13 = Vertex( .5,  1.0,  0)
        vb14 = Vertex( .7,  1.0,  0)
        pyl_P9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_P9)
        
        vc11 = Vertex( .4 + pygap,  .6,  0)
        vc12 = Vertex( .4 + pygap,  .4,  0)
        vc13 = Vertex( .5,          .6,  0)
        vc14 = Vertex( .5,          .4,  0)
        pyl_P3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_P3)

        vc11 = Vertex( .4,       .6,  0)
        vc12 = Vertex( .2,       .4,  0)
        vc13 = Vertex( .4,       .6,  0)
        vc14 = Vertex( .4,       .4,  0)
        pyl_P3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_P3)
        
        self.FontDict[chh] = curr;
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
       




