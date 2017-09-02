#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, helper routines
#

import math, sys, subprocess

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
        self.focus = False 
        self.myname = self2.nextname()

    def  addtext(self, txt):
        self.txtarr.append(txt)

    def setfocus(self, foc):
        self.focus = foc
    
    def  clear(self, txt):
        self.txtarr = []
               
    def draw(self, pos_y, angle):

        # If no text, disappear
        if len(self.txtarr) == 0:
            return
            
        glTranslatef (self.xpos, self.ypos - pos_y, self.zpos)
        glRotatef (angle, 0.0, 1.0, 0.0)

        glLoadName(self.myname)
        
        hsize = 0; vsize = 0
        for aa in self.txtarr:
            exten = self.font.extent3Dstr(aa)
            vsize += self.font.FontHeight  + self.font.linegap
            if exten[0] > hsize: hsize = exten[0]
          
        #print hsize, vsize
        x1 =   -  (self.font.FontHeight  + self.font.linegap)
        y1 =  2 * (self.font.FontHeight  + self.font.linegap)
        x2 =  hsize +  3 * (self.font.FontHeight  + self.font.linegap)
        y2 = - vsize    - 2 * (self.font.FontHeight  + self.font.linegap)
        
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
    
        #       y1
        #    -------- 
        # x1 |        | x2
        #    --------
        #       y2
        
        depth =  self.font.getdepth() * 2
        glBegin(GL_QUADS)
        
        # Background
        glVertex3f(x1,      y1,      0)#self.zpos - depth)
        glVertex3f(x2,      y1,      0)#self.zpos - depth)
        glVertex3f(x2,      y2,      0)#self.zpos - depth)
        glVertex3f(x1,      y2,      0)#self.zpos - depth)
                                     
        # Focus
        if self.focus:
            mat_ambient = [ 0.6, 0.6, 0.6, 1.0 ]
            glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
            
            yf = y1 + self.font.linegap
            glVertex3f(x1,      y1,      0 + depth)
            glVertex3f(x2,      y1,      0 + depth)
            glVertex3f(x2,      yf,      0 + depth)
            glVertex3f(x1,      yf,      0 + depth)
            
            yf = y2 - self.font.linegap
            glVertex3f(x1,      y2,      0 + depth)
            glVertex3f(x2,      y2,      0 + depth)
            glVertex3f(x2,      yf,      0 + depth)
            glVertex3f(x1,      yf,      0 + depth)
            
            xf = x1 - self.font.linegap
            glVertex3f(xf,      y1,      0 + depth)
            glVertex3f(x1,      y1,      0 + depth)
            glVertex3f(x1,      y2,      0 + depth)
            glVertex3f(xf,      y2,      0 + depth)
            xf = x2 + self.font.linegap
            glVertex3f(xf,      y1,      0 + depth)
            glVertex3f(x2,      y1,      0 + depth)
            glVertex3f(x2,      y2,      0 + depth)
            glVertex3f(xf,      y2,      0 + depth)
            
        mat_ambient = [ 0.3, 0.3, 0.3, 1.0 ]
        glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
        
        # Bar
        x12 = x2 -  self.font.FontHeight
        x11 = x12 -  self.font.FontHeight
        
        y12 = y2 +  self.font.FontHeight
        y11 = y1 -  self.font.FontHeight
        
        glVertex3f(x11,     y11,      0 + 0.01)
        glVertex3f(x12,     y11,      0 + 0.01)
        glVertex3f(x12,     y12,      0 + 0.01)
        glVertex3f(x11,     y12,      0 + 0.01)
        
        # Scroller
        x42 = x2 -  self.font.FontHeight
        x41 = x42 -  self.font.FontHeight
        
        mid = (y1 + y2) / 2 + self.font.FontHeight / 2
        y42 = mid
        y41 = mid -  self.font.FontHeight
        
        mat_ambient = [ 0.4, 0.4, 0.4, 1.0 ]
        glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
   
        glVertex3f(x41,     y41,      0 + 0.02)
        glVertex3f(x42,     y41,      0 + 0.02)
        glVertex3f(x42,     y42,      0 + 0.02)
        glVertex3f(x41,     y42,      0 + 0.02)
        
        glEnd()

        # Bar ends
        #   y21     y22
        # x21 \-----/ x22
        #      \   /    
        #       \ /
        #       y23
        #          x23 
           
        mat_ambient = [ 0.4, 0.4, 0.4, 1.0 ]
        glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
   
        x21 = x11;   x22 = x12
        y21 = y12;   y22 = y12
        y23 = y12 -  self.font.FontHeight
        x23 = x21 + self.font.FontHeight / 2

        glBegin(GL_TRIANGLES)
        glVertex3f(x21,     y21,     0 + 0.01) #self.zpos + 0.01)
        glVertex3f(x22,     y22,     0 + 0.01) #self.zpos + 0.01)
        glVertex3f(x23,     y23,     0 + 0.01) #self.zpos + 0.01)

        x31 = x11;   x32 = x12
        y31 = y11;   y32 = y11
        y33 = y11 +  self.font.FontHeight
        x33 = x21 + self.font.FontHeight / 2

        glVertex3f(x31,     y31,     0 + 0.01) #self.zpos + 0.01)
        glVertex3f(x32,     y32,     0 + 0.01) #self.zpos + 0.01)
        glVertex3f(x33,     y33,     0 + 0.01) #self.zpos + 0.01)
        glEnd()

        glLoadName(self.myname)
        
        hoffset = .0; offset = .0
        for aa in self.txtarr:
            
            glPushMatrix ()
            glTranslatef (hoffset, offset, 0 + 0.01)#self.zpos)
            self.font.print3Dstr(aa, self.myname)
            glPopMatrix ()
            
            exten = self.font.extent3Dstr(aa)
            offset -= self.font.FontHeight  + self.font.linegap
            
    def button(self, res, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if self.myname in res.names:
                #print  "Near", res.near, "Far", res.far, "Names", res.names, event.type
                self.focus = True 
            else: 
                self.focus = False
    
    def motion(self, event):
        #print "textpad motion", event
        pass







