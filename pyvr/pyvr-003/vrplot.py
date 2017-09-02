#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time, math

import plotmenu, vrutil

# ------------------------------------------------------------------------

class VrPlot(gtk.DrawingArea):

    coords = []

    def __init__(self, pvg = None, parent=None):
    
        gtk.DrawingArea.__init__(self)

        self.drawpad = None; self.drawpad2 = None; 
        self.cnt = 0                
        self.pause = False
        self.virt_x = 0; self.virt_y = 0
        
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        self.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
        
        self.connect("expose-event", self.area_expose_cb)
        self.connect("key-press-event", self.area_key)
        self.connect("button-press-event", self.area_button)
        self.connect("motion-notify-event", self.area_motion)
        self.connect("configure-event", self.area_config)
        
    def area_config(self, widget, event):
        #print "area_config", widget, event
        self.colormap = gtk.widget_get_default_colormap()        
        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        self.gcx = gtk.gdk.GC(self.window); self.gcx.copy(self.gc)
        self.gcx.set_foreground(self.colormap.alloc_color("#ffffff"))
        self.gcx.set_foreground(self.colormap.alloc_color("#eeeeee"))
        # We force the recreation of backing structure
        self.drawpad = None
    
    # Key handler
    def area_key(self, area, event):
        #print "area_key", event
        if event.keyval == gtk.keysyms.space: 
            self.pause = not self.pause
           
    def area_expose_cb(self, area, event):
        #print "area_expose", area, "event", event, len(self.coords)
        ww, hh = self.window.get_size()
        
        if not self.drawpad:
            self.drawpad = gtk.gdk.Pixmap(self.window, ww, hh)
            self.drawpad.draw_rectangle(self.gcx, True, 0, 0, ww, hh)
            self.drawpad2 = gtk.gdk.Pixmap(self.window, ww, hh)
            self.drawpad2.draw_rectangle(self.gcx, True, 0, 0, ww, hh)
            self.draw_grid()
                
        area.window.draw_drawable(self.gc, self.drawpad, \
                event.area[0], event.area[1], event.area[0], \
                    event.area[1], event.area[2], event.area[3])

    def draw_grid(self):
    
        ww, hh = self.window.get_size()
        self.colormap = gtk.widget_get_default_colormap()        
        gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        gcr.set_foreground(self.colormap.alloc_color("#ff0000"))
        gcr.set_foreground(self.colormap.alloc_color("#000000"))
        self.drawpad.draw_line(gcr, 10, hh/2, ww-10, hh/2)
        self.drawpad.draw_line(gcr, 10, 10, 10, hh-10)
        
        for aa in range(10, ww - 10, 10):
            self.drawpad.draw_line(gcr, aa, hh/2 - 3, aa, hh/2 + 3)
        for aa in range(hh/2, 10, -10):
            self.drawpad.draw_line(gcr, 10-3, aa, 10 + 3, aa)
        for aa in range(hh/2, hh - 10, 10):
            self.drawpad.draw_line(gcr, 10-3, aa, 10 + 3, aa)
        
    def area_motion(self, area, event):    
        #print self.__class__, "motion", area, event
        if event.state & gtk.gdk.BUTTON1_MASK:            
            style = self.get_style()
            self.gc = style.fg_gc[gtk.STATE_NORMAL]
            gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
            gcx.set_foreground(self.colormap.alloc_color("#ffffff"))
            gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
            gcr.set_foreground(self.colormap.alloc_color("#ff0000"))
            self.coords.append((event.x, event.y, 1))
            clen = len(self.coords)
            if  clen > 1:
                #print "lbdown motion", event.x, event.y
                xx = self.coords[clen-2][0]
                yy = self.coords[clen-2][1]
                xx2 = self.coords[clen-1][0]
                yy2 = self.coords[clen-1][1]
                self.plotpoint(xx, yy)
    
    def area_button(self, area, event):
        #print "area_button", area, event
        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                self.coords.append((event.x, event.y, 0))
                #print "Left Click at x=", event.x, "y=", event.y
                self.ldown = True 
            if event.button == 3:
                #print "Right Click at x=", event.x, "y=", event.y
                self.item_factory = plotmenu.build_menu(self.window, plotmenu.rclick_menu)
                mm = self.item_factory.get_widget("<pydoc>")
                mm.popup(None, None, None, event.button, event.time)
        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                #print "Left Release at x=", event.x, "y=", event.y
                self.ldown = False 
                #self.coords.append((event.x, event.y, 0))
            if event.button == 3:
                print "Right Release at x=", event.x, "y=", event.y

    # Change current plot color
    def plotcolor(self, color_str):
        self.gc.set_foreground(self.colormap.alloc_color(color_str))

    # Draw a dot on the widget
    def plotpoint(self, xx, yy):
        self.drawpad.draw_point(self.gc, xx, yy)
        rect = gtk.gdk.Rectangle(xx - 1, yy - 1, xx + 1, yy + 1)
        self.window.invalidate_rect(rect, False)
        # Test the whole surface
        #ww, hh = self.window.get_size()
        #rect = gtk.gdk.Rectangle(0, 0, ww, hh)
        #self.window.invalidate_rect(rect, False)
    
    # Draw a line on the widget
    def plotline(self, xx, yy, xx2, yy2):
        self.drawpad.draw_line(self.gc, xx, yy, xx2, yy2)
        rect = gtk.gdk.Rectangle(min(xx, xx2) - 1, min(yy, yy2) - 1, \
                        max(xx, xx2) + 1, max(yy, yy2) + 1)
        self.window.invalidate_rect(rect, False)

    # --------------------------------------------------------------------
    # Draw an oscilloscope like line on the widget. Scroll if needed.
    
    def plotline2(self, yy):
        if self.pause:
            return
        ww, hh = self.window.get_size()
        yy2 = yy; yy = self.virt_y 
        scr = 100
        # Scroll
        if self.virt_x >= ww:
            # Make a copy, clean it, shift it back
            self.drawpad2.draw_drawable(\
                    self.gcx, self.drawpad, 0, 0, 0, 0, ww, hh)
            self.drawpad.draw_rectangle(self.gcx, True, 0, 0, ww, hh)
            self.drawpad.draw_drawable(\
                    self.gcx, self.drawpad2, scr, 0, 0, 0, ww-scr, hh)
            self.draw_grid()
            self.virt_x = ww - scr; 
            
        xx = self.virt_x;  xx2 = xx + 1
        self.drawpad.draw_line(self.gc, xx, yy, xx2, yy2)
        self.virt_y = yy2; self.virt_x = xx2
        rect = gtk.gdk.Rectangle(min(xx, xx2) - 1, min(yy, yy2) - 1, \
                        max(xx, xx2) + 1, max(yy, yy2) + 1)
        rect = gtk.gdk.Rectangle(0, 0, ww, hh)
        self.window.invalidate_rect(rect, False)
        #vrutil.usleep(1000)

    # Draw a rect on the widget
    def plotrect(self, xx, yy, xx2, yy2, fill = False):
        #print "plotrect", xx, yy, xx2, yy2
        self.drawpad.draw_rectangle(self.gc, fill, xx, yy, xx2, yy2)
        rect = gtk.gdk.Rectangle(min(xx, xx2) - 1, min(yy, yy2) - 1, \
                        max(xx, xx2) + 2, max(yy, yy2) + 2)
        self.window.invalidate_rect(rect, False)
            
    # Draw a circle on the widget
    def plotcirc(self, xx, yy, xx2, yy2, fill = False):
        #print "plotcircle", xx, yy, xx2, yy2
        self.drawpad.draw_arc(self.gc, fill, xx, yy, xx2, yy2, 0, 360 * 64)
        rect = gtk.gdk.Rectangle(min(xx, xx2) - 1, min(yy, yy2) - 1, \
                        max(xx, xx2) + 2, max(yy, yy2) + 2)
        self.window.invalidate_rect(rect, False)
            
        
