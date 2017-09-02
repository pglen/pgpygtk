#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, helper routines
# 

import math, sys, rand

import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *

from pyfmshape import *
from pyfmfont import *

CUBE1   = 1; CUBE2   = 2; DONUT   = 3; TRIANG  = 4
TRIANG2 = 5; TRIANG3 = 6; STARS   = 7

triarr = Shapearr();

v1 = Vertex(-1, -1, 1)
v2 = Vertex( 1, -1, 1)
v3 = Vertex( 0,  1, 0)
tri_1 = Triangle(v1, v2, v3); triarr.add(tri_1)
 
v11 = Vertex( 0,  1, 0)
v12 = Vertex(-1, -1, -1)
v13 = Vertex( 1, -1, -1)
tri_2 = Triangle(v11, v12, v13); triarr.add(tri_2)

rectarr = Shapearr();
v21 = Vertex(-1,  1, 0)
v22 = Vertex( 1,  1, 0)
v23 = Vertex(-1,  0, 0)
v24 = Vertex( 1,  0, 0)

# ------------------------------------------------------------------------

def cubes(self):

    # Surface material properties.
    mat_ambient = [ 0.629412, 0.223529, 0.027451, 1.0 ]
    mat_diffuse = [ 0.980392, 0.568627, 0.113725, 1.0 ]
    mat_specular = [ 0.392157, 0.341176, 0.07843, 1.0 ]
    mat_shininess = 0.11794872 * 128.0

    glPushMatrix ()
    glTranslatef (-1.2, 1 - self.pos_y, 2.0)
    glRotatef (self.angle, 0.0, 1.0, 0.0)
    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    glLoadName(CUBE1)
    glPassThrough(CUBE1)
    gtk.gdkgl.draw_cube(True, 0.5)
    glPopMatrix ()

    glPushMatrix ()
    glTranslatef (-self.pos_x2, 1 - self.pos_y2, 2.0)
    glRotatef (self.angle, 0.0, 1.0, 0.0)
    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    #glPushName(CUBE2)
    glLoadName(CUBE2)
    glPassThrough(CUBE2)
    
    gtk.gdkgl.draw_cube(True, 0.5)
    glPopMatrix ()

# ------------------------------------------------------------------------

def randtri(self):
    
    glPushMatrix ()
    glRotatef (self.angle7, 0.0, 1.0, 0.0)
    
        # Surface material properties.
    if 0:
        mat_ambient = [ 0.629412, 0.223529, 0.027451, 1.0 ]
        mat_diffuse = [ 0.980392, 0.568627, 0.113725, 1.0 ]
        mat_specular = [ 0.392157, 0.341176, 0.07843, 1.0 ]
        mat_shininess = 0.11794872 * 128.0
        
        glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    
    glEnable(GL_COLOR_MATERIAL)
    
    glBegin(GL_TRIANGLES)
                         
    #glColor3f (frand(1), frand(1),  frand(1))
    
    for aa in range(2000):
        
        glColor3f (rand.frand(1), rand.frand(1),  rand.frand(1))
        
        #glColor3f(self.xrand.rand(), self.xrand.rand(), self.xrand.rand())
        
        xx = rand.frand2(2); yy = rand.frand2(2); zz = rand.frand2(2)
        #xx = self.xrand.s2(2)
        #yy = self.xrand.s2(2)
        #zz = self.xrand.s2(2)
        
        glVertex3f(xx, yy, zz)
        #glVertex3f(self.xrand.s3(xx, .1), self.xrand.s3(yy, .1), self.xrand.s3(zz, .1))
        #glVertex3f(self.xrand.s3(xx, .2), self.xrand.s3(yy, .2), self.xrand.s3(zz, .2))
        
        glVertex3f(rand.frand3(xx, .2), rand.frand3(yy, .1), rand.frand3(zz, .2))
        glVertex3f(rand.frand3(xx, .2), rand.frand3(yy, .2), rand.frand3(zz, .2))
        
    glEnd()
        
    glDisable(GL_COLOR_MATERIAL)
    glPopMatrix ()
    
# ------------------------------------------------------------------------

def stuff(self):

    glPushMatrix ()
    glRotatef (self.angle7, 0.0, 1.0, 0.0)
    glTranslatef (-2, 0, 0)
    print3Dstr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    #print3Dstr("VWXYZ")
    glPopMatrix ()

    #glPushMatrix ()
    #glRotatef (self.angle7, 0.0, 1.0, 0.0)
    #jello = "HELLO JELLO"
    #hhh = getCharHeight()
    #www = extent3Dstr(jello)
    #print www, hhh
    #glTranslatef (-www/2, -(hhh + hhh / 10), 0)
    #print3Dstr(jello)
    #glPopMatrix ()

# ------------------------------------------------------------------------

def text(self):

    glPushMatrix ()
    
    mat_ambient = [0.980392, 0.823529, 0.927451, 1.0 ]
    mat_diffuse = [ 0.980392, 0.568627, 0.113725, 1.0 ]
    mat_specular = [ 0.392157, 0.341176, 0.07843, 1.0 ]
    mat_shininess = 0.11794872 * 128.0

    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    
    glBegin(GL_LINE_STRIP)
    
    aa2 = 0; bb3 = 0; 
    aa3 = 0; bb3 = 0; 
    cnt = 0
    try:
        for aa, bb, cc, dd in self.arr:
            glVertex3f(aa, bb, cc)
            if cnt % 3 == 0 and cnt: 
                glEnd()
                mat_ambient = [dd , dd, 0.927451, 1.0 ]
                mat_diffuse = [ 0.980392, 0.568627, 0.113725, 1.0 ]
                mat_specular = [ 0.392157, 0.341176, 0.07843, 1.0 ]
                mat_shininess = 0.11794872 * 128.0
            
                glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
                glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
                glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
                glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
                
                glBegin(GL_TRIANGLES)
                glVertex3f(aa, bb, cc)
                glVertex3f(aa2, bb2, cc)
                glVertex3f(aa3, bb3, cc)
                glEnd()
                glBegin(GL_LINE_STRIP)
                
            if cnt % 3 == 1: 
                aa3 = aa; bb3 = bb
            if cnt % 3 == 2: 
                aa2 = aa; bb2 = bb
            cnt += 1
        
    except:
        print sys.exc_info()
        exit
        raise SystemExit
        
    finally:
        pass
        
    glEnd()
        
    glPopMatrix()

