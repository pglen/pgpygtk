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
        # is maintained for visual.
        #
        
        # ------------------------------------------------------------------------
        #   / \
        #  /   \
        #  | - |
        #  |   |
        
        chh = 'a'
        pylonarr_A = Shapearr()
        
        v31 = Vertex( .0,  .0,  0)
        v32 = Vertex( .2,  .0,  0)
        v33 = Vertex( .0,  .4,  0)
        v34 = Vertex( .2,  .4,  0)
        pyl_A1 = Pylon(v31, v32, v33, v34); pylonarr_A.add(pyl_A1)
        
        v41 = Vertex( .0,  .4,  0)
        v42 = Vertex( .2,  .6,  0)
        v43 = Vertex( .2, .4 + pygap,  0)
        v44 = Vertex( .4, .6 + pygap,  0)
        #pyl_A2 = Pylon(v41, v42, v43, v44); pylonarr_A.add(pyl_A2)
        
        v51 = Vertex( .25,  1.2,  0)
        v52 = Vertex( .45,  1.2,  0)
        v53 = Vertex( .5, .8 + pygap,  0)
        v54 = Vertex( .7, .8 + pygap,  0)
        #pyl_A3 = Pylon(v51, v52, v53, v54); pylonarr_A.add(pyl_A3)
        
        v61 = Vertex( .5,  .8,  0)
        v62 = Vertex( .7,  .8,  0)
        v63 = Vertex( .5,  .0,  0)
        v64 = Vertex( .7,  .0,  0)
        #pyl_A4 = Pylon(v61, v62, v63, v64); pylonarr_A.add(pyl_A4)
        
        v71 = Vertex( .2 + pygap,  .65,  0)
        v72 = Vertex( .5 - pygap,  .65,  0)
        v73 = Vertex( .2 + pygap,  .45,  0)
        v74 = Vertex( .5 - pygap,  .45,  0)
        pyl_A5 = Pylon(v71, v72, v73, v74); pylonarr_A.add(pyl_A5)
                                      
        self.FontDict[chh] = pylonarr_A; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
                            
        # ------------------------------------------------------------------------
        #  |--\
        #  |   |
        #  | _/
        #  |  \
        #  |   |
        #  |--/
        
        chh = 'b'
        pylonarr_B = Shapearr()
        
        vb1 = Vertex( .0,  .0,  0)
        vb2 = Vertex( .2,  .0,  0)
        vb3 = Vertex( .0,  1.2,  0)
        vb4 = Vertex( .2,  1.2,  0)
        pyl_B1 = Pylon(vb1, vb2, vb3, vb4); pylonarr_B.add(pyl_B1)
        
        vb5 = Vertex( .2 + pygap,  1.2,  0)
        vb6 = Vertex( .4,   1.2,  0)
        vb7 = Vertex( .2 + pygap,  1.0,  0)
        vb8 = Vertex( .4,   1.0,  0)
        pyl_B2 = Pylon(vb5, vb6, vb7, vb8); pylonarr_B.add(pyl_B2)
        
        vb11 = Vertex( .4 + pygap,  1.2,  0)
        vb12 = Vertex( .4 + pygap,  1.,  0)
        vb13 = Vertex( .6,  1. + pygap,  0)
        vb14 = Vertex( .6,  1. + pygap,  0)
        pyl_B3 = Pylon(vb11, vb12, vb13, vb14); pylonarr_B.add(pyl_B3)
        
        vb11 = Vertex( .4,  1.,  0)
        vb12 = Vertex( .6,  1.,  0)
        vb13 = Vertex( .4,  .8 +  pygap,  0)
        vb14 = Vertex( .6,  .8 + pygap,  0)
        pyl_B4 = Pylon(vb11, vb12, vb13, vb14); pylonarr_B.add(pyl_B4)
        
        vb11 = Vertex( .4,  .8,  0)
        vb12 = Vertex( .6,  .8,  0)
        vb13 = Vertex( .3,  .6,  0)
        vb14 = Vertex( .5,  .6,  0)
        pyl_B5 = Pylon(vb11, vb12, vb13, vb14); pylonarr_B.add(pyl_B5)
        
        vb11 = Vertex( .3,  .6,  0)
        vb12 = Vertex( .5,  .6,  0)
        vb13 = Vertex( .4,  .4,  0)
        vb14 = Vertex( .6,  .4,  0)
        pyl_B6 = Pylon(vb11, vb12, vb13, vb14); pylonarr_B.add(pyl_B6)
        
        vb11 = Vertex( .4,  .4 -  pygap,  0)
        vb12 = Vertex( .6,  .4 -  pygap,  0)
        vb13 = Vertex( .4,  .2,  0)
        vb14 = Vertex( .6,  .2,  0)
        pyl_B7 = Pylon(vb11, vb12, vb13, vb14); pylonarr_B.add(pyl_B7)
        
        vb11 = Vertex( .4,  .2 -  pygap,  0)
        vb12 = Vertex( .6,  .2 -  pygap,  0)
        vb13 = Vertex( .4,  .0,  0)
        vb14 = Vertex( .4,  .0,  0)
        pyl_B8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_B.add(pyl_B8)
        
        vb11 = Vertex( .4 -  pygap,  .2 ,  0)
        vb12 = Vertex( .2 +  pygap,  .2,  0)
        vb13 = Vertex( .4 -  pygap,  .0,  0)
        vb14 = Vertex( .2 +  pygap,  .0,  0)
        pyl_B9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_B.add(pyl_B9)
        
        self.FontDict[chh] = pylonarr_B; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----
        #  |   
        #  |   
        #  \----
        
        chh = 'c'
        pylonarr_C = Shapearr()
        
        vc1 = Vertex( .0,  .2 + pygap,  0)
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_C1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_C.add(pyl_C1)
        
        vc5 = Vertex( .0 + pygap,  .2,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_C2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_C.add(pyl_C2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .5,  .2,  0)
        vc14 = Vertex( .5,  0,  0)
        pyl_C3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_C.add(pyl_C3)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_C4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_C.add(pyl_C4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        
        pyl_C5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_C.add(pyl_C5)
        
        self.FontDict[chh] = pylonarr_C; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        #scalefont(.5)
        
        # ------------------------------------------------------------------------
        #  |---\
        #  |   |
        #  |   |
        #  |---/
        
        chh = 'd'
        pylonarr_D = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_D1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_D.add(pyl_D1)
        
        vc5 = Vertex( .2 + pygap,   1.2,  0)
        vc6 = Vertex( .2 + pygap,   1.0,  0)
        vc7 = Vertex( .4,           1.2,  0)
        vc8 = Vertex( .4,           1.0,  0)
        pyl_D2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_D.add(pyl_D2)
        
        vb11 = Vertex( .4 + pygap,  1.2,  0)
        vb12 = Vertex( .4 + pygap,  1.,  0)
        vb13 = Vertex( .6,  1. + pygap,  0)
        vb14 = Vertex( .6,  1. + pygap,  0)
        pyl_D3 = Pylon(vb11, vb12, vb13, vb14); pylonarr_D.add(pyl_D3)
        
        vb11 = Vertex( .4,  1.,  0)
        vb12 = Vertex( .6,  1.,  0)
        vb13 = Vertex( .4,  .2 +  pygap,  0)
        vb14 = Vertex( .6,  .2 + pygap,  0)
        pyl_D4 = Pylon(vb11, vb12, vb13, vb14); pylonarr_D.add(pyl_D4)
        
        vb11 = Vertex( .4,  .2,  0)
        vb12 = Vertex( .6,  .2,  0)
        vb13 = Vertex( .4,  .0,  0)
        vb14 = Vertex( .4,  .0,  0)
        pyl_D8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_D.add(pyl_D8)
        
        vb11 = Vertex( .4 -  pygap,  .2 ,  0)
        vb12 = Vertex( .2 +  pygap,  .2,  0)
        vb13 = Vertex( .4 -  pygap,  .0,  0)
        vb14 = Vertex( .2 +  pygap,  .0,  0)
        pyl_D9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_D.add(pyl_D9)
        
        self.FontDict[chh] = pylonarr_D; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |----
        #  |   
        #  |--
        #  |   
        #  |----
        
        chh = 'e'
        pylonarr_E = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_E1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_E.add(pyl_E1)
        
        vc5 = Vertex( .2 + pygap,   1.2,  0)
        vc6 = Vertex( .2 + pygap,   1.0,  0)
        vc7 = Vertex( .5,           1.2,  0)
        vc8 = Vertex( .5,           1.0,  0)
        pyl_E2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_E.add(pyl_E2)
        
        vb11 = Vertex( .2 + pygap,  .5,  0)
        vb12 = Vertex( .2 + pygap,  .7,  0)
        vb13 = Vertex( .4,  .5,  0)
        vb14 = Vertex( .4,  .7,  0)
        pyl_E3 = Pylon(vb11, vb12, vb13, vb14); pylonarr_E.add(pyl_E3)
        
        vb11 = Vertex( .2 +  pygap,   .0,  0)
        vb12 = Vertex( .2 +  pygap,   .2,  0)
        vb13 = Vertex( .5,  .0,  0)
        vb14 = Vertex( .5,  .2 + pygap,  0)
        pyl_E4 = Pylon(vb11, vb12, vb13, vb14); pylonarr_E.add(pyl_E4)
        
        self.FontDict[chh] = pylonarr_E; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |----
        #  |   
        #  |--
        #  |   
        #  |
        
        chh = 'f'
        pylonarr_F = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_F1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_F.add(pyl_F1)
        
        vc5 = Vertex( .2 + pygap,   1.2,  0)
        vc6 = Vertex( .2 + pygap,   1.0,  0)
        vc7 = Vertex( .5,           1.2,  0)
        vc8 = Vertex( .5,           1.0,  0)
        pyl_F2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_F.add(pyl_F2)
        
        vb11 = Vertex( .2 + pygap,  .5,  0)
        vb12 = Vertex( .2 + pygap,  .7,  0)
        vb13 = Vertex( .4,  .5,  0)
        vb14 = Vertex( .4,  .7,  0)
        pyl_F3 = Pylon(vb11, vb12, vb13, vb14); pylonarr_F.add(pyl_F3)
        
        self.FontDict[chh] = pylonarr_F; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----
        #  |   
        #  |  -|
        #  \----
               
        chh = 'g'
        pylonarr_G = Shapearr()
        
        vc1 = Vertex( .0,  .2 + pygap,  0)
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_G1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_G.add(pyl_G1)
        
        vc5 = Vertex( .0 + pygap,  .2,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_G2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_G.add(pyl_G2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)
        vc12 = Vertex( .2 + pygap,   0,  0)
        vc13 = Vertex( .6,          .2,  0)
        vc14 = Vertex( .6,           0,  0)
        pyl_G3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_G.add(pyl_G3)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_G4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_G.add(pyl_G4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .6,  1.2,  0)
        vc14 = Vertex( .6,  1.,  0)
        pyl_G5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_G.add(pyl_G5)
        
        vc11 = Vertex( .4,  .6,  0)
        vc12 = Vertex( .6,  .6,  0)
        vc13 = Vertex( .4,  .2 + pygap,  0)
        vc14 = Vertex( .6,  .2 + pygap,  0)
        pyl_G6 = Pylon(vc11, vc12, vc13, vc14); pylonarr_G.add(pyl_G6)
        
        vc11 = Vertex( .3,  .6 ,  0)
        vc12 = Vertex( .4- pygap,  .6,  0)
        vc13 = Vertex( .3,  .4 ,  0)
        vc14 = Vertex( .4- pygap,  .4 ,  0)
        pyl_G7 = Pylon(vc11, vc12, vc13, vc14); pylonarr_G.add(pyl_G7)
        
        self.FontDict[chh] = pylonarr_G; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
                                    
        # ------------------------------------------------------------------------
        #  |   |
        #  |   |
        #  |---|
        #  |   |
        #  |   |
        
        chh = 'h'
        pylonarr_H = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_H1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_H.add(pyl_H1)
        
        vc5 = Vertex( .4,       1.2,  0)
        vc6 = Vertex( .4 ,      .0,  0)
        vc7 = Vertex( .6,       1.2,  0)
        vc8 = Vertex( .6,       .0,  0)
        pyl_H2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_H.add(pyl_H2)
        
        vb11 = Vertex( .2 + pygap,  .5,  0)
        vb12 = Vertex( .2 + pygap,  .7,  0)
        vb13 = Vertex( .4 - pygap,  .5,  0)
        vb14 = Vertex( .4 - pygap,  .7,  0)
        pyl_H3 = Pylon(vb11, vb12, vb13, vb14); pylonarr_H.add(pyl_H3)
        
        self.FontDict[chh] = pylonarr_H; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |
        #  |
        #  |
        #  |
        #  |
        
        chh = 'i'
        pylonarr_I = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_I1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_I.add(pyl_I1)
        
        self.FontDict[chh] = pylonarr_I; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #    |
        #    |   
        #    |   
        #  --/
        
        chh = 'j'
        pylonarr_J = Shapearr()
        
        vc1 = Vertex( .2,  1.2,  0)
        vc2 = Vertex( .4,  1.2,  0)
        vc3 = Vertex( .2,  .2 + pygap,  0)
        vc4 = Vertex( .4,  .2 + pygap,  0)
        pyl_J1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_J.add(pyl_J1)
        
        vc5 = Vertex( .4 + pygap,  .2,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .4 + pygap,  .2,  0)
        vc8 = Vertex( .2,   .2,  0)
        pyl_J2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_J.add(pyl_J2)
        
        vc11 = Vertex( .0,          .2,  0)
        vc12 = Vertex( .0,          0,  0)
        vc13 = Vertex( .2 + pygap,  .2,  0)
        vc14 = Vertex( .2 + pygap,  0,  0)
        pyl_J3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_J.add(pyl_J3)
        
        self.FontDict[chh] = pylonarr_J; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |    /
        #  |  /
        #  |/
        #  |\
        #  |  \
        #  |    \
        
        chh = 'k'
        pylonarr_K = Shapearr()
        
        vb1 = Vertex( .0,  .0,  0)
        vb2 = Vertex( .2,  .0,  0)
        vb3 = Vertex( .0,  1.2,  0)
        vb4 = Vertex( .2,  1.2,  0)
        pyl_K1 = Pylon(vb1, vb2, vb3, vb4); pylonarr_K.add(pyl_K1)
        
        vc5 = Vertex( .2,   .6+ pygap,  0)
        vc6 = Vertex( .4,   .6+ pygap,  0)
        vc7 = Vertex( .4,   1.2, 0)
        vc8 = Vertex( .6,   1.2, 0)
        pyl_K2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_K.add(pyl_K2)
        
        vc11 = Vertex( .2,          .6,  0)
        vc12 = Vertex( .4,          .6,  0)
        vc13 = Vertex( .4 + pygap,  .0,  0)
        vc14 = Vertex( .6 + pygap,  .0,  0)
        pyl_K3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_K.add(pyl_K3)
        
        self.FontDict[chh] = pylonarr_K; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |
        #  |
        #  |
        #  |
        #  |------
        
        chh = 'l'
        pylonarr_L = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_L1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_L.add(pyl_L1)
        
        vc5 = Vertex( .2+ pygap,    .0,  0)
        vc6 = Vertex( .2+ pygap,    .2,  0)
        vc7 = Vertex( .4,           .0,  0)
        vc8 = Vertex( .4,           .2,  0)
        pyl_L2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_L.add(pyl_L2)
        
        self.FontDict[chh] = pylonarr_L; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |\    /|
        #  | \  / |
        #  |  \/  |
        #  |      |
        #  |      |
        
        chh = 'm'
        pylonarr_M = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_M1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_M.add(pyl_M1)
        
        vc5 = Vertex( .2 + pygap,   1.2,  0)
        vc6 = Vertex( .2 + pygap,   .9,  0)
        vc7 = Vertex( .4,           .8,  0)
        vc8 = Vertex( .4,           .5,  0)
        pyl_M2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_M.add(pyl_M2)
        
        vc5 = Vertex( .4 + pygap,   .5,  0)
        vc6 = Vertex( .4 + pygap,   .8,  0)
        vc7 = Vertex( .6 - pygap,   .9,  0)
        vc8 = Vertex( .6 - pygap,   1.2,  0)
        pyl_M2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_M.add(pyl_M2)
        
        vc11 = Vertex( .6,  .0,  0)
        vc12 = Vertex( .8,  .0,  0)
        vc13 = Vertex( .6,  1.2,  0)
        vc14 = Vertex( .8,  1.2,  0)
        pyl_M3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_M.add(pyl_M3)
        
        self.FontDict[chh] = pylonarr_M; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |\    |
        #  | \   |
        #  |  \  |
        #  |   \ |
        #  |    \|
        
        chh = 'n'
        pylonarr_N = Shapearr()
        
        vc1 = Vertex( .0,  .0,  0)
        vc2 = Vertex( .2,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_N1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_N.add(pyl_N1)
        
        vc5 = Vertex( .2 + pygap,   1.2,  0)
        vc6 = Vertex( .2 + pygap,   .8,  0)
        vc7 = Vertex( .5,           .4,  0)
        vc8 = Vertex( .5,           .0,  0)
        pyl_N2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_N.add(pyl_N2)
        
        vc11 = Vertex( .5+ pygap,  .0,  0)
        vc12 = Vertex( .7,  .0,  0)
        vc13 = Vertex( .5+ pygap,  1.2,  0)
        vc14 = Vertex( .7,  1.2,  0)
        pyl_N3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_N.add(pyl_N3)
        
        self.FontDict[chh] = pylonarr_N; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----\
        #  |    |
        #  |    |
        #  \----/
        
        chh = 'o'
        pylonarr_O = Shapearr()
        
        vc1 = Vertex( .0,  .2 + pygap,  0)
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_O1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_O.add(pyl_O1)
        
        vc5 = Vertex( .0 + pygap,  .2,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .2 + pygap,  .2,  0)
        vc8 = Vertex( .0,   .2,  0)
        pyl_O2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_O.add(pyl_O2)
        
        vc11 = Vertex( .2 + pygap,  .2,  0)
        vc12 = Vertex( .2 + pygap,  0,  0)
        vc13 = Vertex( .5,  .2,  0)
        vc14 = Vertex( .5,  0,  0)
        pyl_O3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_O.add(pyl_O3)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_O4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_O.add(pyl_O4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_O5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_O.add(pyl_O5)
        
        vb11 = Vertex( .5,  1.,  0)
        vb12 = Vertex( .7,  1.,  0)
        vb13 = Vertex( .5,  .2 +  pygap,  0)
        vb14 = Vertex( .7,  .2 + pygap,  0)
        pyl_O4 = Pylon(vb11, vb12, vb13, vb14); pylonarr_O.add(pyl_O4)
        
        vb11 = Vertex( .5,  .2,  0)
        vb12 = Vertex( .7,  .2,  0)
        vb13 = Vertex( .5 +  pygap,  .0,  0)
        vb14 = Vertex( .5 +  pygap,  .0,  0)
        pyl_O8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_O.add(pyl_O8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 , 0)
        vb12 = Vertex( .5 +  pygap,  1.2,  0)
        vb13 = Vertex( .5,  1.0,  0)
        vb14 = Vertex( .7,  1.0,  0)
        pyl_O9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_O.add(pyl_O9)
        
        self.FontDict[chh] = pylonarr_O; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----\
        #  |    |
        #  |----/
        #  |
        #  |
        
        chh = 'p'
        pylonarr_P = Shapearr()
        
        vc1 = Vertex( .0,  .0 + pygap,  0)
        vc2 = Vertex( .2,  .0 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_P1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_P.add(pyl_P1)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_P4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_P.add(pyl_P4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_P5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_P.add(pyl_P5)
        
        vb11 = Vertex( .5,  1.,  0)
        vb12 = Vertex( .7,  1.,  0)
        vb13 = Vertex( .5,  .6 +  pygap,  0)
        vb14 = Vertex( .7,  .6 + pygap,  0)
        pyl_P6 = Pylon(vb11, vb12, vb13, vb14); pylonarr_P.add(pyl_P6)
        
        vb11 = Vertex( .5,  .6,  0)
        vb12 = Vertex( .7,  .6,  0)
        vb13 = Vertex( .5 +  pygap,  .4,  0)
        vb14 = Vertex( .5 +  pygap,  .4,  0)
        pyl_P8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_P.add(pyl_P8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 , 0)
        vb12 = Vertex( .5 +  pygap,  1.2,  0)
        vb13 = Vertex( .5,  1.0,  0)
        vb14 = Vertex( .7,  1.0,  0)
        pyl_P9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_P.add(pyl_P9)
        
        vc11 = Vertex( .2 + pygap,  .6,  0)
        vc12 = Vertex( .2 + pygap,  .4,  0)
        vc13 = Vertex( .5,          .6,  0)
        vc14 = Vertex( .5,          .4,  0)
        pyl_P3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_P.add(pyl_P3)
        
        self.FontDict[chh] = pylonarr_P; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----\
        #  |    |
        #  |    |
        #  \----/
        #       \
        
        chh = 'q'
        pylonarr_Q = Shapearr()
        
        vc1 = Vertex( .0,  .4 + pygap,  0)
        vc2 = Vertex( .2,  .4 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_Q1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_Q.add(pyl_Q1)
        
        vc5 = Vertex( .0 + pygap,   .4,  0)
        vc6 = Vertex( .2,           .2,  0)
        vc7 = Vertex( .2 + pygap,   .4,  0)
        vc8 = Vertex( .0,           .4,  0)
        pyl_Q2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_Q.add(pyl_Q2)
        
        vc11 = Vertex( .2 + pygap,  .4,  0)
        vc12 = Vertex( .2 + pygap, .2,  0)
        vc13 = Vertex( .5,  .4,  0)
        vc14 = Vertex( .5,  .2,  0)
        pyl_Q3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_Q.add(pyl_Q3)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_Q4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_Q.add(pyl_Q4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_Q5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_Q.add(pyl_Q5)
        
        vb11 = Vertex( .5,  1.,  0)
        vb12 = Vertex( .7,  1.,  0)
        vb13 = Vertex( .5,  .4 +  pygap,  0)
        vb14 = Vertex( .7,  .4 + pygap,  0)
        pyl_Q6 = Pylon(vb11, vb12, vb13, vb14); pylonarr_Q.add(pyl_Q6)
        
        vb11 = Vertex( .5,  .4,  0)
        vb12 = Vertex( .7,  .4,  0)
        vb13 = Vertex( .5 +  pygap,  .2,  0)
        vb14 = Vertex( .5 +  pygap,  .2,  0)
        pyl_Q8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_Q.add(pyl_Q8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 , 0)
        vb12 = Vertex( .5 +  pygap,  1.2,  0)
        vb13 = Vertex( .5,  1.0 - pygap,  0)
        vb14 = Vertex( .7,  1.0  - pygap, 0)
        pyl_Q9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_Q.add(pyl_Q9)
        
        vb11 = Vertex( .3 +  pygap,  .2 , 0)
        vb12 = Vertex( .5 +  pygap,  .2,  0)
        vb13 = Vertex( .5,  .0 - pygap,  0)
        vb14 = Vertex( .7,  .0  - pygap, 0)
        pyl_Q7 = Pylon(vb11, vb12, vb13, vb14); pylonarr_Q.add(pyl_Q7)
        
        self.FontDict[chh] = pylonarr_Q; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /----\
        #  |    |
        #  |----/
        #  |  \
        #  |   \
        
        chh = 'r'
        pylonarr_R = Shapearr()
        
        vc1 = Vertex( .0,  .0 + pygap,  0)
        vc2 = Vertex( .2,  .0 + pygap,  0)
        vc3 = Vertex( .0,  1.,  0)
        vc4 = Vertex( .2,  1.,  0)
        pyl_R1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_R.add(pyl_R1)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2,  1.2 +  pygap,  0)
        vc14 = Vertex( .2,  1. + pygap,  0)
        pyl_R4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_R.add(pyl_R4)
        
        vc11 = Vertex( .2+ pygap,  1.2,  0)
        vc12 = Vertex( .2+ pygap,  1.,  0)
        vc13 = Vertex( .5,  1.2,  0)
        vc14 = Vertex( .5,  1.,  0)
        pyl_R5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_R.add(pyl_R5)
        
        vb11 = Vertex( .5,  1.,  0)
        vb12 = Vertex( .7,  1.,  0)
        vb13 = Vertex( .5,  .6 +  pygap,  0)
        vb14 = Vertex( .7,  .6 + pygap,  0)
        pyl_R6 = Pylon(vb11, vb12, vb13, vb14); pylonarr_R.add(pyl_R6)
        
        vb11 = Vertex( .5,  .6,  0)
        vb12 = Vertex( .7,  .6,  0)
        vb13 = Vertex( .5 +  pygap,  .4,  0)
        vb14 = Vertex( .5 +  pygap,  .4,  0)
        pyl_R8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_R.add(pyl_R8)
        
        vb11 = Vertex( .5 +  pygap,  1.2 , 0)
        vb12 = Vertex( .5 +  pygap,  1.2,  0)
        vb13 = Vertex( .5,  1.0,  0)
        vb14 = Vertex( .7,  1.0,  0)
        pyl_R9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_R.add(pyl_R9)
        
        vc11 = Vertex( .2 + pygap,  .6,  0)
        vc12 = Vertex( .2 + pygap,  .4,  0)
        vc13 = Vertex( .5,          .6,  0)
        vc14 = Vertex( .5,          .4,  0)
        pyl_R3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_R.add(pyl_R3)
        
        vc11 = Vertex( .3 + pygap,  .4,  0)
        vc12 = Vertex( .5 + pygap,  .0,  0)
        vc13 = Vertex( .5,          .4,  0)
        vc14 = Vertex( .7,          .0,  0)
        pyl_R3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_R.add(pyl_R3)
        
        self.FontDict[chh] = pylonarr_R; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  /-----
        #  |    
        #  \----\
        #       |
        #  -----/
        
        chh = 's'
        pylonarr_S = Shapearr()
        
        vc1 = Vertex( .0,  .7,  0)
        vc2 = Vertex( .2,  .7,  0)
        vc3 = Vertex( .0,  1.- pygap,  0)
        vc4 = Vertex( .2,  1.- pygap,  0)
        pyl_S1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_S.add(pyl_S1)
        
        vc11 = Vertex( .0 + pygap,  .2,  0)
        vc12 = Vertex( .0 + pygap,  0,  0)
        vc13 = Vertex( .4,  .2,  0)
        vc14 = Vertex( .4,  0,  0)
        pyl_S3 = Pylon(vc11, vc12, vc13, vc14); pylonarr_S.add(pyl_S3)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .0,  1,  0)
        vc13 = Vertex( .2 -  pygap,  1.2,  0)
        vc14 = Vertex( .2 -  pygap,  1.,  0)
        pyl_S4 = Pylon(vc11, vc12, vc13, vc14); pylonarr_S.add(pyl_S4)
        
        vc11 = Vertex( .2,  1.2,  0)
        vc12 = Vertex( .2,  1.,  0)
        vc13 = Vertex( .6,  1.2,  0)
        vc14 = Vertex( .6,  1.,  0)
        pyl_S5 = Pylon(vc11, vc12, vc13, vc14); pylonarr_S.add(pyl_S5)
        
        vb11 = Vertex( .4,  .5-  pygap,  0)
        vb12 = Vertex( .6,  .5-  pygap,  0)
        vb13 = Vertex( .4,  .2+  pygap,  0)
        vb14 = Vertex( .6,  .2+  pygap,  0)
        pyl_S6 = Pylon(vb11, vb12, vb13, vb14); pylonarr_S.add(pyl_S6)
        
        vb11 = Vertex( .6,    .5,  0)
        vb12 = Vertex( .4 + pygap,    .7,  0)
        vb13 = Vertex( .4+  pygap,    .5,  0)
        vb14 = Vertex( .4+  pygap,    .7,  0)
        pyl_S7 = Pylon(vb11, vb12, vb13, vb14); pylonarr_S.add(pyl_S7)
        
        vb11 = Vertex( .4 + pygap,  .2,  0)
        vb12 = Vertex( .6,  .2,  0)
        vb13 = Vertex( .4 +  pygap,  .0,  0)
        vb14 = Vertex( .4 ,  .0,  0)
        pyl_S8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_S.add(pyl_S8)
        
        vb11 = Vertex( .2,    .5,  0)
        vb12 = Vertex( .2,    .5,  0)
        vb13 = Vertex( .0,    .7-  pygap,  0)
        vb14 = Vertex( .2,    .7-  pygap,  0)
        pyl_S9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_S.add(pyl_S9)
        
        vc11 = Vertex( .4,   .5,  0)
        vc12 = Vertex( .4 ,  .7,  0)
        vc13 = Vertex( .2 + pygap,  .5,  0)
        vc14 = Vertex( .2 + pygap,  .7,  0)
        pyl_S2 = Pylon(vc11, vc12, vc13, vc14); pylonarr_S.add(pyl_S2)
        
        self.FontDict[chh] = pylonarr_S; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #     ------
        #       |
        #       |
        #       |
        #  
        
        chh = 't'
        pylonarr_T = Shapearr()
        
        vc1 = Vertex( .2,  .0,  0)
        vc2 = Vertex( .4,  .0,  0)
        vc3 = Vertex( .2,  1. - pygap,  0)
        vc4 = Vertex( .4,  1. - pygap,  0)
        pyl_T1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_T.add(pyl_T1)
        
        vc5 = Vertex( .0,    1,  0)
        vc6 = Vertex( .0,    1.2,  0)
        vc7 = Vertex( .6,           1,  0)
        vc8 = Vertex( .6,           1.2,  0)
        pyl_T2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_T.add(pyl_T2)
        
        self.FontDict[chh] = pylonarr_T; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  |   |
        #  |   |
        #  |   |
        #  \---/
        
        chh = 'u'
        pylonarr_U = Shapearr()
        
        vc1 = Vertex( .0,  .2+ pygap,  0)
        vc2 = Vertex( .2,  .2+ pygap,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_U1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_U.add(pyl_U1)
        
        vc5 = Vertex( .2,   .0,  0)
        vc6 = Vertex( .2,   .0,  0)
        vc7 = Vertex( .0,   .2,  0)
        vc8 = Vertex( .2,   .2,  0)
        pyl_U2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_U.add(pyl_U2)
        
        vb11 = Vertex( .4,  1.2,  0)
        vb12 = Vertex( .6,  1.2,  0)
        vb13 = Vertex( .4,  .2 +  pygap,  0)
        vb14 = Vertex( .6,  .2 + pygap,  0)
        pyl_U4 = Pylon(vb11, vb12, vb13, vb14); pylonarr_U.add(pyl_U4)
        
        vb11 = Vertex( .4,  .2,  0)
        vb12 = Vertex( .6,  .2,  0)
        vb13 = Vertex( .4,  .0,  0)
        vb14 = Vertex( .4,  .0,  0)
        pyl_U8 = Pylon(vb11, vb12, vb13, vb14); pylonarr_U.add(pyl_U8)
        
        vb11 = Vertex( .4 -  pygap,  .2 ,  0)
        vb12 = Vertex( .2 +  pygap,  .2,  0)
        vb13 = Vertex( .4 -  pygap,  .0,  0)
        vb14 = Vertex( .2 +  pygap,  .0,  0)
        pyl_U9 = Pylon(vb11, vb12, vb13, vb14); pylonarr_U.add(pyl_U9)
        
        self.FontDict[chh] = pylonarr_U; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  \      /
        #   \    /
        #    \  /
        #     \/
        # 
        
        chh = 'v'
        pylonarr_V = Shapearr()
        
        vc1 = Vertex( .2,  .0,  0)
        vc2 = Vertex( .35,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_V1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_V.add(pyl_V1)
        
        vc5 = Vertex( .2,    .0,  0)
        vc6 = Vertex( .35,    .0,  0)
        vc7 = Vertex( .4,    1.2,  0)
        vc8 = Vertex( .6,    1.2,  0)
        pyl_V2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_V.add(pyl_V2)
        
        self.FontDict[chh] = pylonarr_V; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        
        # ------------------------------------------------------------------------
        #  \          /
        #   \        /
        #    \  /\  /
        #     \/  \/
        # 
        
        chh = 'w'
        pylonarr_W = Shapearr()
        
        vc1 = Vertex( .2,  .0,  0)
        vc2 = Vertex( .35,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_W1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_W.add(pyl_W1)
        
        vc5 = Vertex( .2,    .0,  0)
        vc6 = Vertex( .35,    .0,  0)
        vc7 = Vertex( .35,    .6,  0)
        vc8 = Vertex( .5,    .6,  0)
        pyl_W2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_W.add(pyl_W2)
        
        vc1 = Vertex( .55,   .0,  0)
        vc2 = Vertex( .7 ,   .0,  0)
        vc3 = Vertex( .35,   .6,  0)
        vc4 = Vertex( .5,    .6,  0)
        pyl_W3 = Pylon(vc1, vc2, vc3, vc4); pylonarr_W.add(pyl_W3)
        
        vc5 = Vertex( .55,    .0,  0)
        vc6 = Vertex( .7,     .0,  0)
        vc7 = Vertex( .7,     1.2,  0)
        vc8 = Vertex( .9,     1.2,  0)
        pyl_W4 = Pylon(vc5, vc6, vc7, vc8); pylonarr_W.add(pyl_W4)
        
        self.FontDict[chh] = pylonarr_W; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  \   /
        #   \ /  
        #   / \ 
        #  /   \
        # 
        chh = 'x'
        pylonarr_X = Shapearr()
        
        vc1 = Vertex( .4,  .0,  0)
        vc2 = Vertex( .6,  .0,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_X1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_X.add(pyl_X1)
        
        vc5 = Vertex( .0,    .0,  0)
        vc6 = Vertex( .2,    .0,  0)
        vc7 = Vertex( .4,    1.2,  0)
        vc8 = Vertex( .6,    1.2,  0)
        pyl_X2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_X.add(pyl_X2)
        
        self.FontDict[chh] = pylonarr_X; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #  \   /
        #   \ /  
        #    |
        #    |
        # 
        chh = 'y'
        pylonarr_Y = Shapearr()
        
        vc1 = Vertex( .3,  .5,  0)
        vc2 = Vertex( .5,  .5,  0)
        vc3 = Vertex( .0,  1.2,  0)
        vc4 = Vertex( .2,  1.2,  0)
        pyl_Y1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_Y.add(pyl_Y1)
        
        vc5 = Vertex( .3,    .5,  0)
        vc6 = Vertex( .5,    .5,  0)
        vc7 = Vertex( .6,    1.2,  0)
        vc8 = Vertex( .8,    1.2,  0)
        pyl_Y2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_Y.add(pyl_Y2)
        
        vc5 = Vertex( .3,    .5-pygap,  0)
        vc6 = Vertex( .5,    .5-pygap,  0)
        vc7 = Vertex( .3,    .0,  0)
        vc8 = Vertex( .5,    .0,  0)
        pyl_Y3 = Pylon(vc5, vc6, vc7, vc8); pylonarr_Y.add(pyl_Y3)
        
        self.FontDict[chh] = pylonarr_Y; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()
        
        # ------------------------------------------------------------------------
        #    ----/
        #       /
        #      /
        #     /----
        
        chh = 'z'
        pylonarr_Z = Shapearr()
        
        vc1 = Vertex( .0,  .2 + pygap,  0)
        vc2 = Vertex( .2,  .2 + pygap,  0)
        vc3 = Vertex( .3,  1.- pygap,  0)
        vc4 = Vertex( .5,  1.- pygap,  0)
        pyl_Z1 = Pylon(vc1, vc2, vc3, vc4); pylonarr_Z.add(pyl_Z1)
        
        vc5 = Vertex( .0,    .0,  0)
        vc6 = Vertex( .0,    .2,  0)
        vc7 = Vertex( .5,    .0,  0)
        vc8 = Vertex( .5,     .2,  0)
        pyl_Z2 = Pylon(vc5, vc6, vc7, vc8); pylonarr_Z.add(pyl_Z2)
        
        vc5 = Vertex( .0,    1.,  0)
        vc6 = Vertex( .0,    1.2,  0)
        vc7 = Vertex( .5,    1.0,  0)
        vc8 = Vertex( .5,    1.2,  0)
        pyl_Z3 = Pylon(vc5, vc6, vc7, vc8); pylonarr_Z.add(pyl_Z3)
        
        self.FontDict[chh] = pylonarr_Z; 
        self.FontSizeDict[chh] = self.FontDict[chh].getShapeWidth()




