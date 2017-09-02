#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, Lower Case ASCII letters.
# 

from pyfmshape import *

# This is a gap for the pylons. Define as 0 for continuos face, 0.01 for a 
# nice gap. The small gap helps see how the font is created.

pygap = 0.01
#pygap = 0.0

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
        vc12 = Vertex( .2,  .2,  0)
        vc13 = Vertex( .0,  .0,  0)
        vc14 = Vertex( .2,  .0,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vb11 = Vertex( .2,  .2,  0)                 # right lower
        vb12 = Vertex( .4,  .2,  0)
        vb13 = Vertex( .2 +  pygap,  .0,  0)
        vb14 = Vertex( .2 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .2,  .2+pygap,  0)           # right mid-low
        vb12 = Vertex( .4,  .2+pygap,  0)
        vb13 = Vertex( .2,  .5-pygap,  0)
        vb14 = Vertex( .4,  .5-pygap,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .1,  .5,  0)                 # mid
        vb12 = Vertex( .4,  .5,  0)
        vb13 = Vertex( .1,  .7,  0)
        vb14 = Vertex( .4,  .7,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)

        vb11 = Vertex( .2,   1.-pygap,  0)              # right mid-upper
        vb12 = Vertex( .4,   1.-pygap,  0)
        vb13 = Vertex( .2,  .7 + pygap,  0)
        vb14 = Vertex( .4,  .7 + pygap,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)

        vb11 = Vertex( .2 +  pygap,  1.2 - pygap , 0)   # upper right
        vb12 = Vertex( .2 +  pygap,  1.2 - pygap,  0)
        vb13 = Vertex( .2,  1.,  0)
        vb14 = Vertex( .4,  1.,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vc11 = Vertex( .0,  1.2,  0)
        vc12 = Vertex( .2,  1.2,  0)
        vc13 = Vertex( .0,  1.,  0)
        vc14 = Vertex( .2,  1.,  0)
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
        vc12 = Vertex( .4,  1.2,  0)
        vc13 = Vertex( .0,  1.,  0)
        vc14 = Vertex( .4,  1,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        vc11 = Vertex( .0,  1.-pygap,  0)
        vc12 = Vertex( .2,  1.-pygap,  0)
        vc13 = Vertex( .0,  .6+pygap,  0)
        vc14 = Vertex( .2,  .6+pygap,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_S4)

        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()



