#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, triangle, rect, pylon routines
# 

import sys

import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *
from copy import copy

__gl_id = 0

# Return next ID. Used on hit testing the pylon.
def newid():
    global __gl_id
    __gl_id = __gl_id + 1
    return __gl_id

# Give some defaults  (dark gray)
ambient = [ 0.229412, 0.223529, 0.227451, 1.0 ]
diffuse = [ 0.280392, 0.268627, 0.213725, 1.0 ]
specular = [ 0.292157, 0.2341176, 0.27843, 1.0 ]
shininess = 0.11794872 * 128.0

class Vertex():
    def __init__(self, x, y, z):
        self._x = x; self._y = y; self._z = z
          
# ------------------------------------------------------------------------
# The instance is tagged with ID, which can be used for hit match
# on interactive usage.

class   Shapearr():

    def __init__(self):
        self.arr = []; self.id = newid()
        self.rot = None; self.trans = None
        
        self.ambient = [ 0.229412, 0.223529, 0.227451, 1.0 ]
        self.diffuse = [ 0.480392, 0.468627, 0.413725, 1.0 ]
        self.specular = [ 0.892157, 0.841176, 0.8843, 1.0 ]
        self.shininess = 0.11794872 * 50.0

    def add(self, tri):
        self.arr.append(tri)    
    
    def copycol(self, tri):
        tri.ambient   = copy(self.ambient)
        tri.diffuse   = copy(self.diffuse)
        tri.specular  = copy(self.specular) 
        tri.shininess = copy(self.shininess) 
        
    def getShapeWidth(self):
        ret = 0
        for aa in self.arr:
            for bb in aa.verts:
                if bb._x > ret:
                    ret = bb._x
        return ret
        
    def getShapeHeight(self):
        ret = 0
        for aa in self.arr:
            for bb in aa.verts:
                if bb._y > ret:
                    ret = bb._y
        return ret

    def draw(self):
    
        glPushMatrix ()
        
        glPassThrough(self.id); glLoadName(self.id)
        #glEnable(GL_CULL_FACE); glFrontFace(GL_CCW)
        
        if self.rot:
            glRotatef (self.rot, 0.0, 1.0, 0.0)
        if self.trans:           
            glTranslatef (self.trans._x, self.trans._y, self.trans._z)
    
        glMaterialfv (GL_FRONT, GL_AMBIENT, self.ambient)
        glMaterialfv (GL_FRONT, GL_DIFFUSE, self.diffuse)
        glMaterialfv (GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialf (GL_FRONT, GL_SHININESS, self.shininess)
     
        try:
            glBegin(GL_TRIANGLES)
            for aa in self.arr:
                aa.draw(True )
            glEnd()
        except:
            #print sys.exc_info()
            a,b,c = sys.exc_info(); print sys.excepthook(a,b,c)
            #exit(1)
            glPopMatrix ()
            return
            
        glPopMatrix ()

class   Triangle():

    def __init__(self, v1, v2, v3):
        self._v1 = v1; self._v2 = v2; self._v3 = v3
        self.ambient = [ 0.429412, 0.223529, 0.227451, 1.0 ]
        self.diffuse = [ 0.980392, 0.268627, 0.113725, 1.0 ]
        self.specular = [ 0.992157, 0.0341176, 0.07843, 1.0 ]
        self.shininess = 0.11794872 * 128.0

    def draw(self, drawcolor = False ):
        if drawcolor:
            glMaterialfv (GL_FRONT, GL_AMBIENT, self.ambient)
            glMaterialfv (GL_FRONT, GL_DIFFUSE, self.diffuse)
            glMaterialfv (GL_FRONT, GL_SPECULAR, self.specular)
            glMaterialf  (GL_FRONT, GL_SHININESS, self.shininess)
        
        glVertex3f(self._v1._x, self._v1._y, self._v1._z)
        glVertex3f(self._v2._x, self._v2._y, self._v2._z)
        glVertex3f(self._v3._x, self._v3._y, self._v3._z)

#  Draw a rectangle with two triangles. Need for speed.
#
#    v1  ------------------ v2
#        |                |
#        |                |
#    v3  ------------------ v4
#   
# Drawing order: V1, V2, V3 --- V3, v2, v4
#

class   Rect():

    def __init__(self, v1, v2, v3, v4):
        self._v1 = v1; self._v2 = v2
        self._v3 = v3; self._v4 = v4
        
        self.ambient = [ 0.929412, 0.223529, 0.227451, 1.0 ]
        self.diffuse = [ 0.480392, 0.268627, 0.113725, 1.0 ]
        self.specular = [ 0.392157, 0.0341176, 0.07843, 1.0 ]
        self.shininess = 0.11794872 * 128.0

    def draw(self, drawcolor = False ):
        
        if drawcolor:
            glMaterialfv (GL_FRONT, GL_AMBIENT, self.ambient)
            glMaterialfv (GL_FRONT, GL_DIFFUSE, self.diffuse)
            glMaterialfv (GL_FRONT, GL_SPECULAR, self.specular)
            glMaterialf (GL_FRONT, GL_SHININESS, self.shininess)

        glVertex3f(self._v1._x,  self._v1._y,  self._v1._z)
        glVertex3f(self._v2._x,  self._v2._y,  self._v2._z)
        glVertex3f(self._v3._x,  self._v3._y,  self._v3._z)

        glVertex3f(self._v3._x,  self._v3._y,  self._v3._z)
        glVertex3f(self._v2._x,  self._v2._y,  self._v2._z)
        glVertex3f(self._v4._x,  self._v4._y,  self._v4._z)

# ------------------------------------------------------------------------
# Draw a pylon with rectangles. Need for speed, so we draw with triangles
#
#  Drawing Method:
#
#       Upper rect 
#       Lower rect
#       Front face
#       Right face
#       Back face
#       Left face
#
#        v5  /------------------/  v6
#           / |                / |
#          /  /---------------/--/  v8
#         /  / v7            /  /
#        /  /           v2  /  /
#   v1  / -/---------------/  /
#        |/                | /
#   v3   -------------------/ v4
#                           

class   Pylon():

    def initvars(self):
        self.rects = []; self.verts = []
        self.rot = None; self.trans = None; self.scale = None
            
        self.ambient = [ 0.229412, 0.223529, 0.927451, 1.0 ]
        self.diffuse = [ 0.280392, 0.268627, 0.913725, 1.0 ]
        self.specular = [ 0.292157, 0.2341176, 0.27843, 1.0 ]
        self.shininess = 0.11794872 * 64.0

        self.ambient2 = [ 0.429412, 0.423529, 0.427451, 1.0 ]
        self.diffuse2 = [ 0.480392, 0.468627, 0.413725, 1.0 ]
        self.specular2 = [ 0.392157, 0.0341176, 0.07843, 1.0 ]
        self.shininess2 = 0.11794872 * 64.0
        
    def __init__(self, v1, v2, v3, v4, v5=None, v6=None, v7=None, v8=None):
    
        self.initvars()
        if v5 == None:
            self._v1 = copy(v1); self._v2 = copy(v2)
            self._v3 = copy(v3); self._v4 = copy(v4)
            self._v5 = copy(v1); self._v6 = copy(v2)
            self._v7 = copy(v3); self._v8 = copy(v4)
            
            self._v5._z += .1;  self._v6._z += .1
            self._v7._z += .1;  self._v8._z += .1
            
        else: 
            self._v1 = copy(v1); self._v2 = copy(v2)
            self._v3 = copy(v3); self._v4 = copy(v4)
            self._v5 = copy(v5); self._v6 = copy(v6)
            self._v7 = copy(v7); self._v8 = copy(v8)
            
        self.do_verts(); self.do_rect()

    def setdepth(self, dd):
        self._v5._z = dd;  self._v6._z = dd
        self._v7._z = dd;  self._v8._z = dd

    def  do_verts(self):  
        self.verts = []
        self.verts.append(self._v1)
        self.verts.append(self._v2)
        self.verts.append(self._v3)
        self.verts.append(self._v4)
        self.verts.append(self._v5)
        self.verts.append(self._v6)
        self.verts.append(self._v7)
        self.verts.append(self._v8)
        
    def do_rect(self):
        self.r1 = Rect(self._v1, self._v2, self._v3, self._v4)
        self.r2 = Rect(self._v5, self._v6, self._v7, self._v8)
        self.r3 = Rect(self._v3, self._v4, self._v7, self._v8)
        self.r4 = Rect(self._v4, self._v2, self._v8, self._v6)
        self.r5 = Rect(self._v1, self._v2, self._v5, self._v6)
        self.r6 = Rect(self._v3, self._v1, self._v7, self._v5)
        
        self.rects = []
        self.rects.append(self.r1)
        self.rects.append(self.r2)
        self.rects.append(self.r3)
        self.rects.append(self.r4)
        self.rects.append(self.r5)
        self.rects.append(self.r6)
      
    # Move in any direction
    def translate(self, xx, yy, zz = 0):
    
        self._v1._x += xx;          self._v2._x += xx;
        self._v3._x += xx;          self._v4._x += xx;
        self._v5._x += xx;          self._v6._x += xx;
        self._v7._x += xx;          self._v8._x += xx;
        self._v1._y += yy;          self._v2._y += yy;
        self._v3._y += yy;          self._v4._y += yy;
        self._v5._y += yy;          self._v6._y += yy;
        self._v7._y += yy;          self._v8._y += yy;
        self.do_verts(); self.do_rect()
    
    # Scale 
    def scalepylon(self, xx, yy, zz = 1):
    
        self._v1._x *= xx;          self._v2._x *= xx;
        self._v3._x *= xx;          self._v4._x *= xx;
        self._v5._x *= xx;          self._v6._x *= xx;
        self._v7._x *= xx;          self._v8._x *= xx;
        
        self._v1._y *= yy;          self._v2._y *= yy;
        self._v3._y *= yy;          self._v4._y *= yy;
        self._v5._y *= yy;          self._v6._y *= yy;
        self._v7._y *= yy;          self._v8._y *= yy;
        
        self._v1._z *= zz;          self._v2._z *= zz;
        self._v3._z *= zz;          self._v4._z *= zz;
        self._v5._z *= zz;          self._v6._z *= zz;
        self._v7._z *= zz;          self._v8._z *= zz;
        
        self.do_verts(); self.do_rect()
    
    # Create the illusion of bold font, fatten proportional to width 
    
    def   fatpylon(self, xx):
        
        self._v1._x *= xx;          self._v2._x *= xx;
        self._v3._x *= xx;          self._v4._x *= xx;
        self._v5._x *= xx;          self._v6._x *= xx;
        self._v7._x *= xx;          self._v8._x *= xx;
                                   
        self.do_verts(); self.do_rect()
        
    # Create the illusion of italic font, skew proportional to height
    
    def   skewpylon(self, ref, ss):
        
        self._v1._x = self._v1._x + (ss * self._v1._y / ref);
        self._v2._x = self._v2._x + (ss * self._v2._y / ref);
        self._v3._x = self._v3._x + (ss * self._v3._y / ref);
        self._v4._x = self._v4._x + (ss * self._v4._y / ref);
        self._v5._x = self._v5._x + (ss * self._v5._y / ref);
        self._v6._x = self._v6._x + (ss * self._v6._y / ref);
        self._v7._x = self._v7._x + (ss * self._v7._y / ref);
        self._v8._x = self._v8._x + (ss * self._v8._y / ref);
                                    
        self.do_verts(); self.do_rect()
    
    # Draw thyself            
    def draw(self, drawcolor = False ):

        # If rot/trans/scale needed, create new cycle
        if self.rot or self.trans or self.scale:
            glEnd()
            glPushMatrix ()
            if self.trans:           
                glTranslatef (self.trans._x, self.trans._y, self.trans._z)
            if self.rot:
                glRotatef (self.rot, 0.0, 0.0, 1.0)
            if self.scale:           
                glScalef (self.scale._x, self.scale._y, self.scale._z)
                
            glBegin(GL_TRIANGLES)
                    
        if drawcolor:
            glMaterialfv (GL_FRONT, GL_AMBIENT, self.ambient)
            glMaterialfv (GL_FRONT, GL_DIFFUSE, self.diffuse)
            glMaterialfv (GL_FRONT, GL_SPECULAR, self.specular)
            glMaterialf (GL_FRONT, GL_SHININESS, self.shininess)

        self.r1.draw()
        self.r2.draw()

        glMaterialfv (GL_FRONT, GL_AMBIENT, self.ambient2)
        glMaterialfv (GL_FRONT, GL_DIFFUSE, self.diffuse2)
        glMaterialfv (GL_FRONT, GL_SPECULAR, self.specular2)
        glMaterialf (GL_FRONT, GL_SHININESS, self.shininess2)

        self.r3.draw()
        self.r4.draw()
        self.r5.draw()
        self.r6.draw()
        
        # Create new draw cycle
        if self.rot or self.trans or self.scale:
            glEnd()
            glPopMatrix ()
            glBegin(GL_TRIANGLES)
           




