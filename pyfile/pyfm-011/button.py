#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, helper routines
#

import math, sys, subprocess

#import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *

#from gtk.gtkgl.apputils import *
from OpenGL.GL.ARB.multitexture import *


class Button():

    def __init__(self, self2, font, txt, command, xpos = 0, ypos = 0, zpos = 0):
        self.command = command
        self.self2 = self2
        self.txt = txt; 
        self.xpos = xpos;  self.ypos = ypos; self.zpos = zpos
        self.myname = self2.nextname()
        self.focus = False 
        self.font = font
        self.offset = 0.


    def draw(self, pos_y, angle):

        depth = self.font.getdepth()
        glLoadName(self.myname)
        
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
    
        exten = self.font.extent3Dstr(self.txt)
        
        x1 =  - (self.font.FontHeight  + self.font.linegap)
        y1 =  2 * (self.font.FontHeight  + self.font.linegap)
        x2 =   exten[0] +   (self.font.FontHeight  + self.font.linegap)
        y2 = - exten[1] 
        
        glPushMatrix ()
        glTranslatef (self.xpos, self.ypos - pos_y, self.zpos)
        glRotatef (angle, 0.0, 1.0, 0.0)
      
        mat_ambient = [ 0.6, 0.6, 0.6, 1.0 ]
        glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
        
        glBegin(GL_QUADS)
        glVertex3f(x1,      y1 ,     2*depth)
        glVertex3f(x2,      y1,      2*depth)
        glVertex3f(x2,      y2,      2*depth)
        glVertex3f(x1,      y2,      2*depth)
        glEnd()
        
        glPopMatrix ()
        
        glPushMatrix ()
        #glTranslatef (self.xpos + self.offset, self.ypos - pos_y - self.offset,
        #     self.zpos - self.offset)
        glTranslatef (self.xpos + self.offset/ 2, self.ypos - pos_y - self.offset/ 2,
             self.zpos - self.offset)
        glRotatef (angle, 0.0, 1.0, 0.0)
      
        mat_ambient = [ 0.3, 0.3, 0.3, 1.0 ]
        glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
        
        glBegin(GL_QUADS)
        glVertex3f(x1-depth,    y1+depth,        depth)
        glVertex3f(x2+depth,    y1+depth,        depth)
        glVertex3f(x2+depth,    y2-depth,        depth)
        glVertex3f(x1-depth,    y2-depth,        depth)
        glEnd()
        
        self.font.print3Dstr(self.txt, self.myname)
        glPopMatrix ()


    def motion(self, event):
        #print "buton motion", event
        pass
        
    def button(self, res, event):
    
        ret = False 
        
        if self.myname in res.names:
            got = True 
        else: 
            got = False 
           
        if event.type == gtk.gdk.BUTTON_PRESS:
            if got:
                ret = True 
                self.focus = True 
                #print "button press"
                self.offset = 0.04
            else: 
                self.focus = False

        if event.type == gtk.gdk._2BUTTON_PRESS:
            if got:
                pass
            
        if event.type == gtk.gdk.BUTTON_RELEASE:
            if got:
                self.focus = True 
                self.offset = 0.0
                print "button event", self.txt
                ret = True 
            
        return ret





