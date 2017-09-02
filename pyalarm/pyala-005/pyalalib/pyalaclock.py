#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time

FGCOLOR  = "#000000"
BGCOLOR  = "#ffffff"              
HICOLOR  = "#cccccc"              

from pgutil import *

# ------------------------------------------------------------------------

class PyAlaClock(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        self.set_events(    gtk.gdk.ALL_EVENTS_MASK )
        self.pangolayout  = self.create_pango_layout("a")
        self.pangolayout2  = self.create_pango_layout("a")
        self.connect("expose-event", self.area_expose_cb)
        self.colormap = gtk.widget_get_default_colormap()        
        self.items = []; self.coords = []; self.curr = 0
        self.scrolly = 0;  self.scrollx = 0
        self.limit = 1000
        self.txcol = self.colormap.alloc_color(FGCOLOR)
        self.bgcol = self.colormap.alloc_color(BGCOLOR)
        self.hlcol = self.colormap.alloc_color(HICOLOR)
        self.tstr = "00:00"
        self.old_ttt = 0
        # Get Pango steps
        self.cxx, self.cyy = self.pangolayout2.get_pixel_size()
        
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
        gobject.timeout_add(1000, self.clock_tick)
        
    def button_press_event(self, win, event):
        #print "butt_press_event", win, event
        vstep = self.cyy + self.cyy / 5
        self.curr = int(event.y / vstep) + self.scrolly
        if event.button == 1:
            #print "mouse L on", self.curr
            pass
        if event.button == 3:
            # "mouse R on", self.curr
            mmm = pgMenu()
            mmm.additem(" Show Item ", self.showitem, self.curr)
            mmm.additem(" -------- ")
            mmm.additem(" World ", self.hello)
            mmm.popmenu(event)
        self.invalidate()
        return True
      
    def clock_tick(self):
        now = time.time()
        ttt = time.localtime(now)
        self.tstr = "%02d:%02d" % (ttt[3], ttt[4])
        self.lstr = time.asctime(ttt)
        # Tiptoe around DST
        dstr = time.tzname[0]
        try: dstr = time.tzname[time.daylight]
        except: pass
        self.lstr += " " +  dstr
        #print self.lstr
        if ttt[4] != self.old_ttt:
            self.old_ttt = ttt[4] 
            self.invalidate()
        else:
            rect = gtk.gdk.Rectangle(10, 10, self.cxx * len(self.lstr), self.cyy)
            self.invalidate(rect)
        return True
        
    def showitem(self, win, strx, extra):
        print "show", win, strx, extra
        
    def hello(self, win, strx, extra):
        print "hello", win, strx, extra
       
    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        if event.keyval == gtk.keysyms.Up:
            return True
        if event.keyval == gtk.keysyms.Down:
            return True
        if event.keyval == gtk.keysyms.Page_Up:
            return True
        if event.keyval == gtk.keysyms.Page_Down:
            return True
        if event.keyval == gtk.keysyms.Home:
            return True
        if event.keyval == gtk.keysyms.End:
            return True
        if event.keyval == gtk.keysyms.Return:
            return True
        
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
    
    def area_expose_cb(self, area, event):
        vstep = self.cyy + self.cyy / 5
        # We have a window, goto start pos
        hhh = self.get_height()
        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        self.coords = []
        
        # Paint BG
        ww = self.get_width();  hh = self.get_height() 
        
        gcr.set_foreground(self.bgcol)
        self.window.draw_rectangle(gcr, True, 0, 0, ww-1, hh-1) 
        
        gcr.set_foreground(self.colormap.alloc_color("#444444"))
        self.pangolayout2.set_text(self.lstr)
        self.window.draw_layout(gcr, 10, 10, self.pangolayout2) 

        gcr.set_foreground(self.colormap.alloc_color("#888888"))
        fd = pango.FontDescription()
        fd.set_size(ww / len(self.tstr) * pango.SCALE)
        self.pangolayout.set_font_description(fd)
        self.pangolayout.set_text(self.tstr)
        rrr = self.pangolayout.get_size()
        xx = (ww - rrr[0]/pango.SCALE) / 2
        yy = (hh - rrr[1]/pango.SCALE) / 2
        self.window.draw_layout(gcr, xx, yy, self.pangolayout) 
        # Shadow
        gcr.set_foreground(self.colormap.alloc_color("#eeeeee"))
        self.window.draw_layout(gcr, xx + 4, yy + 4, self.pangolayout) 
        
    def invalidate(self, rect = None):                        
        if not self.window:
            return
        if rect == None:
            ww, hh = self.window.get_size()
            rect = gtk.gdk.Rectangle(0,0, ww, hh)
        #print "Invalidate:", rect
        self.window.invalidate_rect(rect, False)

# ------------------------------------------------------------------------
# Creates a set of scroll bars around the area. It is accessed with the 
# self.area property.

class   PySAlaClock(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self)
        self.area = PyAlaClock()
        frame = gtk.Frame(); frame.add(self.area)
        hbox = gtk.HBox()
        hbox.pack_start(frame, True, True)
        #hbox.pack_end(self.area.vscroll, False, False)
        self.pack_start(hbox, True, True)
        #self.pack_end(self.area.hscroll, False, False)






