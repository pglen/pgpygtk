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
# The Initial Low Power Requirement System 3D font
#
    
class LowerCase():

    def __init__(self):
        
        self.FontDict = {}
        self.FontSizeDict = {}
        
        # ----------------------------------------------------------------
        # The Lower Case Fonts:
        #
        # Following is an individual definition of each letter. A short synopsis
        # is maintained for visual. aA
        #
        
        # ------------------------------------------------------------------------
        #  
        #  /----\
        #  |    |
        #  \----/\
        
        chh = 'a'
        pylonarr_a = Shapearr()
        
        v31 = Vertex( .0,  .2,  0)                  # left mid
        v32 = Vertex( .2,  .2,  0)
        v33 = Vertex( .0,  .6-pygap,  0)
        v34 = Vertex( .2,  .6-pygap,  0)
        pyl_a1 = Pylon(v31, v32, v33, v34); pylonarr_a.add(pyl_a1)
        
        v41 = Vertex( .2,  .6,  0)                  # upper mid
        v42 = Vertex( .4- pygap,  .6,  0)
        v43 = Vertex( .2, .8,  0)
        v44 = Vertex( .4- pygap, .8,  0)
        pyl_a2 = Pylon(v41, v42, v43, v44); pylonarr_a.add(pyl_a2)
        
        v51 = Vertex( .4,  .8,  0)                  # mid right
        v52 = Vertex( .6,  .8,  0)
        v53 = Vertex( .4, .0 ,  0)
        v54 = Vertex( .6, .0 ,  0)
        pyl_a3 = Pylon(v51, v52, v53, v54); pylonarr_a.add(pyl_a3)
        
        vb11 = Vertex( .4 +  pygap,  .8 - pygap , 0) # upper right
        vb12 = Vertex( .4 +  pygap,  .8 - pygap,  0)
        vb13 = Vertex( .4,  .6,  0)
        vb14 = Vertex( .6,  .6,  0)
        #pyl_o9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_a.add(pyl_o9)
      
        vc11 = Vertex( .2,  .6,  0)                 # left upper
        vc12 = Vertex( .0,  .6,  0)
        vc13 = Vertex( .2,  .6,  0)
        vc14 = Vertex( .2,  .8,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_a.add(pyl_o4)

        vc11 = Vertex( .2,  .2,  0)         # lower mid
        vc12 = Vertex( .2,   0,  0)
        vc13 = Vertex( .4 - pygap,  .2,  0)
        vc14 = Vertex( .4 - pygap,   0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_a.add(pyl_o3)
      
        vc5 = Vertex( .0,  .2,  0)                  # low left
        vc6 = Vertex( .2-pygap,   .0,  0)
        vc7 = Vertex( .2-pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_a.add(pyl_o2)

        vb11 = Vertex( .6,  .2,  0)                 # right lower
        vb12 = Vertex( .7,  .0,  0)
        vb13 = Vertex( .6 +  pygap,  .0,  0)
        vb14 = Vertex( .6 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_a.add(pyl_o8)
        
        self.FontDict[chh] = pylonarr_a; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
                            
        # ------------------------------------------------------------------------
        #  |  
        #  | 
        #  |--\
        #  |   |
        #  |--/
        
        chh = 'b';  pylonarr_b = Shapearr()
        curr = pylonarr_b
        
        vc1 = Vertex( .0,  .0,  0)          # Left middle
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2 - pygap,  0)
        vc4 = Vertex( .2,  1.2 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)         # lower mid
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .4 - pygap,  .2,  0)
        vc14 = Vertex( .4 - pygap,  0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .2+ pygap,  .8,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .6,  0)
        vc13 = Vertex( .4,  .8,  0)
        vc14 = Vertex( .4,  .6,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .4,  .6-pygap,  0)           # right middle
        vb12 = Vertex( .6,  .6-pygap,  0)
        vb13 = Vertex( .4,  .2 +  pygap,  0)
        vb14 = Vertex( .6,  .2 + pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .4,  .2,  0)                 # right lower
        vb12 = Vertex( .6,  .2,  0)
        vb13 = Vertex( .4 +  pygap,  .0,  0)
        vb14 = Vertex( .4 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .4 +  pygap,  .8 - pygap , 0) # upper right
        vb12 = Vertex( .4 +  pygap,  .8 - pygap,  0)
        vb13 = Vertex( .4,  .6,  0)
        vb14 = Vertex( .6,  .6,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        self.FontDict[chh] = curr;
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----
        #  |   
        #  |   
        #  \----
        
        chh = 'c'; pylonarr_o = Shapearr()
        curr = pylonarr_o
        
        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  .6 - pygap,  0)
        vc4 = Vertex( .2,  .6 - pygap,  0)
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
        
        vc11 = Vertex( .2,  .6,  0)                 # left upper
        vc12 = Vertex( .0,  .6,  0)
        vc13 = Vertex( .2,  .6,  0)
        vc14 = Vertex( .2,  .8,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .2+ pygap,  .8,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .6,  0)
        vc13 = Vertex( .5,  .8,  0)
        vc14 = Vertex( .5,  .6,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        self.FontDict[chh] = curr;
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
     
        # ------------------------------------------------------------------------
        #       |
        #       |
        #   /---|
        #   |   |
        #   \---/
        
        chh = 'd'; pylonarr_d = Shapearr()
        curr  = pylonarr_d;
        
        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  .6 - pygap,  0)
        vc4 = Vertex( .2,  .6 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc5 = Vertex( .0,  .2,  0)          # low left
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)         # lower mid
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .4 - pygap,  .2,  0)
        vc14 = Vertex( .4 - pygap,  0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .2,  .6,  0)                 # left upper
        vc12 = Vertex( .0,  .6,  0)
        vc13 = Vertex( .2,  .6,  0)
        vc14 = Vertex( .2,  .8,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .2+ pygap,  .8,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .6,  0)
        vc13 = Vertex( .4 - pygap,  .8,  0)
        vc14 = Vertex( .4 - pygap,  .6,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .4,  1.2-pygap,  0)           # right middle
        vb12 = Vertex( .6,  1.2-pygap,  0)
        vb13 = Vertex( .4,  .0,  0)
        vb14 = Vertex( .6,  .0,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        self.FontDict[chh] = curr
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #
        #  |----\
        #  |    |
        #  |----/
        #  |
        #  \----
        
        chh = 'e'; pylonarr_e = Shapearr()
        curr = pylonarr_e
        
        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  .7 - pygap,  0)
        vc4 = Vertex( .2,  .7 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc5 = Vertex( .0 + pygap,  .2,  0)          # low left
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)         # lower mid
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .4 - pygap,  .2,  0)
        vc14 = Vertex( .4 - pygap,  0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .2,  .7,  0)                 # left upper
        vc12 = Vertex( .0,  .7,  0)
        vc13 = Vertex( .2,  .7,  0)
        vc14 = Vertex( .2,  .9,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .2+ pygap,  .9,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .7,  0)
        vc13 = Vertex( .4,  .9,  0)
        vc14 = Vertex( .4,  .7,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .4,  .7-pygap,  0)           # right middle
        vb12 = Vertex( .6,  .7-pygap,  0)
        vb13 = Vertex( .4,  .5 +  pygap,  0)
        vb14 = Vertex( .6,  .5 + pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .4,  .5,  0)                 # right lower
        vb12 = Vertex( .6,  .5,  0)
        vb13 = Vertex( .4 +  pygap,  .3,  0)
        vb14 = Vertex( .4 +  pygap,  .3,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .4 +  pygap,  .9 - pygap , 0) # upper right
        vb12 = Vertex( .4 +  pygap,  .9 - pygap,  0)
        vb13 = Vertex( .4,  .7,  0)
        vb14 = Vertex( .6,  .7,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vc11 = Vertex( .2 + pygap,  .3,  0)         # mid mid
        vc12 = Vertex( .2 + pygap,  .5,  0)
        vc13 = Vertex( .4 - pygap,  .3,  0)
        vc14 = Vertex( .4 - pygap,  .5,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vb11 = Vertex( .4,  .2,  0)                 # right lower
        vb12 = Vertex( .6,  .2,  0)
        vb13 = Vertex( .4 ,  .0,  0)
        vb14 = Vertex( .4,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        self.FontDict[chh] = curr; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /--
        #  |   
        #  |-
        #  |
        
        chh = 'f'
        pylonarr_f = Shapearr()
        curr = pylonarr_f
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  .8 - pygap,  0)
        vc4 = Vertex( .2,  .8 - pygap,  0)
        pyl_f1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_f.add(pyl_f1)
        
        vc5 = Vertex( .2,   1.,  0)
        vc6 = Vertex( .0,   .8,  0)
        vc7 = Vertex( .2,   1.,  0)
        vc8 = Vertex( .2,   .8,  0)
        pyl_f2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_f.add(pyl_f2)
        
        vc5 = Vertex( .2 + pygap,   1.,  0)
        vc6 = Vertex( .2 + pygap,   .8,  0)
        vc7 = Vertex( .4,           1.,  0)
        vc8 = Vertex( .4,           .8,  0)
        pyl_f2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_f.add(pyl_f2)
        
        vb11 = Vertex( .2 + pygap,  .4,  0)
        vb12 = Vertex( .2 + pygap,  .6,  0)
        vb13 = Vertex( .3,  .4,  0)
        vb14 = Vertex( .3,  .6,  0)
        pyl_f3 = Pylon(vb11, vb12, vb13, vb14); pylonarr_f.add(pyl_f3)
        
        self.FontDict[chh] = pylonarr_f; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----\
        #  |    |
        #  \----|
        #       |
        #   ----/
        
               
        chh = 'g'
        pylonarr_g = Shapearr()
        curr = pylonarr_g

        vc1 = Vertex( .0,  .5 + pygap,  0)      # Left middle
        vc2 = Vertex( .2,  .5 + pygap,  0)
        vc3 = Vertex( .0,  .7 - pygap,  0)
        vc4 = Vertex( .2,  .7 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)     # lower mid
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .4 - pygap,  .2,  0)
        vc14 = Vertex( .4 - pygap,  0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .0,  .2,  0)             # lower left
        vc12 = Vertex( .2,   0,  0)
        vc13 = Vertex( .2,  .2,  0)
        vc14 = Vertex( .2,   0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)

        vc11 = Vertex( .2,  .7,  0)             # left upper
        vc12 = Vertex( .0,  .7,  0)
        vc13 = Vertex( .2,  .7,  0)
        vc14 = Vertex( .2,  .9,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .0,  .5,  0)                 # left lower
        vc12 = Vertex( .2,  .3,  0)
        vc13 = Vertex( .2,  .5,  0)
        vc14 = Vertex( .2,  .3,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)

        
        vc11 = Vertex( .2+ pygap,  .9,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .7,  0)
        vc13 = Vertex( .4,  .9,  0)
        vc14 = Vertex( .4,  .7,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .4,  .7-pygap,  0)           # right middle
        vb12 = Vertex( .6,  .7-pygap,  0)
        vb13 = Vertex( .4,  .2 +  pygap,  0)
        vb14 = Vertex( .6,  .2 + pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .4,  .2,  0)                 # right lower
        vb12 = Vertex( .6,  .2,  0)
        vb13 = Vertex( .4 +  pygap,  .0,  0)
        vb14 = Vertex( .4 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .4 +  pygap,  .9 - pygap , 0) # upper right
        vb12 = Vertex( .4 +  pygap,  .9 - pygap,  0)
        vb13 = Vertex( .4,  .7,  0)
        vb14 = Vertex( .6,  .7,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        vc11 = Vertex( .2 + pygap,  .3,  0)         # mid mid
        vc12 = Vertex( .2 + pygap,  .5,  0)
        vc13 = Vertex( .4 - pygap,  .3,  0)
        vc14 = Vertex( .4 - pygap,  .5,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        self.FontDict[chh] = pylonarr_g; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
                                    
        # ------------------------------------------------------------------------
        #  |   
        #  |   
        #  |---\
        #  |   |
        #  |   |
        
        chh = 'h'
        pylonarr_h = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_h1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_h.add(pyl_h1)
        
        vc5 = Vertex( .4,       .5 - pygap,  0)
        vc6 = Vertex( .4 ,      .0,  0)
        vc7 = Vertex( .6,       .5 - pygap,  0)
        vc8 = Vertex( .6,       .0,  0)
        pyl_h2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_h.add(pyl_h2)
        
        vb11 = Vertex( .2 + pygap,  .5,  0)
        vb12 = Vertex( .2 + pygap,  .7,  0)
        vb13 = Vertex( .4 - pygap,  .5,  0)
        vb14 = Vertex( .4 - pygap,  .7,  0)
        pyl_h3 = Pylon(vb11, vb12, vb13, vb14); pylonarr_h.add(pyl_h3)
        
        vb11 = Vertex( .4,  .5,  0)
        vb12 = Vertex( .4,  .7,  0)
        vb13 = Vertex( .6,  .5,  0)
        vb14 = Vertex( .4,  .7,  0)
        pyl_h3 = Pylon(vb11, vb12, vb13, vb14); pylonarr_h.add(pyl_h3)

        self.FontDict[chh] = pylonarr_h; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |
        #  
        #  |
        #  |
        #  |
        
        chh = 'i'
        pylonarr_i = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  .7,  0)
        vc4 = Vertex( .2,  .7,  0)
        pyl_i1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_i.add(pyl_i1)
        
        vc1 = Vertex( .0,  .8,  0)
        vc2 = Vertex( .2,  .8,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_i1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_i.add(pyl_i1)

        self.FontDict[chh] = pylonarr_i; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #    |
        #    |   
        #    |   
        #  --/
        
        chh = 'j'
        pylonarr_j = Shapearr()
        
        vc1 = Vertex( .2,  .7,  0)
        vc2 = Vertex( .4,  .7,  0)
        vc3 = Vertex( .2,  .2 + pygap,  0)
        vc4 = Vertex( .4,  .2 + pygap,  0)
        pyl_j1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_j.add(pyl_j1)
        
        vc1 = Vertex( .2,  .8,  0)
        vc2 = Vertex( .4,  .8,  0)
        vc3 = Vertex( .2,  1.,  0)
        vc4 = Vertex( .4,  1.,  0)
        pyl_i1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_j.add(pyl_i1)

        vc5 = Vertex( .4 + pygap,  .2,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .4 + pygap,  .2,  0)
        vc8 = Vertex( .2,   .2,  0)
        pyl_j2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_j.add(pyl_j2)
        
        vc11 = Vertex( .0,          .2,  0)
        vc12 = Vertex( .0,          0,  0)
        vc13 = Vertex( .2 + pygap,  .2,  0)
        vc14 = Vertex( .2 + pygap,  0,  0)
        pyl_j3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_j.add(pyl_j3)
        
        self.FontDict[chh] = pylonarr_j; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |    
        #  |  
        #  |  /
        #  | /
        #  | \
        #  |  \
        
        chh = 'k'
        pylonarr_k = Shapearr()
        
        vb1 = Vertex( .0,  .0,  0)
        vb2 = Vertex( .2,  .0,  0)
        vb3 = Vertex( .0,  1.2,  0)
        vb4 = Vertex( .2,  1.2,  0)
        pyl_k1 = Pylon(vb1, vb2, vb3, vb4); pylonarr_k.add(pyl_k1)
        
        vc5 = Vertex( .2,   .4+ pygap,  0)
        vc6 = Vertex( .4,   .4+ pygap,  0)
        vc7 = Vertex( .4,   .0, 0)
        vc8 = Vertex( .6,   .0, 0)
        pyl_k2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_k.add(pyl_k2)
        
        vc11 = Vertex( .2,          .4,  0)
        vc12 = Vertex( .4,          .4,  0)
        vc13 = Vertex( .4 + pygap,  .8,  0)
        vc14 = Vertex( .6 + pygap,  .8,  0)
        pyl_k3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_k.add(pyl_k3)
        
        self.FontDict[chh] = pylonarr_k; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |
        #  |
        #  |
        #  |
        #  \---
        
        chh = 'l'
        pylonarr_l = Shapearr()
        
        vc1 = Vertex( .0,  .2,  0)
        vc2 = Vertex( .2,  .2,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_l1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_l.add(pyl_l1)
        
        vc5 = Vertex( .2+ pygap,    .0,  0)
        vc6 = Vertex( .2+ pygap,    .2,  0)
        vc7 = Vertex( .4,           .0,  0)
        vc8 = Vertex( .4,           .2,  0)
        pyl_l2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_l.add(pyl_l2)

        vc5 = Vertex( .2,    .0,  0)
        vc6 = Vertex( .0,    .2,  0)
        vc7 = Vertex( .2,    .0,  0)
        vc8 = Vertex( .2,    .2,  0)
        pyl_l2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_l.add(pyl_l2)
        
        self.FontDict[chh] = pylonarr_l; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |\    /|
        #  | \  / |
        #  |  \/  |
        #  |      |
        #  |      |
        
        chh = 'm'
        pylonarr_m = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  .6 - pygap,  0)
        vc4 = Vertex( .2,  .6 - pygap,  0)
        pyl_m1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_m.add(pyl_m1)
        
        vc1 = Vertex( .0,  .6,  0)
        vc2 = Vertex( .2,  .6,  0)
        vc3 = Vertex( .2,  .8,  0)
        vc4 = Vertex( .2,  .8,  0)
        pyl_m1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_m.add(pyl_m1)
        
        vc1 = Vertex( .2+pygap,  .6,  0)
        vc2 = Vertex( .2+pygap,  .8,  0)
        vc3 = Vertex( .6-pygap,  .6,  0)
        vc4 = Vertex( .6-pygap,  .8,  0)
        pyl_m1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_m.add(pyl_m1)
        
        vc1 = Vertex( .3,  .3,  0)
        vc2 = Vertex( .3,  .6-pygap,  0)
        vc3 = Vertex( .5,  .3,  0)
        vc4 = Vertex( .5,  .6-pygap,  0)
        pyl_m1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_m.add(pyl_m1)
        
        vc11 = Vertex( .6,  .0,  0)
        vc12 = Vertex( .8,  .0,  0)
        vc13 = Vertex( .6,  .6 - pygap,  0)
        vc14 = Vertex( .8,  .6 - pygap,  0)
        pyl_m3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_m.add(pyl_m3)

        vc1 = Vertex( .8,  .6,  0)
        vc2 = Vertex( .6,  .6,  0)
        vc3 = Vertex( .6,  .8,  0)
        vc4 = Vertex( .6,  .8,  0)
        pyl_m1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_m.add(pyl_m1)
        
        self.FontDict[chh] = pylonarr_m; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |----\   
        #  |    |
        #  |    |
        # 
        
        chh = 'n'
        pylonarr_n = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  .8,  0)
        vc4 = Vertex( .2,  .8,  0)
        pyl_n1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_n.add(pyl_n1)
        
        vc5 = Vertex( .2 + pygap,   .6,  0)
        vc6 = Vertex( .2 + pygap,   .8,  0)
        vc7 = Vertex( .4-pygap, .6,  0)
        vc8 = Vertex( .4-pygap, .8,  0)
        pyl_n2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_n.add(pyl_n2)
        
        vc11 = Vertex( .4,  .6-pygap,  0)
        vc12 = Vertex( .6,  .6-pygap,  0)
        vc13 = Vertex( .4,  .0,  0)
        vc14 = Vertex( .6,  .0,  0)
        pyl_n3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_n.add(pyl_n3)
        
        vc11 = Vertex( .4,  .8,  0)
        vc12 = Vertex( .4,  .8,  0)
        vc13 = Vertex( .4,  .6,  0)
        vc14 = Vertex( .6,  .6,  0)
        pyl_n3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_n.add(pyl_n3)
        
        self.FontDict[chh] = pylonarr_n; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----\
        #  |    |
        #  |    |
        #  \----/
        
        chh = 'o'; pylonarr_o = Shapearr()
        curr = pylonarr_o
        
        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  .6 - pygap,  0)
        vc4 = Vertex( .2,  .6 - pygap,  0)
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
        
        vc11 = Vertex( .2,  .6,  0)                 # left upper
        vc12 = Vertex( .0,  .6,  0)
        vc13 = Vertex( .2,  .6,  0)
        vc14 = Vertex( .2,  .8,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .2+ pygap,  .8,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .6,  0)
        vc13 = Vertex( .5,  .8,  0)
        vc14 = Vertex( .5,  .6,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .5,  .6-pygap,  0)           # right middle
        vb12 = Vertex( .7,  .6-pygap,  0)
        vb13 = Vertex( .5,  .2 +  pygap,  0)
        vb14 = Vertex( .7,  .2 + pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .5,  .2,  0)                 # right lower
        vb12 = Vertex( .7,  .2,  0)
        vb13 = Vertex( .5 +  pygap,  .0,  0)
        vb14 = Vertex( .5 +  pygap,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .5 +  pygap,  .8 - pygap , 0) # upper right
        vb12 = Vertex( .5 +  pygap,  .8 - pygap,  0)
        vb13 = Vertex( .5,  .6,  0)
        vb14 = Vertex( .7,  .6,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        self.FontDict[chh] = curr;
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----\
        #  |    |
        #  |----/
        #  |
        #  |
        
        chh = 'p'
        pylonarr_p = Shapearr()
        
        vc1 = Vertex( .0,  .0 + pygap,  0)
        vc2 = Vertex( .2,  .0 + pygap,  0)
        vc3 = Vertex( .0,  .8,  0)
        vc4 = Vertex( .2,  .8,  0)
        pyl_p1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_p.add(pyl_p1)
        
        #vc11 = Vertex( .2,  .8,  0)            # Upper Right
        #vc12 = Vertex( .0,  .6,  0)
        #vc13 = Vertex( .2,  .8 +  pygap,  0)
        #vc14 = Vertex( .2,  .6 + pygap,  0)
        #pyl_p4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_p.add(pyl_p4)
        
        vc11 = Vertex( .2+ pygap,   .8,  0)
        vc12 = Vertex( .2+ pygap,   .6,  0)
        vc13 = Vertex( .4,          .8,  0)
        vc14 = Vertex( .4,          .6,  0)
        pyl_p5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_p.add(pyl_p5)
        
        vb11 = Vertex( .4,  .6,  0)
        vb12 = Vertex( .6,  .6,  0)
        vb13 = Vertex( .4,  .4 +  pygap,  0)
        vb14 = Vertex( .6,  .4 + pygap,  0)
        pyl_p6 = Pylon(vb11, vb12, vb13, vb14); pylonarr_p.add(pyl_p6)
        
        vb11 = Vertex( .4,  .4,  0)
        vb12 = Vertex( .6,  .4,  0)   
        vb13 = Vertex( .4 +  pygap,  .2,  0)
        vb14 = Vertex( .4 +  pygap,  .2,  0)
        pyl_p8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_p.add(pyl_p8)
        
        vb11 = Vertex( .4 +  pygap,  .8 , 0)
        vb12 = Vertex( .4 +  pygap,  .8,  0)
        vb13 = Vertex( .4,  .6,  0)
        vb14 = Vertex( .6,  .6,  0)
        pyl_p9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_p.add(pyl_p9)
        
        vc11 = Vertex( .2 + pygap,  .4,  0)
        vc12 = Vertex( .2 + pygap,  .2,  0)
        vc13 = Vertex( .4,          .4,  0)
        vc14 = Vertex( .4,          .2,  0)
        pyl_p3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_p.add(pyl_p3)
        
        self.FontDict[chh] = pylonarr_p; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----\
        #  |    |
        #  |  \ |
        #  \--- \
        #       
        
        chh = 'q'
        pylonarr_q = Shapearr();  curr = pylonarr_q
        
        vc1 = Vertex( .0,  .2 + pygap,  0)          # Left middle
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  .6 - pygap,  0)
        vc4 = Vertex( .2,  .6 - pygap,  0)
        pyl_o1 = Pylon(vc1, vc2, vc3, vc4); curr.add(pyl_o1)
        
        vc5 = Vertex( .0 + pygap,  .2,  0)          # low left
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_o2 = Pylon(vc5, vc6, vc7, vc8); curr.add(pyl_o2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)         # lower mid
        vc12 = Vertex( .2 + pygap,   0,  0)
        vc13 = Vertex( .4 - pygap,  .2,  0)
        vc14 = Vertex( .6 - pygap,   0,  0)
        pyl_o3 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o3)
        
        vc11 = Vertex( .2,  .6,  0)                 # left upper
        vc12 = Vertex( .0,  .6,  0)
        vc13 = Vertex( .2,  .6,  0)
        vc14 = Vertex( .2,  .8,  0)
        pyl_o4 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o4)
        
        vc11 = Vertex( .2+ pygap,  .8,  0)          # upper mid
        vc12 = Vertex( .2+ pygap,  .6,  0)
        vc13 = Vertex( .5,  .8,  0)
        vc14 = Vertex( .5,  .6,  0)
        pyl_o5 = Pylon(vc11, vc12, vc13, vc14); curr.add(pyl_o5)
        
        vb11 = Vertex( .5,  .6-pygap,  0)           # right middle
        vb12 = Vertex( .7,  .6-pygap,  0)
        vb13 = Vertex( .5,  .3 +  pygap,  0)
        vb14 = Vertex( .7,  .1 + pygap,  0)
        pyl_o4 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o4)
        
        vb11 = Vertex( .3,  .3,  0)                 # right lower
        vb12 = Vertex( .5,  .3,  0)
        vb13 = Vertex( .6,  .0,  0)
        vb14 = Vertex( .8,  .0,  0)
        pyl_o8 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o8)
        
        vb11 = Vertex( .5 +  pygap,  .8 - pygap , 0) # upper right
        vb12 = Vertex( .5 +  pygap,  .8 - pygap,  0)
        vb13 = Vertex( .5,  .6,  0)
        vb14 = Vertex( .7,  .6,  0)
        pyl_o9 = Pylon(vb11, vb12, vb13, vb14); curr.add(pyl_o9)
        
        self.FontDict[chh] = curr;
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #
        #  |---\
        #  |  
        #  |   
        
        chh = 'r'
        pylonarr_r = Shapearr()
        
        vc1 = Vertex( .0,  .0 + pygap,  0)
        vc2 = Vertex( .2,  .0 + pygap,  0)
        vc3 = Vertex( .0,  .8,  0)
        vc4 = Vertex( .2,  .8,  0)
        pyl_p1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_r.add(pyl_p1)
        
        #vc11 = Vertex( .2,  .8,  0)            # Upper Right
        #vc12 = Vertex( .0,  .6,  0)
        #vc13 = Vertex( .2,  .8 +  pygap,  0)
        #vc14 = Vertex( .2,  .6 + pygap,  0)
        #pyl_p4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_p.add(pyl_p4)
        
        vc11 = Vertex( .2+ pygap,   .8,  0)
        vc12 = Vertex( .2+ pygap,   .6,  0)
        vc13 = Vertex( .4,          .8,  0)
        vc14 = Vertex( .4,          .6,  0)
        pyl_p5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_r.add(pyl_p5)
        
        vb11 = Vertex( .4,  .6,  0)
        vb12 = Vertex( .6,  .6,  0)
        vb13 = Vertex( .4,  .4 +  pygap,  0)
        vb14 = Vertex( .6,  .4 + pygap,  0)
        pyl_p6 = Pylon(vb11, vb12, vb13, vb14); pylonarr_r.add(pyl_p6)
        
        vb11 = Vertex( .4,  .4,  0)
        vb12 = Vertex( .6,  .4,  0)   
        vb13 = Vertex( .4 +  pygap,  .2,  0)
        vb14 = Vertex( .4 +  pygap,  .2,  0)
        #pyl_p8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_r.add(pyl_p8)
        
        vb11 = Vertex( .4 +  pygap,  .8 , 0)
        vb12 = Vertex( .4 +  pygap,  .8,  0)
        vb13 = Vertex( .4,  .6,  0)
        vb14 = Vertex( .6,  .6,  0)
        pyl_p9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_r.add(pyl_p9)
        
        vc11 = Vertex( .2 + pygap,  .4,  0)
        vc12 = Vertex( .2 + pygap,  .2,  0)
        vc13 = Vertex( .4,          .4,  0)
        vc14 = Vertex( .4,          .2,  0)
        #pyl_p3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_r.add(pyl_p3)
        
        self.FontDict[chh] = pylonarr_r; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /-----
        #  |    
        #  \----\
        #       |
        #  -----/
        
        chh = 's'
        pylonarr_s = Shapearr()
        
        vc1 = Vertex( .0,  .6 - pygap,  0)
        vc2 = Vertex( .2,  .6 - pygap,  0)
        vc3 = Vertex( .0,  .5+ pygap,  0)
        vc4 = Vertex( .2,  .5+ pygap,  0)
        pyl_s1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_s.add(pyl_s1)
        
        vc11 = Vertex( .0 + pygap,  .2,  0)
        vc12 = Vertex( .0 + pygap,  0,  0)
        vc13 = Vertex( .4,  .2,  0)
        vc14 = Vertex( .4,  0,  0)
        pyl_s3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_s.add(pyl_s3)
        
        vc11 = Vertex( .2,           .8,  0)
        vc12 = Vertex( .0,           .6,  0)
        vc13 = Vertex( .2 -  pygap,  .8,  0)
        vc14 = Vertex( .2 -  pygap,  .6,  0)
        pyl_s4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_s.add(pyl_s4)
        
        vc11 = Vertex( .2,  .8,  0)
        vc12 = Vertex( .2,  .6,  0)
        vc13 = Vertex( .6,  .8,  0)
        vc14 = Vertex( .6,  .6,  0)
        pyl_s5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_s.add(pyl_s5)
        
        vb11 = Vertex( .4,  .3-  pygap,  0)
        vb12 = Vertex( .6,  .3-  pygap,  0)
        vb13 = Vertex( .4,  .2+  pygap,  0)
        vb14 = Vertex( .6,  .2+  pygap,  0)
        pyl_s6 = Pylon(vb11, vb12, vb13, vb14); pylonarr_s.add(pyl_s6)
        
        vb11 = Vertex( .6,            .3,  0)
        vb12 = Vertex( .4 + pygap,    .5, 0)
        vb13 = Vertex( .4+  pygap,    .3,  0)
        vb14 = Vertex( .4+  pygap,    .5,  0)
        pyl_s7 = Pylon(vb11, vb12, vb13, vb14); pylonarr_s.add(pyl_s7)
        
        vb11 = Vertex( .4 + pygap,  .2,  0)
        vb12 = Vertex( .6,  .2,  0)
        vb13 = Vertex( .4 +  pygap,  .0,  0)
        vb14 = Vertex( .4 ,  .0,  0)
        pyl_s8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_s.add(pyl_s8)
        
        vb11 = Vertex( .2,    .3,  0)
        vb12 = Vertex( .2,    .3,  0)
        vb13 = Vertex( .0,    .5-  pygap,  0)
        vb14 = Vertex( .2,    .5-  pygap,  0)
        pyl_s9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_s.add(pyl_s9)
        
        vc11 = Vertex( .4,   .3,  0)
        vc12 = Vertex( .4 ,  .5,  0)
        vc13 = Vertex( .2 + pygap,  .3,  0)
        vc14 = Vertex( .2 + pygap,  .5,  0)
        pyl_s2 = Pylon(vc11, vc12, vc13, vc14); pylonarr_s.add(pyl_s2)
        
        self.FontDict[chh] = pylonarr_s; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #       |
        #      -|-
        #       |
        #       |
        #        \
        
        chh = 't'
        pylonarr_t = Shapearr()
        
        vc1 = Vertex( .1,  .2,  0)
        vc2 = Vertex( .3,  .2,  0)
        vc3 = Vertex( .1,   1.,  0)
        vc4 = Vertex( .3,   1.,  0)
        pyl_t1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_t.add(pyl_t1)
        
        vc5 = Vertex( .0,       .6,  0)
        vc6 = Vertex( .0,       .8,  0)
        vc7 = Vertex( .1-pygap, .6,  0)
        vc8 = Vertex( .1-pygap, .8,  0)
        pyl_t2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_t.add(pyl_t2)

        vc5 = Vertex( .3 + pygap,   .6,  0)
        vc6 = Vertex( .3 + pygap,   .8,  0)
        vc7 = Vertex( .4,           .6,  0)
        vc8 = Vertex( .4,           .8,  0)
        pyl_t2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_t.add(pyl_t2)
        
        vc5 = Vertex( .1,   .2-pygap,  0)     
        vc6 = Vertex( .3,   .0,  0)
        vc7 = Vertex( .3 ,  .2-pygap,  0)
        vc8 = Vertex( .1,   .2-pygap,  0)
        pyl_t2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_t.add(pyl_t2)
        
        vc5 = Vertex( .3+pygap,   .0,  0)     
        vc6 = Vertex( .4,   .0,  0)
        vc7 = Vertex( .3+pygap ,  .2,  0)
        vc8 = Vertex( .4,   .2,  0)
        pyl_t2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_t.add(pyl_t2)
        
        self.FontDict[chh] = pylonarr_t; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #
        #  |   |
        #  |   |
        #  \---/
        
        chh = 'u'
        pylonarr_u = Shapearr()
        
        vc1 = Vertex( .0,  .2+ pygap,  0)
        vc2 = Vertex( .2,  .2+ pygap,  0)
        vc3 = Vertex( .0,  .8,  0)
        vc4 = Vertex( .2,  .8,  0)
        pyl_u1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_u.add(pyl_u1)
        
        vc5 = Vertex( .2,   .0,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .0,   .2,  0)
        vc8 = Vertex( .2,   .2,  0)
        pyl_u2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_u.add(pyl_u2)
        
        vb11 = Vertex( .4,  .8,  0)
        vb12 = Vertex( .6,  .8,  0)
        vb13 = Vertex( .4,  .2 +  pygap,  0)
        vb14 = Vertex( .6,  .2 + pygap,  0)
        pyl_u4 = Pylon(vb11, vb12, vb13, vb14); pylonarr_u.add(pyl_u4)
        
        vb11 = Vertex( .4,  .2,  0)
        vb12 = Vertex( .6,  .2,  0)
        vb13 = Vertex( .4,  .0,  0)
        vb14 = Vertex( .4,  .0,  0)
        pyl_u8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_u.add(pyl_u8)
        
        vb11 = Vertex( .4 -  pygap,  .2 ,  0)
        vb12 = Vertex( .2 +  pygap,  .2,  0)
        vb13 = Vertex( .4 -  pygap,  .0,  0)
        vb14 = Vertex( .2 +  pygap,  .0,  0)
        pyl_u9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_u.add(pyl_u9)
        
        self.FontDict[chh] = pylonarr_u; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #   \    /
        #    \  /
        #     \/
        # 
        
        chh = 'v'
        pylonarr_v = Shapearr()
        
        vc1 = Vertex( .2,    .0,  0)
        vc2 = Vertex( .35,   .0,  0)
        vc3 = Vertex( .0,   0.8,  0)
        vc4 = Vertex( .2,   0.8,  0)
        pyl_v1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_v.add(pyl_v1)
        
        vc5 = Vertex( .2,    .0,  0)
        vc6 = Vertex( .35,   .0,  0)
        vc7 = Vertex( .4,   0.8,  0)
        vc8 = Vertex( .6,   0.8,  0)
        pyl_v2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_v.add(pyl_v2)
        
        self.FontDict[chh] = pylonarr_v; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #   \        /
        #    \  /\  /
        #     \/  \/
        # 
        
        chh = 'w'
        pylonarr_w = Shapearr()
        
        vc1 = Vertex( .2,    .0,  0)
        vc2 = Vertex( .35,   .0,  0)
        vc3 = Vertex( .0,   0.8,  0)
        vc4 = Vertex( .2,   0.8,  0)
        pyl_w1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_w.add(pyl_w1)
        
        vc5 = Vertex( .2,    .0,  0)
        vc6 = Vertex( .35,   .0,  0)
        vc7 = Vertex( .35,   .6,  0)
        vc8 = Vertex( .5,    .6,  0)
        pyl_w2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_w.add(pyl_w2)
        
        vc1 = Vertex( .55,   .0,  0)
        vc2 = Vertex( .7 ,   .0,  0)
        vc3 = Vertex( .35,   .6,  0)
        vc4 = Vertex( .5,    .6,  0)
        pyl_w3 = Pylon(vc1, vc2, vc3, vc4); pylonarr_w.add(pyl_w3)
        
        vc5 = Vertex( .55,   .0,  0)
        vc6 = Vertex( .7,    .0,  0)
        vc7 = Vertex( .7,   0.8,  0)
        vc8 = Vertex( .9,   0.8,  0)
        pyl_w4 = Pylon(vc5, vc6, vc7, vc8); pylonarr_w.add(pyl_w4)
        
        self.FontDict[chh] = pylonarr_w; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  \   /
        #   \ /  
        #   / \ 
        #  /   \
        # 
        chh = 'x'
        pylonarr_x = Shapearr()
        
        vc1 = Vertex( .4,  .0,  0)
        vc2 = Vertex( .6,  .0,  0)
        vc3 = Vertex( .0,  0.8,  0)
        vc4 = Vertex( .2,  0.8,  0)
        pyl_x1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_x.add(pyl_x1)
        
        vc5 = Vertex( .0,    .0,  0)
        vc6 = Vertex( .2,    .0,  0)
        vc7 = Vertex( .4,    0.8,  0)
        vc8 = Vertex( .6,    0.8,  0)
        pyl_x2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_x.add(pyl_x2)
        
        self.FontDict[chh] = pylonarr_x; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  \   /
        #   \ /  
        #    |
        #    |
        # 
        chh = 'y'
        pylonarr_y = Shapearr()
        
        vc1 = Vertex( .2,  .3,  0)
        vc2 = Vertex( .4,  .3,  0)
        vc3 = Vertex( .0,  0.8,  0)
        vc4 = Vertex( .2,  0.8,  0)
        pyl_y1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_y.add(pyl_y1)
        
        vc5 = Vertex( .2,    .3,  0)
        vc6 = Vertex( .4,    .3,  0)
        vc7 = Vertex( .4,    0.8,  0)
        vc8 = Vertex( .6,    0.8,  0)
        pyl_y2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_y.add(pyl_y2)
        
        vc5 = Vertex( .2,    .3-pygap,  0)
        vc6 = Vertex( .4,    .3-pygap,  0)
        vc7 = Vertex( .2,    .0,  0)
        vc8 = Vertex( .4,    .0,  0)
        pyl_y3 = Pylon(vc5, vc6, vc7, vc8); pylonarr_y.add(pyl_y3)
        
        self.FontDict[chh] = pylonarr_y; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #    ----/
        #       /
        #      /
        #     /----
        
        chh = 'z'
        pylonarr_z = Shapearr()
        
        vc1 = Vertex( .0,  .2 + pygap,  0)
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .3,  .6- pygap,  0)
        vc4 = Vertex( .5,  .6- pygap,  0)
        pyl_z1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_z.add(pyl_z1)
        
        vc5 = Vertex( .0,    .0,  0)
        vc6 = Vertex( .0,    .2,  0)
        vc7 = Vertex( .5,    .0,  0)
        vc8 = Vertex( .5,    .2,  0)
        pyl_z2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_z.add(pyl_z2)
        
        vc5 = Vertex( .0,    0.6,  0)
        vc6 = Vertex( .0,    0.8,  0)
        vc7 = Vertex( .5,    0.6,  0)
        vc8 = Vertex( .5,    0.8,  0)
        pyl_z3 = Pylon(vc5, vc6, vc7, vc8); pylonarr_z.add(pyl_z3)
        
        self.FontDict[chh] = pylonarr_z; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
    
        #for aa in self.FontDict:
        #    self.FontSizeDict[aa] = self.FontDict[aa].getShapeWidth()
            















