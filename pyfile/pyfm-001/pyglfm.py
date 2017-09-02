#!/usr/bin/env python

# 3D File Manager in Python OpenGL
# 
# Copyright by Peter Glen
#
# Permission to use, copy, modify, distribute, and sell this software and its
# documentation for any purpose is hereby granted without fee, provided that
# the above copyright notice appear in all copies and that both that
# copyright notice and this permission notice appear in supporting
# documentation.  No representations are made about the suitability of this
# software for any purpose.  It is provided "as is" without express or 
# implied warranty.
#

import math, sys, time, os

import pygtk;  pygtk.require('2.0')
import gtk
import gtk.gtkgl
import gobject
import pango

from OpenGL.GL import *
from OpenGL.GLU import *
from pyfmutil import *
#from rand import *
import rand 

# Simple window holding a toggle button inside which a bouncing torus shows up.
class GLfileMan (object):

    def __init__ (self):
        self.display_mode = gtk.gdkgl.MODE_RGB    | \
                            gtk.gdkgl.MODE_DEPTH  | \
                            gtk.gdkgl.MODE_DOUBLE

        self.__sdepth = -15
        self.__sphi = 0.0
        self.__stheta = 0.0
        self.__sgamma = 0.0
        
        self.twinkle = 0.0
        self.donut = False 
        self.starcol = 0.3
        self.cnt = 0
        
        #ttt =  time.time()
        self.xrand =  rand.XRand()
        #print "Random gen time", time.time() - ttt 
    
        self.stars = []
        for jj in range(300):
            self.stars.append( (rand.frand2(8.0), rand.frand2(8.0), \
                 rand.frand4(-3, -12), rand.frand(1)))

        self.bigstars = []
        for jj in range(200):
            self.bigstars.append((rand.frand2(8.0), rand.frand2(8.0), \
                rand.frand4(-3, -12), rand.frand(1) ))
        
        self.fontListBase = glGenLists(128)

        self.fontString = 'courier 36'
        fontDesc = pango.FontDescription(self.fontString)
        font = gtk.gdkgl.font_use_pango_font(fontDesc, 0, 128, self.fontListBase)
        if not font:
            print "Can't load the font %s" % (self.fontString)
            raise SystemExit
        
        fontMetrics = font.get_metrics()
        self.fontHeight = fontMetrics.get_ascent() + fontMetrics.get_descent()
        self.fontHeight = pango.PIXELS(self.fontHeight)
        #print "self.fontHeight", self.fontHeight
                                                
        #colormap = self.glconfig.get_colormap()
        #self.BLACK = colormap.alloc_color(0x0, 0x0, 0x0, False, False)
        #self.RED = colormap.alloc_color(0xffff, 0x0, 0x0, False, False)
        #self.GREEN = colormap.alloc_color(0x0, 0xffff, 0x0, False, False)
        #self.BLUE = colormap.alloc_color(0x0, 0x0, 0xffff, False, False)
        
        self.BLACK = gtk.gdk.Color(0x0, 0x0, 0x0)
        self.RED = gtk.gdk.Color(0xffff, 0x0, 0x0)
        self.GREEN = gtk.gdk.Color(0x0, 0xffff, 0x0)
        self.BLUE = gtk.gdk.Color(0x0, 0x0, 0xffff)
        
        #self.render_type = gtk.gdkgl.RGBA_TYPE
                
        # Try to create a double buffered framebuffer, if not successful then
        # attempt to create a single buffered one.
        try:
            self.glconfig = gtk.gdkgl.Config(mode=self.display_mode)
        except gtk.gdkgl.NoMatches:
            print "Switching to non double mode"
            self.display_mode &= ~gtk.gdkgl.MODE_DOUBLE
            self.glconfig = gtk.gdkgl.Config(mode=self.display_mode)

        # Create the window for the app.
        self.win = gtk.Window()
        self.win.set_title('Python 3D File Manager')
        if sys.platform != 'win32':
            self.win.set_resize_mode(gtk.RESIZE_IMMEDIATE)
            
        self.win.set_reallocate_redraws(True)
        #self.win.set_border_width(10)
        self.win.connect('destroy', lambda quit: gtk.main_quit())

        # DrawingArea for OpenGL rendering.
        self.glarea = gtk.gtkgl.DrawingArea(self.glconfig)
        
        #self.glarea.set_size_request(600, 600)
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        self.glarea.set_size_request(3*www/4, 3*hhh/4)
        
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.fullscreen()

        self.win.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
                            
        self.win.connect("motion-notify-event", self.area_motion)
        self.win.connect("key-press-event", self.area_key)
        self.win.connect("key-release-event", self.area_key)
     
        # connect to the relevant signals.
        self.glarea.connect_after('realize', self.__realize)
        self.glarea.connect('configure_event', self.__configure_event)
        self.glarea.connect('expose_event', self.__expose_event)
        self.glarea.connect('map_event', self.__map_event)
        self.glarea.connect('unmap_event', self.__unmap_event)
        self.glarea.connect('visibility_notify_event', self.__visibility_notify_event)
        self.glarea.add_events(gtk.gdk.VISIBILITY_NOTIFY_MASK)
        self.glarea.show()
    
        self.win.add(self.glarea)
        
        self.angle   = 0.0
        self.angle2  = 0.0
        self.angle3  = 0.0
        self.angle5  = 0.0
        self.angle7  = 0.0
        
        self.pos_y  = 0.0
        self.pos_y2 = 0.0
        self.pos_x = 0.0
        self.pos_x2 = 0.0

        self.__enable_timeout = True
        self.__timeout_interval = 30
        self.__timeout_id = 0

    def area_motion(self, area, event):    
        #print "motion event", event.state, event.x, event.y     
        if event.state & gtk.gdk.BUTTON1_MASK:
            self.__sgamma += (self.__beginX - event.x)/10.0
            self.__stheta += (self.__beginY - event.y)/4.0
        elif event.state & gtk.gdk.BUTTON3_MASK:
            self.__sdepth += (self.__beginY - event.y)/10.0
            self.__sphi += (event.x - self.__beginX)/4.0
        # Mark old positions
        self.__beginX = event.x
        self.__beginY = event.y

    # Call key handler
    def area_key(self, area, event):
        #print "key event", event
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.plus or \
                   event.keyval == gtk.keysyms.KP_Add :
                # Zoom in.
                self.__sdepth += 2.0
    
            if event.keyval == gtk.keysyms.minus or \
                   event.keyval == gtk.keysyms.KP_Subtract :
                # Zoom out.   
                self.__sdepth -= 2.0
                
            if event.keyval == gtk.keysyms.KP_Right :
                self.__sgamma -= 2
            if event.keyval == gtk.keysyms.KP_Left :
                self.__sgamma += 2
            
            if event.keyval == gtk.keysyms.KP_Up :
                self.__stheta -= 2
            if event.keyval == gtk.keysyms.KP_Down :
                self.__stheta += 2
            
            if event.keyval == gtk.keysyms.KP_Page_Up :
                self.__sphi -= 2
            if event.keyval == gtk.keysyms.KP_Page_Down :
                self.__sphi += 2
                
            if event.keyval == gtk.keysyms.x or \
                    event.keyval == gtk.keysyms.X:
                if event.state  & gtk.gdk.MOD1_MASK:
                    self.__timeout_remove()
                    area.destroy()
                    
            if event.keyval == gtk.keysyms.s or \
                    event.keyval == gtk.keysyms.S:
                if event.state  & gtk.gdk.MOD1_MASK:
                    self.win.fullscreen()

            if event.keyval == gtk.keysyms.u or \
                    event.keyval == gtk.keysyms.U:
                if event.state  & gtk.gdk.MOD1_MASK:
                    self.win.unfullscreen()
                    
            if event.keyval == gtk.keysyms.r:
                self.__sdepth = -15
                self.__sphi = 0.0
                self.__stheta = 0.0
                self.__sgamma = 0.0
                
            if event.keyval == gtk.keysyms.d:
                self.donut = not self.donut
            
    def __realize(self, widget):
        #print "realize"
        gldrawable = widget.get_gl_drawable()
        glcontext = widget.get_gl_context()

        # OpenGL begin.
        if not gldrawable.gl_begin(glcontext):
            return

        # Lighting properties.
        #light_ambient = [0.0, 0.0, 0.0, 1.0]
        #light_ambient = [1.0, 1.0, 1.0, 1.0]
        light_ambient = [0.5, 0.5, 0.5, 1.0]
        
        #light_diffuse = [0.0, 0.0, 0.0, 1.0]
        light_diffuse = [0.5, 0.5, 0.5, 1.0]
        #light_diffuse = [1.0, 1.0, 1.0, 1.0]
        
        light_specular = [.5, .5, .5, 1.0]
        #light_specular = [1.0, 1.0, 1.0, 1.0]
        #light_specular = [.2, .2, .2, 1.0]
        
        #light_position = [1.0, 1.0, 1.0, 1.0]
        #light_position = [0.0, 5.0, 5.0, 0.0]
        light_position = [0.0, 0.0, 1.0, 0.0]
        #light_position = [5.0, 5.0, 5.0, 0.0]
        
        #light_model_ambient = [0.2, 0.2, 0.2, 1.0]
        light_model_ambient = [0.5, 0.5, 0.5, 1.0]
        #light_model_ambient = [0.9, 0.9, 0.9, 1.0]
        light_local_view = 0.0
        #pos = (5.0, 5.0, 5.0, 0.0)
   
        # Initialise the lighting properties.
        glLightfv (GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv (GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv (GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv (GL_LIGHT0, GL_POSITION, light_position)
        #glLightModelfv (GL_LIGHT_MODEL_AMBIENT, light_model_ambient)
        #glLightModelf (GL_LIGHT_MODEL_LOCAL_VIEWER, light_local_view)

        glEnable (GL_LIGHTING)
        glEnable (GL_LIGHT0)
        glEnable (GL_DEPTH_TEST)

        glClearColor(.0, .0, .0, 1.0)
        #glClearColor(.5, .5, .5, 1.0)
        #glClearColor(1.0, 1.0, 1.0, 1.0)
        glClearDepth(1.0)

        gldrawable.gl_end()
        # OpenGL end
    
    def __configure_event(self, widget, event):
        #print "configure"
        
        self.width = widget.allocation.width
        self.height = widget.allocation.height

        gldrawable = widget.get_gl_drawable()
        glcontext = widget.get_gl_context()

        # OpenGL begin.
        if not gldrawable.gl_begin(glcontext):
            return

        width = widget.allocation.width
        height = widget.allocation.height

        glViewport (0, 0, width, height)

        glMatrixMode (GL_PROJECTION)
        glLoadIdentity ()
        
        if (width > height):
            aspect = width / height
            glFrustum (-aspect, aspect, -1.0, 1.0, 5.0, 160.0)
        else:
            aspect = height / width
            glFrustum (-1.0, 1.0, -aspect, aspect, 5.0, 160.0)

        glMatrixMode (GL_MODELVIEW)

        gldrawable.gl_end()
        # OpenGL end

    def __expose_event(self, widget, event):
        #print "expose"
        gldrawable = widget.get_gl_drawable()
        glcontext = widget.get_gl_context()

        # OpenGL begin.
        if not gldrawable.gl_begin(glcontext):
            return

        # Surface material properties.
        #mat_ambient = [ 0.329412, 0.223529, 0.027451, 1.0 ]
        mat_ambient = [ 0.529412, 0.523529, 0.127451, 1.0 ]
        #mat_diffuse = [ 0.780392, 0.568627, 0.113725, 1.0 ]
        mat_diffuse = [ 0.780392, 0.568627, 0.213725, 1.0 ]
        #mat_specular = [ 0.992157, 0.941176, 0.807843, 1.0 ]
        mat_specular = [ 0.992157, 0.941176, 0.907843, 1.0 ]
        mat_shininess = 0.21794872 * 128.0
        #mat_shininess = 0.11794872 * 128.0

        glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity ()
        
        glTranslatef (0.0, 0.0, self.__sdepth)
        glRotatef(-self.__stheta, 1.0, 0.0, 0.0)
        glRotatef(self.__sphi, 0.0, 0.0, 1.0)
        glRotatef(self.__sgamma, 0.0, 1.0, 0.0)

        #glTranslatef (0.0, 0.0, -15.0)

        glPushMatrix ()
        glTranslatef (self.pos_x, self.pos_y, 0.0)
        glRotatef (self.angle2, 0.0, 1.0, 0.0)
        
        #glMaterialfv (GL_FRONT, GL_AMBIENT, mat_ambient)
        #glMaterialfv (GL_FRONT, GL_DIFFUSE, mat_diffuse)
        #glMaterialfv (GL_FRONT, GL_SPECULAR, mat_specular)
        #glMaterialf (GL_FRONT, GL_SHININESS, mat_shininess)
        if self.donut:
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

        try:
            #cubes(self)
            #randtri(self)
            stuff(self)
            #text(self)
            stars(self)
        except:
            print sys.exc_info()
            raise SystemExit
          
        #glColor3f(1.0, 0.0, 0.0)
        #glRasterPos2f(0.0, 0.0, 5)
        #glListBase(self.fontListBase)
        #glCallLists(self.fontString)
          
        if gldrawable.is_double_buffered():
            gldrawable.swap_buffers()
        else:
            glFlush()

        gldrawable.gl_end()
        # OpenGL end

   
    def __timeout(self, widget):
    
        self.cnt += 1
        if self.cnt >= 1000:
            self.cnt = 0
        
        self.angle += 1.0
        if (self.angle >= 360.0):
            self.angle2 -= 360.0

        self.angle2 += 2.0
        if (self.angle2 >= 360.0):
            self.angle2 -= 360.0

        self.angle3 += 3.0
        if (self.angle >= 360.0):
            self.angle -= 360.0

        self.angle5 += 5.0
        if (self.angle5 >= 360.0):
            self.angle5 -= 360.0

        self.angle7 += 7.0
        if (self.angle7 >= 360.0):
            self.angle7 -= 360.0

        if  self.cnt % 50 == 0:
            self.twinkle += 1
            
        if  self.twinkle % 2 == 0:
            self.starcol += 0.02
        else: 
            self.starcol -= 0.02
        
        t = self.angle * math.pi / 180.0
        if t > math.pi:
            t = 2.0 * math.pi - t

        t2 = self.angle * math.pi / 180.0
        
        self.pos_y   = 2.0 * (math.sin (t) + 0.4 * math.sin (3.0*t)) - 1.0
        self.pos_y2  = 2.0 * (math.sin (t))

        self.pos_x  = 2.0 * (math.sin (t/2)) - 1
        self.pos_x2  = 2.0 * (math.sin (t2/2)) - 1

        # Invalidate whole window.
        self.glarea.window.invalidate_rect(self.glarea.allocation, False)
        
        # Update window synchronously (fast).
        #self.glarea.window.process_updates(False)

        return True

    def __timeout_add(self):
        if self.__timeout_id == 0:
            self.__timeout_id = gobject.timeout_add(self.__timeout_interval,
                                                self.__timeout,
                                                self.glarea)

    def __timeout_remove(self):
        if self.__timeout_id != 0:
            gobject.source_remove(self.__timeout_id)
            self.__timeout_id = 0

    def __map_event(self, widget, event):
        if self.__enable_timeout:
            self.__timeout_add()
        return True

    def __unmap_event(self, widget, event):
        self.__timeout_remove()
        return True

    def __visibility_notify_event(self, widget, event):
        if self.__enable_timeout:
            if event.state == gtk.gdk.VISIBILITY_FULLY_OBSCURED:
                self.__timeout_remove()
            else:
                self.__timeout_add()
        return True

    def toggle_animation(self, widget):
        self.__enable_timeout = not self.__enable_timeout;
        if self.__enable_timeout:
            self.__timeout_add()
        else:
            self.__timeout_remove()
            self.glarea.window.invalidate_rect(self.glarea.allocation,
                                               False)

    def run (self):
        self.win.show()
        gtk.main()


if __name__ == '__main__':

    glapp = GLfileMan()
    glapp.run()




