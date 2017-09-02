#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, helper routines
# 

import math, sys
#import rand

#import pygtk;  pygtk.require('2.0')
#import gtk
#import gobject

import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *

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
    gtk.gdkgl.draw_cube(True, 0.5)
    glPopMatrix ()

    glPushMatrix ()
    glTranslatef (-self.pos_x2, 1 - self.pos_y2, 2.0)
    glRotatef (self.angle, 0.0, 1.0, 0.0)
    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    gtk.gdkgl.draw_cube(True, 0.5)
    glPopMatrix ()


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
        
        glColor3f (frand(1), frand(1),  frand(1))
        
        #glColor3f(self.xrand.rand(), self.xrand.rand(), self.xrand.rand())
        
        xx = frand2(2); yy = frand2(2); zz = frand2(2)
        #xx = self.xrand.s2(2)
        #yy = self.xrand.s2(2)
        #zz = self.xrand.s2(2)
        
        glVertex3f(xx, yy, zz)
        #glVertex3f(self.xrand.s3(xx, .1), self.xrand.s3(yy, .1), self.xrand.s3(zz, .1))
        #glVertex3f(self.xrand.s3(xx, .2), self.xrand.s3(yy, .2), self.xrand.s3(zz, .2))
        
        glVertex3f(frand3(xx, .2), frand3(yy, .1), frand3(zz, .2))
        glVertex3f(frand3(xx, .2), frand3(yy, .2), frand3(zz, .2))
        
    glEnd()
        
    glDisable(GL_COLOR_MATERIAL)
    glPopMatrix ()
    
    
def stuff(self):

    glPushMatrix ()

    glRotatef (self.angle7, 0.0, 1.0, 0.0)
    
    mat_ambient = [ 0.429412, 0.223529, 0.227451, 1.0 ]
    mat_diffuse = [ 0.980392, 0.268627, 0.113725, 1.0 ]
    mat_specular = [ 0.992157, 0.0341176, 0.07843, 1.0 ]
    mat_shininess = 0.11794872 * 128.0
    #glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    
    glBegin(GL_TRIANGLES)
    
    glVertex3f( 0,  1, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f( 1, -1, 1)
    
    glEnd()
    
    #mat_ambient2 = [ 0.029412, 0.223529, 0.427451, 1.0 ]
    #mat_diffuse2 = [ 0.080392, 0.268627, 0.413725, 1.0 ]
    #mat_specular2 = [ 0.092157, 0.0341176, 0.87843, 1.0 ]
    #mat_shininess2 = 0.11794872 * 128.0
    #glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient2)
    #glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse2)
    #glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular2)
    #glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess2)
   
    glEnable(GL_COLOR_MATERIAL)
    
    glBegin(GL_TRIANGLES)
    
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f( 0,  1, 0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1, -1, -1)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f( 1, -1, -1)
    
    glEnd()
    
    glDisable(GL_COLOR_MATERIAL)
    
    glPopMatrix ()


def text(self):

    glPushMatrix ()
    
    glRotatef (self.angle, 0.0, 1.0, 0.0)
    
    mat_ambient = [ 0.629412, 0.823529, 0.927451, 1.0 ]
    mat_diffuse = [ 0.980392, 0.568627, 0.113725, 1.0 ]
    mat_specular = [ 0.392157, 0.341176, 0.07843, 1.0 ]
    mat_shininess = 0.11794872 * 128.0

    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    
    glColor3f(0.0, 0.0, 0.0)
    
    '''for ii in range(2,-3,-1):
        #glRasterPos2f(10.0, 0.5 * self.height + ii * self.fontHeight, 0)
        glRasterPos2f(0, 0, 0)
        # ASCII(32) --> ' ', ASCII(90) --> 'Z'
        for jj in range(32, 91):
            glCallList(self.fontListBase+jj)
        pass
    '''    
        
    '''    
    try:
        
        glBegin(GL_TRIANGLES)
        
        glIndexi(self.RED.pixel)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0, 1, 1)
        
        glIndexi(self.GREEN.pixel)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(1, 1, 1)
        
        glIndexi(self.GREEN.pixel)
        glColor3f(0.0, 1.0, 0.0)
        #glVertex3f(-1, -1, 0)
        glVertex3f(random.gauss(1, .3), random.gauss(1, .3), random.gauss(1, .3))
        
        #glColor3f(0.0, 0.0, 1.0)
        #glVertex3f(1, -1, 1)
        #glVertex3f(1, -2, 1.2)
        #glVertex3f(1, -1.3, 1.4)
        
    except:
        print sys.exc_info()
        raise SystemExit
        
    finally:
        glEnd()
    '''
        
    glPopMatrix()


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