# ------------------------------------------------------------------------

def grid(self):

    glPushMatrix ()
    
    #mat_ambient = [ 0.929412, 0.923529, 0.927451, 1.0  ]
    mat_ambient = [ 0.229412, 0.223529, 0.227451, 1.0  ]
    mat_diffuse = [ 0.280392, 0.268627, 0.213725, 1.0 ]
    mat_specular = [ 0.392157, 0.341176, 0.07843, 1.0 ]
    mat_shininess = 0.11794872 * 128.0
    
    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)

    glColor3f(.5, .5, .5)
    glBegin(GL_LINES)
    
    glVertex3f(-2, .0,  .01)
    glVertex3f( 2,  0,  .01)
    
    glVertex3f(.0, -2,  .01)
    glVertex3f(.0,  2,  .01)
    
    glEnd()
    
    mat_ambient = [ 0.229412, 0.223529, 0.227451, 1.0  ]
    mat_diffuse = [ 0.580392, 0.568627, 0.113725, 1.0 ]
    mat_shininess = 0.11794872 * 12.0
    
    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)

    #glColor3f(.5, .5, .5)
    glBegin(GL_LINES)
    
    step = 10
    www = 0.03
    for aa in range (4 * step + 1):
        glVertex3f(-2 + float(aa) / step,  www,  .01)
        glVertex3f(-2 + float(aa) / step,  -www,  .01)
    for aa in range (4 * step + 1):
        glVertex3f(www, -2 + float(aa) / step,   .01)
        glVertex3f(-www,-2 + float(aa) / step,    .01)
        
    glEnd()
    
    glPopMatrix()

# ------------------------------------------------------------------------

def stars(self):

    glPushMatrix ()
    
    mat_ambient = [ 0.929412, 0.923529, 0.927451, 1.0  ]
    mat_diffuse = [ 0.980392, 0.568627, 0.113725, 1.0 ]
    mat_specular = [ 0.392157, 0.341176, 0.07843, 1.0 ]
    mat_shininess = 0.11794872 * 128.0

    #glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    #glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    #glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    #glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
        
    glLoadName(STARS)
    glPassThrough(STARS)
    
    glPointSize(2)
    glBegin (GL_POINTS);
    for xx, yy, zz, pp in self.stars:
        glVertex3f (xx, yy, zz)
    glEnd ();
        
    mat_ambient = [ 0.929412, 0.523529, 0.527451, 1.0 ]
    mat_diffuse = [ 0.980392, 0.568627, 0.113725, 1.0 ]
    mat_specular = [ 0.392157, 0.341176, 0.07843, 1.0 ]
    mat_shininess = 0.11794872 * 128.0

    #glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    #glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    #glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    #glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    
    glPointSize(4)
    glEnable(GL_COLOR_MATERIAL)
    
    #print self.starcol
    
    cnt = 0
    glBegin (GL_POINTS);
    for xx, yy, zz, pp in self.bigstars:
        if cnt % 2:        
            glColor3f (self.starcol, self.starcol, self.starcol)
        else: 
            glColor3f (2- self.starcol, 2-self.starcol, 2-self.starcol)
        glVertex3f (xx, yy, zz)
        cnt += 1
    glEnd ();
    
    # Leave as 
    glColor3f (0.5, 0.5, 0.5)
        
    glDisable(GL_COLOR_MATERIAL)
    
    glPopMatrix ()

# ------------------------------------------------------------------------

def donut(self):

    glPushMatrix ()
    
    glTranslatef (self.pos_x, self.pos_y, 0.0)
    glRotatef (self.angle2, 0.0, 1.0, 0.0)
    
    # Surface material properties.
    mat_ambient = [ 0.529412, 0.523529, 0.127451, 1.0 ]
    mat_diffuse = [ 0.780392, 0.568627, 0.213725, 1.0 ]
    mat_specular = [ 0.992157, 0.941176, 0.907843, 1.0 ]
    mat_shininess = 0.21794872 * 128.0

    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    
    #glPushName(DONUT)
    glLoadName(DONUT)
    glPassThrough(DONUT)
    
    gtk.gdkgl.draw_torus (True, 0.3, 0.6, 30, 30)

    #gtk.gdkgl.draw_cone (True, 0.5, 0.5, 30, 30)
    #gtk.gdkgl.draw_sphere (True, 0.5, 30, 30)
    #gtk.gdkgl.draw_cube (True, 0.5)
    #gtk.gdkgl.draw_tetrahedron(True)
    #gtk.gdkgl.draw_octahedron(True)
    #gtk.gdkgl.draw_dodecahedron(True)
    #gtk.gdkgl.draw_icosahedron(True)
    #gtk.gdkgl.draw_icosahedron(True)
    
    glPopMatrix ()
    
def pvertex(vx):
    return "%.f:%.f:%.f" % \
        (vx.vertex[0], vx.vertex[1], vx.vertex[2])









        







