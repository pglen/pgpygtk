#!/usr/bin/env python

# 3D File Manager in Python OpenGL
#
# Copyright by Peter Glen; Jan, 2015
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
import gtk, gtk.gtkgl
import gobject, pango

#import pyrand

from OpenGL.GL import *
from OpenGL.GLU import *

from pyfmutil import *
from pyfmlight import *

from py3dfont.pyfmfont import *

display_mode = \
    gtk.gdkgl.MODE_RGB | gtk.gdkgl.MODE_DEPTH | gtk.gdkgl.MODE_DOUBLE

# Simple window holding the file manager's 3D space

class GLfileMan (object):

    def __init__ (self):

        self.display_mode = display_mode

        self.initvars()

        self.twinkle = 0.0
        self.showstars = True
        self.showgrid = True
        self.showtri = not False
        self.showdonut = False
        self.showcubes = False
        self.showrand = False
        self.showtext = False
        self.enable = False
        self.anicount = 0
        self.starcol = 0.3
        self.cnt = 0
        self.full = False
        self.zoffset = -50

        self.arr = []
        self.selarr = []

        #ttt =  time.time()
        self.xrand =  rand.XRand()
        #print "Random gen time", time.time() - ttt

        self.stars = []
        for jj in range(300):
            self.stars.append( (rand.frand2(10.0), rand.frand2(10.0), \
                 rand.frand4(-3, -12), rand.frand(1)))

        self.bigstars = []
        for jj in range(200):
            self.bigstars.append((rand.frand2(8.0), rand.frand2(8.0), \
                rand.frand4(-3, -12), rand.frand(1) ))

        self.initfonts()

        self.BLACK = gtk.gdk.Color(0x0, 0x0, 0x0)
        self.RED = gtk.gdk.Color(0xffff, 0x0, 0x0)
        self.GREEN = gtk.gdk.Color(0x0, 0xffff, 0x0)
        self.BLUE = gtk.gdk.Color(0x0, 0x0, 0xffff)

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
        #print "www/hhh", www, hhh
        self.glarea.set_size_request(www/4, hhh/4)

        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.fullscreen(); self.full = True


        #print gtk.gdk.screen_width(), gtk.gdk.screen_height();
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
        self.win.connect("button-press-event", self.area_button)
        self.win.connect("button-release-event", self.area_button)

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

        #self.__enable_timeout = False
        self.__enable_timeout = True
        self.__timeout_interval = 30
        self.__timeout_id = 0

    # Init system fonts
    def initfonts(self):

        self.font   = GlSysFont(1.)
        self.font.setdepth(-.2)
        self.font.setfontcolor([ 0.729412, 0.723529, 0.727451, 1.0 ])

        self.fontb  = GlSysFont(1.)
        self.fontb.setfontcolor([ 0.929412, 0.023529, 0.927451, 1.0 ])

        self.font2  = GlSysFont(.5)

        self.font2s  = GlSysFont(.5)
        self.font2s.setfontcolor([ 0.929412, 0.023529, 0.927451, 1.0 ])
        self.font2s.fatfont(.6)

        self.font4  = GlSysFont(.25)
        self.font4.setfontcolor([ 0.929412, 0.023529, 0.027451, 1.0 ])
        self.font4.setsidecolor([ 0.929412, 0.923529, 0.027451, 1.0 ])
        self.font4.setdepth(.03)
        #self.font4.resetfont()

        self.font4i = GlSysFont(.25)
        self.font4i.setfontcolor([ 0.029412, 0.923529, 0.927451, 1.0 ])
        self.font4i.skewfont(.4)

        self.font4b = GlSysFont(.25)
        self.font4b.fatfont(1.4)
        self.font4b.setfontcolor([ 0.329412, 0.023529, 0.027451, 1.0 ])

        self.font4ib = GlSysFont(.25)
        self.font4ib.fatfont(1.7)
        self.font4ib.skewfont(.3)

        self.font8  = GlSysFont(1./8)
        self.font8.setfontcolor([ 0.029412, 0.923529, 0.027451, 1.0 ])

        self.font12 = GlSysFont(1./12)


    def initvars(self):
        self.__sdepth = -15
        self.__sphi = 0.0
        self.__stheta = 0.0
        self.__sgamma = 0.0
        self.__supdown = 0
        self.__sside = 0

        self.angle   = 0.0
        self.angle2  = 0.0
        self.angle3  = 0.0
        self.angle5  = 0.0
        self.angle7  = 0.0

    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                #print "area_button", event.x, event.y
                #midx = event.x - self.width / 2
                #midy = event.y - self.height / 2

                # Get the viewport
                viewport = glGetIntegerv(GL_VIEWPORT)
                width =  viewport[2]; height = viewport[3]
                print  viewport[2],  viewport[3], event.x, event.y

                buff = glSelectBuffer(100)
                #bs = glGetIntegerv(GL_SELECTION_BUFFER_SIZE); print "bs", bs

                glMatrixMode (GL_PROJECTION)

                glPushMatrix()
                glLoadIdentity()

                gluPickMatrix(event.x, viewport[3] - event.y, 2, 2, viewport);

                # Apply perspective matrix
                #print "viewport",  viewport[2],  viewport[3]
                #aspect = viewport[2] / viewport[3]
                aspect =  float(gtk.gdk.screen_width()) / gtk.gdk.screen_height()

                gluPerspective(20.0, aspect, 5.0, 160.0);
                glRenderMode(GL_SELECT)

                glMatrixMode (GL_MODELVIEW)
                glPushMatrix()
                glLoadIdentity()
                self.renderscene()
                glPopMatrix();

                lookfor = []
                self.selarr = []
                res = glRenderMode(GL_RENDER)
                for aa in res:
                    print aa.near, aa.far, aa.names
                    lookfor = list(aa.names)

                glMatrixMode (GL_PROJECTION)
                glPopMatrix();

                self.selarr.append(lookfor)
                #self.pick(lookfor)

                #print "buff", buff
                #self.arr.append((midx / 170, -midy  / 170, 0, rand.frand(1) ))
                #self.glarea.window.invalidate_rect(
                #            self.glarea.allocation, False)

                #glMatrixMode (GL_PROJECTION)
                #glPopMatrix();

        self.invalidate()

        #elif  event.type == gtk.gdk._2BUTTON_PRESS:
        #    if event.button == 1:
                #print "double", event.x, event.y

    def pick(self, lookfor):

        viewport = glGetIntegerv(GL_VIEWPORT)

        fbbuff = glFeedbackBuffer(62000, GL_3D_COLOR)
        glRenderMode(GL_FEEDBACK)

        glMatrixMode (GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        # // Apply perspective matrix
        aspect =  float(gtk.gdk.screen_width()) / gtk.gdk.screen_height()
        #aspect = viewport[2] / viewport[3]
        gluPerspective(20.0, aspect, 5.0, 160.0);

        glMatrixMode (GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.renderscene()
        glPopMatrix();

        glMatrixMode (GL_PROJECTION)
        glPopMatrix();

        res2 = None
        try:
            res2 = glRenderMode(GL_RENDER)
        except:
            a,b,c = sys.exc_info()
            print sys.excepthook(a,b,c)
            exit()
            return

        self.arr = []

        found = False
        for aa in res2:
            #print aa
            # Select polygon
            if aa[0] == GL_PASS_THROUGH_TOKEN:
                if aa[1] in lookfor:
                    print "Found:", aa
                    found = True
                else:
                    found = False
                continue

            # Emit vertices
            if found:
                if aa[0] ==  GL_POINT_TOKEN:
                    print pvertex(aa[1])
                if aa[0] ==  GL_LINE_TOKEN:
                    print pvertex(aa[1]),
                    print pvertex(aa[2])
                if aa[0] ==  GL_POLYGON_TOKEN:
                    for cc in aa[1:]:
                        #print pvertex(cc),
                        self.arr.append(cc)
                    #print

    def area_motion(self, area, event):
        #print "motion event", event.state, event.x, event.y
        if event.state & gtk.gdk.BUTTON1_MASK:
            self.__sgamma += (self.__beginX - event.x)/10.0
            self.__stheta += (self.__beginY - event.y)/4.0
            self.invalidate()

        elif event.state & gtk.gdk.BUTTON3_MASK:
            self.__sdepth += (self.__beginY - event.y)/10.0
            self.__sphi += (event.x - self.__beginX)/4.0
            self.invalidate()

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
                self.__sdepth += .5

            if event.keyval == gtk.keysyms.minus or \
                   event.keyval == gtk.keysyms.KP_Subtract :
                # Zoom out.
                self.__sdepth -= .5

            if event.keyval == gtk.keysyms.KP_Right :
                self.__sgamma -= 2
            if event.keyval == gtk.keysyms.KP_Left :
                self.__sgamma += 2

            if event.keyval == gtk.keysyms.Left :
                self.__sside += .5
            if event.keyval == gtk.keysyms.Right :
                self.__sside -= .5

            if event.keyval == gtk.keysyms.Up :
                self.__supdown -= .5
            if event.keyval == gtk.keysyms.Down :
                self.__supdown += .5

            if event.keyval == gtk.keysyms.KP_Up :
                self.__stheta += 2
            if event.keyval == gtk.keysyms.KP_Down :
                self.__stheta -= 2

            if event.keyval == gtk.keysyms.KP_Page_Up :
                self.__sphi -= 2
            if event.keyval == gtk.keysyms.KP_Page_Down :
                self.__sphi += 2

            if event.keyval == gtk.keysyms.x or \
                    event.keyval == gtk.keysyms.X:
                if event.state  & gtk.gdk.MOD1_MASK:
                    self.__timeout_remove()
                    area.destroy()

            if event.keyval == gtk.keysyms.f or \
                    event.keyval == gtk.keysyms.F:
                if event.state  & gtk.gdk.MOD1_MASK:
                    self.win.fullscreen(); self.full = True

            if event.keyval == gtk.keysyms.t or \
                    event.keyval == gtk.keysyms.T:
                self.toggle_animation()

            if event.keyval == gtk.keysyms.u or \
                    event.keyval == gtk.keysyms.U:
                if event.state  & gtk.gdk.MOD1_MASK:
                    self.win.unfullscreen(); self.full = False

            if event.keyval == gtk.keysyms.r or \
                    event.keyval == gtk.keysyms.R or \
                    event.keyval == gtk.keysyms.Home or \
                    event.keyval == gtk.keysyms.KP_Home :
                    # Reset
                    self.initvars()

            if event.keyval == gtk.keysyms.F11:
                    if self.full == True:
                        self.win.unfullscreen(); self.full = False
                    else:
                        self.win.fullscreen(); self.full = True

            if event.keyval == gtk.keysyms.a:
                self.showrand = not self.showrand
            if event.keyval == gtk.keysyms.c:
                self.showcubes = not self.showcubes
            if event.keyval == gtk.keysyms.d:
                self.showdonut = not self.showdonut
            if event.keyval == gtk.keysyms.i:
                self.showtri = not self.showtri
            if event.keyval == gtk.keysyms.s :
                self.showstars = not self.showstars
            if event.keyval == gtk.keysyms.g :
                self.showgrid = not self.showgrid

            self.invalidate()

    # --------------------------------------------------------------------

    def __realize(self, widget):

        #print "realize"
        gldrawable = widget.get_gl_drawable()
        glcontext = widget.get_gl_context()

        # OpenGL begin.
        if not gldrawable.gl_begin(glcontext):
            return

        light(self)

        gldrawable.gl_end()
        # OpenGL end

    # --------------------------------------------------------------------

    def __configure_event(self, widget, event):

        self.width = widget.allocation.width
        self.height = widget.allocation.height

        gldrawable = widget.get_gl_drawable()
        glcontext = widget.get_gl_context()

        # OpenGL begin.
        if not gldrawable.gl_begin(glcontext):
            return

        glViewport (0, 0, self.width, self.height)

        glMatrixMode (GL_PROJECTION)
        glLoadIdentity ()

        #viewport = glGetIntegerv(GL_VIEWPORT)
        #print  "_configure", viewport[2],  viewport[3]
        #aspect = viewport[2] / viewport[3]
        
        # We need screen aspect, not window
        aspect =  float(gtk.gdk.screen_width()) / gtk.gdk.screen_height()
        gluPerspective(20.0, aspect, 5.0, 160.0);

        gldrawable.gl_end()

    # --------------------------------------------------------------------

    def __expose_event(self, widget, event):

        gldrawable = widget.get_gl_drawable()
        glcontext = widget.get_gl_context()

        if not gldrawable.gl_begin(glcontext):
            print "no drawable state"
            return

        glViewport (0, 0, self.width, self.height)
        #print  "_expose", self.width, self.height

        # OpenGL begin.
        glMatrixMode (GL_MODELVIEW)

        glPushMatrix()
        glLoadIdentity ()
        glRenderMode(GL_RENDER)
        self.renderscene(True)
        glPopMatrix()

        if gldrawable.is_double_buffered():
            gldrawable.swap_buffers()
        else:
            glFlush()

        gldrawable.gl_end()
        # OpenGL end

    # --------------------------------------------------------------------

    def renderscene(self, showall = False ):

        glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glInitNames()
        glPushName(0)

        ss = float(self.__sside) / 100
        ud = float(self.__supdown) / 100
        gluLookAt(ss, ud, 0, 0,0,-1, 0,1,0)

        glTranslatef (0.0, 0.0, self.__sdepth)
        glRotatef(-self.__stheta, 1.0, 0.0, 0.0)
        glRotatef(self.__sphi, 0.0, 0.0, 1.0)
        glRotatef(self.__sgamma, 0.0, 1.0, 0.0)

        if  0: #self.anicount < 40:
            ver = "PYTHON"
            xstr = "FILE MANAGER"
            #glRotatef (self.anicount / 2, 1.0, 0.0, 0.0)
            #glRotatef (self.anicount/6, 0.0, 1.0, 0.0)

            glPushMatrix ()
            hoffset = -self.font.extent3Dstr(ver)[0]/2
            offset = 0; self.zoffset += 1
            glPushMatrix ()
            offset -= self.font.FontHeight + self.font.linegap
            glTranslatef (hoffset, offset, self.zoffset)
            self.font.print3Dstr(ver)
            glPopMatrix ()

            glPushMatrix ()
            offset -= self.font.FontHeight + self.font.linegap
            offset -= self.font.FontHeight + self.font.linegap
            hoffset = -self.font.extent3Dstr(xstr)[0]/2
            glTranslatef (hoffset, offset, self.zoffset)
            self.font.print3Dstr(xstr)
            glPopMatrix ()
            glPopMatrix ()
        else:
            try:
                if self.showdonut:
                    donut(self)
                if self.showcubes:
                    cubes(self)
                if self.showrand:
                    randtri(self)
                if self.showtri:
                    stuff(self)
                if self.showtext:
                    text(self)
                if self.showstars:
                    stars(self)
                if self.showgrid:
                    grid(self)

            except:
                a,b,c = sys.exc_info(); print sys.excepthook(a,b,c)
                exit
                return
                #raise SystemExit

        if 1: #showall:
            style = self.glarea.get_style()
            self.gc = style.fg_gc[gtk.STATE_NORMAL]
            gcx = gtk.gdk.GC(self.glarea.window); gcx.copy(self.gc)
            gcr = gtk.gdk.GC(self.glarea.window); gcr.copy(self.gc)
            colormap = gtk.widget_get_default_colormap()
            gcr.set_foreground(colormap.alloc_color("#ff0000"))

            for vv in self.arr:
                aa,bb,cc = vv.vertex
                aa=int(aa); bb=int(bb); cc=int(cc)
                bb = self.height-bb
                dd = 5
                self.glarea.window.draw_line(gcr, aa-dd, bb-dd, aa+dd, bb+dd)
                self.glarea.window.draw_line(gcr, aa+dd, bb-dd, aa-dd, bb+dd)
                #self.win.window.draw_line(gcr, bb, cc, bb+dd, cc+dd)
            if 0:
                global pylonarr
                for vv in self.selarr:
                    if pylonarr.id in vv:
                        for vvv in pylonarr.arr:
                            for vv in vvv.verts:
                                glPushMatrix()
                                glRotatef (self.angle7, 0.0, 1.0, 0.0)
                                glTranslatef (vv._x, vv._y, vv._z)
                                gtk.gdkgl.draw_cube (True, 0.03)
                                glPopMatrix()

    # --------------------------------------------------------------------

    def __timeout_callback(self, widget):

        self.anicount += 1

        # Pre start animation
        if self.anicount < 42:
            self.glarea.window.invalidate_rect(self.glarea.allocation, False)

        #print self.glarea.allocation

        self.cnt += 1
        if self.cnt >= 1000:
            self.cnt = 0

        if not self.enable:
            return True

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
                                                self.__timeout_callback,
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

    def toggle_animation(self):

        #self.__enable_timeout = not self.__enable_timeout;
        #if self.__enable_timeout:
        #    self.__timeout_add()
        #else:
        #    self.__timeout_remove()
        #    self.glarea.window.invalidate_rect(self.glarea.allocation,
        #                                       False)

        self.enable = not self.enable

    def invalidate(self):
        if self.glarea.window:
            self.glarea.window.invalidate_rect(
                self.glarea.allocation, False)

    def run (self):
        self.win.show()
        gtk.main()

if __name__ == '__main__':

    glapp = GLfileMan()
    glapp.run()

































