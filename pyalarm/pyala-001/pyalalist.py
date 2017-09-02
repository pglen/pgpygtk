#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time

FGCOLOR  = "#000000"
BGCOLOR  = "#ffffff"              
HICOLOR  = "#cccccc"              

# ------------------------------------------------------------------------

class PyAlaList(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        self.set_events(    gtk.gdk.ALL_EVENTS_MASK )
        self.pangolayout = self.create_pango_layout("a")
        self.connect("expose-event", self.area_expose_cb)
        self.colormap = gtk.widget_get_default_colormap()        
        self.items = []; self.coords = []; self.curr = 0
        self.scrolly = 0;  self.scrollx = 0
        self.limit = 1000
        self.txcol = self.colormap.alloc_color(FGCOLOR)
        self.bgcol = self.colormap.alloc_color(BGCOLOR)
        self.hlcol = self.colormap.alloc_color(HICOLOR)
        
        # Get Pango steps
        self.cxx, self.cyy = self.pangolayout.get_pixel_size()
        
        # Create scroll items        
        #sm = len(self.items) + self.get_height() / self.cyy + 10        
        self.hadj = gtk.Adjustment(0, 0, 200, 1, 15, 25);
        self.vadj = gtk.Adjustment(0, 0, 200, 1, 15, 25)
        
        self.vscroll = gtk.VScrollbar(self.vadj)
        self.hscroll = gtk.HScrollbar(self.hadj)
        
        # We connect scrollers after construction
        self.hadj.connect("value-changed", self.hscroll_cb)
        self.vadj.connect("value-changed", self.vscroll_cb)
        
        self.connect("key-press-event", self.key_press_event)        
        self.connect("button-press-event", self.button_press_event)        
        
    def button_press_event(self, win, event):
        #print "butt_press_event", win, event
        if event.button == 1:
            vstep = self.cyy + self.cyy / 5
            self.curr = int(event.y / vstep) + self.scrolly
            print self.curr
            self.invalidate()
     
    def moveup(self, cnt = 1):
        if self.curr:
            self.curr -= cnt
            if self.curr < 0: self.curr = 0
            vstep = self.cyy + self.cyy / 5
            if (self.curr - self.scrolly) * vstep < 0:
                #print "scroll up"
                self.scrolly = self.curr 
            self.invalidate()
            
    def movedown(self, cnt = 1):
        lim = len(self.items) - 1
        if self.curr < lim:
            self.curr += cnt
            if self.curr > lim: self.curr = lim
            vstep = self.cyy + self.cyy / 5
            hhh = self.get_height()
            if (self.curr - self.scrolly)* vstep > hhh - vstep:
                self.scrolly = self.curr - hhh / vstep + 1
                #print "scroll down"
            self.invalidate()
       
    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        if event.keyval == gtk.keysyms.Up:
            self.moveup()
            return True
        if event.keyval == gtk.keysyms.Down:
            self.movedown()
            return True
        if event.keyval == gtk.keysyms.Page_Up:
            self.moveup(10)
            return True
        if event.keyval == gtk.keysyms.Page_Down:
            self.movedown(10)
            return True
        if event.keyval == gtk.keysyms.Home:
            self.curr = 1
            self.moveup(1)
            self.invalidate()
            return True
        if event.keyval == gtk.keysyms.End:
            self.moveend()
            return True

    def moveend(self):
        lim = len(self.items) - 1
        self.curr = lim - 1
        self.movedown(1)
        self.invalidate()
    
    def vscroll_cb(self, widget):
        #print "vscroll_cb", widget.get_value()
        self.scrolly = int(widget.get_value())
        self.invalidate()
        
    def hscroll_cb(self, widget):
        #print "vscroll_cb", widget.get_value()
        self.scrollx = int(widget.get_value())
        self.invalidate()
          
    def get_height(self):
        rect = self.get_allocation()
        return rect.height

    def get_width(self):
        rect = self.get_allocation()
        return rect.width
    
    def do_limit(self):
        shift = int(self.limit / 10)
        if len(self.items) >= self.limit:
            self.items = self.items[shift:]

    def area_expose_cb(self, area, event):
     
        vstep = self.cyy + self.cyy / 5
        # We have a window, goto start pos
        hhh = self.get_height()
        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        self.coords = []
        
        # Paint BG
        gcr.set_foreground(self.bgcol)
        self.window.draw_rectangle(gcr, True, 0, 0, \
                self.get_width()-1, self.get_height()-1) 
                
        # Paint text        
        x = 5; y = 5; num = int(self.scrolly)
        while 1:
            if num >= len(self.items):
                break
            if y >= hhh: 
                break
   
            if num == self.curr:
                gcr.set_foreground(self.hlcol)
                self.window.draw_rectangle(gcr, True, 1, y - self.cyy / 5 , \
                        self.get_width() - 2, vstep )
                
            self.pangolayout.set_text(self.items[num][self.scrollx:])            
            gcr.set_foreground(self.txcol)
            self.window.draw_layout(self.gc, x, y, self.pangolayout) 
            num += 1; y += vstep
            
    def invalidate(self, rect = None):                        
        if rect == None:
            ww, hh = self.window.get_size()
            rect = gtk.gdk.Rectangle(0,0, ww, hh)
        #print "Invalidate:", rect
        self.window.invalidate_rect(rect, False)

# ------------------------------------------------------------------------
# Creates a set of scroll bars around the area. It is accessed with the 
# self.area property.

class   PySAlaList(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self)
        self.area = PyAlaList()
        frame = gtk.Frame(); frame.add(self.area)
        hbox = gtk.HBox()
        hbox.pack_start(frame, True, True)
        hbox.pack_end(self.area.vscroll, False, False)
        self.pack_start(hbox, True, True)
        self.pack_end(self.area.hscroll, False, False)
        
    def add_row(self, args):
        self.area.do_limit()
        self.area.items.append(args)
        self.area.moveend()
        
    def limit_row(self, num):
        old = self.area.limit
        self.area.limit = num
        return old

