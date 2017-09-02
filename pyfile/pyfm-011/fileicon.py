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


class FileIcon():

    def __init__(self, self2, fname, txt, command, xpos = 0, ypos = 0, zpos = 0):

        global gl_name
        
        self.pixbuf2 = None
        self.command = command
        self.self2 = self2
        self.txt = txt; self.fname = fname
        self.xpos = xpos;  self.ypos = ypos; self.zpos = zpos
        self.myname = self2.nextname()
        self.focus = False 
                
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file(fname)
        except:
            print "No image."
            return

        if not pixbuf.get_has_alpha():
            #print "Adding Alpha", fname
            #pixbuf.add_alpha(False, 255,255,255)
            pixbuf.add_alpha(True, 0, 0, 0)
            
        www = 256; hhh = 256
        self.pixbuf2 = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, www, hhh)
        pixbuf.scale(self.pixbuf2, 0, 0, www, hhh,
                        0, 0, float(www)/pixbuf.get_width(), float(hhh)/pixbuf.get_height(),
                            gtk.gdk.INTERP_BILINEAR)

    def draw(self, pos_y, angle):

        if not self.pixbuf2:
            print "No image", self.fname
            return
            
        glPushMatrix ()

        #print glGetString(GL_EXTENSIONS)
        #glEnable(GL_TEXTURE_2D)

        # Check the extension availability.
        #if not glInitMultitextureARB():
        #    print "Help!  No GL_ARB_multitexture"
        #    sys.exit(1)

        
        glTranslatef (self.xpos, self.ypos - pos_y, self.zpos)
        glRotatef (angle, 0.0, 1.0, 0.0)

        siz = .4
        glPushMatrix ()
        exten = self.self2.font8.extent3Dstr(self.txt)
        glTranslatef (-exten[0]/2, -siz * 1.5, 0.1)
        self.self2.font8.print3Dstr(self.txt)
        glPopMatrix ()
        
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        #glPixelStorei(GL_UNPACK_ALIGNMENT,    1)
        #glPixelStorei(GL_UNPACK_SKIP_ROWS,    0)
        #glPixelStorei(GL_UNPACK_SKIP_PIXELS,  0)
        #glPixelStorei(GL_UNPACK_ROW_LENGTH,   0)

        glEnable(GL_TEXTURE_2D)
        glActiveTextureARB(GL_TEXTURE0_ARB)
        ww = self.pixbuf2.get_height(); hh = self.pixbuf2.get_width()
        #print ww, hh

        glTexImage2D(GL_TEXTURE_2D, 0, 3, ww, hh, 0, GL_RGBA,
                    GL_UNSIGNED_BYTE, self.pixbuf2.get_pixels() )
        
        glLoadName(self.myname)
        #glPassThrough(self.myname)
    
        glBegin(GL_QUADS)

        # Bottom Left 
        glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 0.0, 1.0)
        glVertex3f(-siz, -siz,  .0)
        # Bottom Right
        glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 1.0, 1.0)
        glVertex3f( siz, -siz,  .0)
        # Top Right 
        glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 1.0, 0.0)
        glVertex3f( siz,  siz,  .0)
        # Top Left 
        glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 0.0, 0.0)
        glVertex3f(-siz,  siz,  .0)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        
        # Focus
        if self.focus:
            #print "focus"
            mat_ambient = [ 0.6, 0.6, 0.6, 1.0 ]
            glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
            
            glBegin(GL_QUADS)

            x1 = -siz;  x2 = siz
            y1 = siz;  y2 = -siz
            linegap = 0.01;  depth = 0.01
            
            yf = y1 + linegap
            glVertex3f(x1,      y1,      0 - depth)
            glVertex3f(x2,      y1,      0 - depth)
            glVertex3f(x2,      yf,      0 - depth)
            glVertex3f(x1,      yf,      0 - depth)
            
            yf = y2 - linegap
            glVertex3f(x1,      y2,      0 - depth)
            glVertex3f(x2,      y2,      0 - depth)
            glVertex3f(x2,      yf,      0 - depth)
            glVertex3f(x1,      yf,      0 - depth)
            
            xf = x1 - linegap
            glVertex3f(xf,      y1,      0 - depth)
            glVertex3f(x1,      y1,      0 - depth)
            glVertex3f(x1,      y2,      0 - depth)
            glVertex3f(xf,      y2,      0 - depth)

            xf = x2 + linegap
            glVertex3f(xf,      y1,      0 - depth)
            glVertex3f(x2,      y1,      0 - depth)
            glVertex3f(x2,      y2,      0 - depth)
            glVertex3f(xf,      y2,      0 - depth)
            
            glEnd()        
            
        glPopMatrix ()

    def do_exec(self):
        print  "Exec", self.txt
        try:
            ret = subprocess.Popen([self.command,])
        except:
            print"\n   Cannot launch ", self.command 
            a,b,c = sys.exc_info()
            print sys.excepthook(a,b,c)
               
    def motion(self, event):
        #print "fileicon motion", event
        pass
        
    def button(self, res, event):
        if self.myname in res.names:
            got = True 
        else: 
            got = False 
           
        if event.type == gtk.gdk.BUTTON_PRESS:
            if got:
                self.focus = True 
            else: 
                self.focus = False

        if event.type == gtk.gdk._2BUTTON_PRESS:
            if got:
                self.do_exec()
            




    








