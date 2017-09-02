#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, helper routines
#

import math, sys, rand, subprocess

import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *


# Text area for showing text

class   TextPad():

    def __init__(self, self2, font, xpos = 0, ypos = 0, zpos = 0):
        self.xpos = xpos;  self.ypos = ypos; self.zpos = zpos
        self.font = font
        self.self2 = self2
        self.txtarr = []

    def  addtext(self, txt):
        self.txtarr.append(txt)

    def  clear(self, txt):
        self.txtarr = []
               
    def draw(self, pos_y, angle):

        if len(self.txtarr) == 0:
            return
            
        glTranslatef (self.xpos, self.ypos - pos_y, self.zpos)
        glRotatef (angle, 0.0, 1.0, 0.0)

        hsize = 0; vsize = 0
        for aa in self.txtarr:
            exten = self.font.extent3Dstr(aa)
            vsize += self.font.FontHeight  + self.font.linegap
            if exten[0] > hsize: hsize = exten[0]
          
        #print hsize, vsize
        ur = 2 * self.font.FontHeight  + self.font.linegap
        lr = -vsize   # - (self.font.FontHeight  + self.font.linegap)
        ll = hsize + self.font.FontHeight
        ul =  -self.font.FontHeight
        
        # Surface material properties.
        mat_ambient = [ 0.09, 0.09, 0.09, 1.0 ]
        mat_diffuse = [ 0.0, 0.0, 0.0, 1.0 ]
        mat_specular = [ 0.0, 0.0, 0.0, 1.0 ]
        mat_shininess = 0.01794872 
        
        #glEnable(GL_COLOR_MATERIAL)
        glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
    
        depth =  self.font.getdepth() * 2
        glBegin(GL_QUADS)
        glVertex3f(ul,      ur,      self.zpos - depth)
        glVertex3f(ul,      lr,      self.zpos - depth)
        glVertex3f( ll,     lr,      self.zpos - depth)
        glVertex3f( ll,     ur,      self.zpos - depth)
        glEnd()

        hoffset = .0; offset = .0
        for aa in self.txtarr:
            
            glPushMatrix ()
            glTranslatef (hoffset, offset, self.zpos)
            self.font.print3Dstr(aa)
            glPopMatrix ()
            
            exten = self.font.extent3Dstr(aa)
            offset -= self.font.FontHeight  + self.font.linegap
            
        




