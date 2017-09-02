#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time, math

import plotmenu

class VrPlot(gtk.DrawingArea):

    hovering_over_link = False
    waiting = False
    coords = []
    hand_cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
    regular_cursor = gtk.gdk.Cursor(gtk.gdk.XTERM)
    wait_cursor = gtk.gdk.Cursor(gtk.gdk.WATCH)
    callback = None
    bscallback = None

    def __init__(self, pvg = None, parent=None):
    
        gtk.DrawingArea.__init__(self)
        
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        self.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
        
        self.connect("expose-event", self.area_expose_cb)
        self.connect("button-press-event", self.area_button)
        self.connect("motion-notify-event", self.area_motion)
        
    # Call key handler
    def area_key(self, area, event):
        #print "key", area, event
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.x or \
                    event.keyval == gtk.keysyms.X:
                if event.state  & gtk.gdk.MOD1_MASK:
                    area.destroy()
           
    def area_expose_cb(self, area, event):
    
        #print "area_expose", area, event, len(self.coords)
        
        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        colormap = gtk.widget_get_default_colormap()        
        gcr.set_foreground(colormap.alloc_color("#ff0000"))

        if len(self.coords) > 1:
            olda = self.coords[0][0]; oldb = self.coords[0][1]
            for aa, bb, cc in self.coords:
                if cc != 0:
                    area.window.draw_line(gcr, olda, oldb, aa, bb)
                olda = aa; oldb = bb
        
        # Draw axes        
        gcr.set_foreground(colormap.alloc_color("#000000"))
        ww, hh = self.window.get_size()
        area.window.draw_line(gcr, 10, hh/2, ww-10, hh/2)
        area.window.draw_line(gcr, 10, 10, 10, hh-10)
        
        for aa in range(10, ww - 10, 10):
            area.window.draw_line(gcr, aa, hh/2 - 3, aa, hh/2 + 3)
                
        for aa in range(hh/2, 10, -10):
            area.window.draw_line(gcr, 10-3, aa, 10 + 3, aa)
            
        for aa in range(hh/2, hh - 10, 10):
            area.window.draw_line(gcr, 10-3, aa, 10 + 3, aa)
          
        vhh = hh - 20   # Leave space on top / buttom
        
        # Draw curve
        '''oldyy = -math.cos(math.radians(0)) * vhh /  + hh/2
        oldxx = 0
        for xx in range(ww - 10):
            yy = -math.cos(math.radians(xx*2)) * vhh / 2 + hh/2
            #area.window.draw_point(gcr, xx+10, yy)
            area.window.draw_line(gcr, oldxx+10, oldyy, xx+10, yy)
            oldxx = xx; oldyy = yy'''
                    
    def area_motion(self, area, event):    
        #print self.__class__, "motion", area, event
        if event.state & gtk.gdk.BUTTON1_MASK:            
            self.coords.append((event.x, event.y, 1))
            clen = len(self.coords)
            if  clen > 1:
                #print "lbdown motion", event.x, event.y
                #ww, hh = area.window.get_size()
                xx = self.coords[clen-2][0]
                yy = self.coords[clen-2][1]
                xx2 = self.coords[clen-1][0]
                yy2 = self.coords[clen-1][1]
                
                rect = gtk.gdk.Rectangle( min(xx,xx2) - 1,
                                            min(yy,yy2) - 1,
                                                abs(xx2-xx) + 2,   
                                                    abs(yy2 - yy) + 2)
                area.window.invalidate_rect(rect, False)
    
    '''def build_menu(self, window, items):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.Menu, "<pydoc>", accel_group)
        item_factory.create_items(items)
        self.item_factory = item_factory
        return item_factory.get_widget("<pydoc>")'''

    def area_button(self, area, event):
        print "area_button", area, event
        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                self.coords.append((event.x, event.y, 0))
                print "Left Click at x=", event.x, "y=", event.y
                self.ldown = True 
            if event.button == 3:
                print "Right Click at x=", event.x, "y=", event.y
                #mm = self.build_menu(self.window, plotmenu.rclick_menu)
                self.item_factory = plotmenu.build_menu(self.window, plotmenu.rclick_menu)
                mm = self.item_factory.get_widget("<pydoc>")
                mm.popup(None, None, None, event.button, event.time)

        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                print "Left Release at x=", event.x, "y=", event.y
                self.ldown = False 
                #self.coords.append((event.x, event.y, 0))

            if event.button == 3:
                print "Right Release at x=", event.x, "y=", event.y



