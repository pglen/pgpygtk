#!/usr/bin/env python

#
# 3D File Manager in Python OpenGL, helper routines
# 

import math, sys, rand

import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *

from gtk.gtkgl.apputils import *
from OpenGL.GL.ARB.multitexture import *

CUBE1   = 1; CUBE2   = 2; DONUT   = 3; TRIANG  = 4
TRIANG2 = 5; TRIANG3 = 6; STARS   = 7


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
    glLoadName(CUBE1)
    glPassThrough(CUBE1)
    
    glDisable(GL_TEXTURE_1D)
    glDisable(GL_TEXTURE_3D)
    #glEnable(GL_TEXTURE_2D)
    
    #fname = "/usr/share/pixmaps/gdm-foot-logo.png"
    #fname = "/usr/share/pixmaps/faces/coffee.jpg"
    fname = "/usr/share/pixmaps/faces/sky.jpg"
    #fname = "/usr/share/pixmaps/apple-green.png"
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(fname)
    except:
        print "No image."
        return
    
    if not pixbuf.get_has_alpha():
        pixbuf.add_alpha(False, 255,255,255)
        
    #id = glGenTextures(1)
    #glBindTexture(GL_TEXTURE_2D, id)   # 2d texture (x and y size)
    
    glActiveTextureARB(GL_TEXTURE0_ARB)
    glEnable(GL_TEXTURE_2D)
    
    www = 256; hhh = 256
    pixbuf2 = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, www, hhh)
    pixbuf.scale(pixbuf2, 0, 0, www, hhh, 
                    0, 0, float(www)/pixbuf.get_width(), float(hhh)/pixbuf.get_height(), 
                        gtk.gdk.INTERP_BILINEAR)
                        
    #print  "bps", pixbuf.get_bits_per_sample()
    #print  "chann", pixbuf.get_n_channels()
    #print  "x/y", pixbuf.get_width(), pixbuf.get_height()
    
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

    # Check the extension availability.
    '''if not glInitMultitextureARB():
        print "Help!  No GL_ARB_multitexture"
        sys.exit(1)'''
    
    ww = pixbuf2.get_height(); hh = pixbuf2.get_width()
    #print ww, hh
    
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ww, hh, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, pixbuf2.get_pixels() )
    
    #glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)
    #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    
    glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 0.0, 1.0)
  
    p = 1 #cos(self.rot*self.deg_rad)**2
    glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_COLOR, (p, p, p, 1))

    glBegin(GL_QUADS)

    # Front Face
    # (note that the texture's corners have to match the quad's corners)

    # Bottom Left Of The Texture and Quad
    glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 0.0, 1.0)
    glVertex3f(-1.0, -1.0,  .0)
    
    # Bottom Right Of The Texture and Quad
    glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 1.0, 1.0)
    glVertex3f( 1.0, -1.0,  .0)
    
    # Top Right Of The Texture and Quad
    glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 1.0, 0.0)
    glVertex3f( 1.0,  1.0,  .0)
    
    # Top Left Of The Texture and Quad
    glMultiTexCoord2fARB(GL_TEXTURE0_ARB, 0.0, 0.0)
    glVertex3f(-1.0,  1.0,  .0)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)
  
    glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv (GL_FRONT, GL_SHININESS, mat_shininess)
    
    #glEnable(GL_COLOR_MATERIAL)
    gtk.gdkgl.draw_cube(True, 0.5)
    glDisable(GL_COLOR_MATERIAL)
    
    glPopMatrix ()

    # --------------------------------------------------------------------
    
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
    
    hoffset = -2.5; offset = 2.
    glPushMatrix ()
    offset -= self.font12.FontHeight + self.font12.linegap
    glTranslatef (hoffset, offset, 0)
    self.font12.print3Dstr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    glPopMatrix ()
    
    glPushMatrix ()
    offset -= self.font8.FontHeight  + self.font8.linegap
    glTranslatef (hoffset, offset, 0)
    self.font8.print3Dstr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    glPopMatrix ()
    
    glPushMatrix ()
    offset -= self.font4.FontHeight  + self.font4.linegap
    glTranslatef (hoffset, offset, 0)
    self.font4.print3Dstr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    glPopMatrix ()
    
    glPushMatrix ()
    offset -= self.font4i.FontHeight  + self.font4i.linegap
    glTranslatef (hoffset, offset, 0)
    self.font4i.print3Dstr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    glPopMatrix ()
    
    glPushMatrix ()
    offset -= self.font4b.FontHeight  + self.font4b.linegap
    glTranslatef (hoffset, offset, 0)
    self.font4b.print3Dstr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    glPopMatrix ()

    glPushMatrix ()
    offset -= self.font4ib.FontHeight  + self.font4ib.linegap
    glTranslatef (hoffset, offset, 0)
    self.font4ib.print3Dstr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    glPopMatrix ()

    glPushMatrix ()
    offset -= self.font2.FontHeight  + self.font2.linegap
    glTranslatef (hoffset, offset, 0)
    self.font2.print3Dstr("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    glPopMatrix ()

    strx = ""
    for aa in range(0, 128):
        strx += chr(aa)
    
    #strx = "{<A?:>B];`CDEF`GHI.JKL,M\'NOPQRSTUVWXYZ"

    glPushMatrix ()
    offset -= self.font2s.FontHeight  + self.font2s.linegap
    glTranslatef (hoffset, offset, 0)
    self.font2s.print3Dstr(strx)
    glPopMatrix ()
    
    glPushMatrix ()
    offset -= self.font.FontHeight  + self.font.linegap
    glTranslatef (hoffset, offset, 0)
    self.font.print3Dstr(strx)
    glPopMatrix ()
    
    glPopMatrix ()

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









        





























