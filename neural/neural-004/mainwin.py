#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time, math

TABSTOP = 4                 # One tab stop worth of spaces

# ------------------------------------------------------------------------

class MainWin():

    def __init__(self):
    
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ex = 0; self.ey = 0;      
        self.maxx = 0; self.maxy = 0; self.minx = 0; self.miny = 0
        self.coords = []; 
        self.coords2 = []; 
        self.coords3 = []; 
        
        window.set_title("PyNeural")
        window.set_position(gtk.WIN_POS_CENTER)
        
        #ic = gtk.Image(); ic.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
        #window.set_icon(ic.get_pixbuf())
        
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        window.set_default_size(www/2, hhh/2)
        
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
         
        window.set_events(gtk.gdk.ALL_EVENTS_MASK)
         
        window.connect("destroy", self.OnExit)
        window.connect("key-press-event", self.key_press_event)        
        window.connect("button-press-event", self.button_press_event)        

        self.setfont()
                
        try:
            window.set_icon_from_file("icon.png")
        except:
            pass
        
        hbox2 = gtk.HBox()
        area = gtk.DrawingArea();  hbox2.pack_start(area)
        area.set_events(gtk.gdk.ALL_EVENTS_MASK)
        area.connect("expose-event", self.area_expose_cb)
        area.connect("motion-notify-event", self.area_motion)

        vbox = gtk.VBox(); vbox.pack_start(hbox2, True)
        hbox = gtk.HBox(); lab1 = gtk.Label("");  hbox.pack_start(lab1)
        #butt1 = gtk.Button(" _New ")
        #butt1.connect("clicked", self.show_new, window)
        #hbox.pack_start(butt1, False)
        
        butt2 = gtk.Button(" E_xit ")
        butt2.connect("clicked", self.OnExit, window)
        hbox.pack_start(butt2, False)
   
        lab2 = gtk.Label("");  hbox.pack_start(lab2)
        vbox.pack_start(hbox, False)
        
        window.add(vbox); window.show_all()


    def setfont(self, fam = None, size = None):
        self.pangolayout = self.window.create_pango_layout("a")
        
        if fam or size:
            fd = pango.FontDescription()
            if fam:
                fd.set_family(fam)
            if size:
                fd.set_size(size * pango.SCALE); 
            self.pangolayout.set_font_description(fd)

        # Get Pango steps
        self.cxx, self.cyy = self.pangolayout.get_pixel_size()
        
        # Get Pango tabs
        self.tabarr = pango.TabArray(80, False)
        for aa in range(self.tabarr.get_size()):
            self.tabarr.set_tab(aa, pango.TAB_LEFT, aa * TABSTOP * self.cxx * pango.SCALE)
                
        self.pangolayout.set_tabs(self.tabarr)
        ts = self.pangolayout.get_tabs()
        
        if ts != None: 
            al, self.tabstop = ts.get_tab(1)
        self.tabstop /= self.cxx * pango.SCALE

    def area_motion(self, area, event):    
        #print "motion", area, event
        self.ex = event.x; self.ey = event.y
        rect = area.get_allocation()
        xx, yy = self.measure_text("a" * 40)
        rect.x = rect.width  - xx - 1; rect.width = xx
        rect.y = rect.height - yy - 1; rect.height = yy
        # This is a test to see the invalidate rectangle
        #gc = area.get_style().fg_gc[gtk.STATE_NORMAL]
        #area.window.draw_rectangle(gc, False, rect.x, rect.y, rect.width - 1, rect.height -1)
        area.window.invalidate_rect(rect, True)

    # Adjust coordinates. Scale / Shift / Convert, and Draw
    def draw_line(self, area, gcr, xx0, yy0, xx1, yy1):
        ww, hh = area.window.get_size()
        # Scale
        try:
            raty = float((hh/2 - 20)) / self.maxy
            ratx = float((ww - 20)) / self.maxx
            # Adjust
            xx00 = ratx * xx0 ;  xx01 = ratx * xx1
            yy00 = -raty * yy0; yy01 = -raty * yy1
            # Convert
            area.window.draw_line(gcr, int(xx00) + 10, int(yy00) + hh/2, int(xx01) + 10, int(yy01) + hh/2)
        except:
            pass
            
    # Draw a text with curent font
    def draw_text(self, area, gc, x, y, text, foreground = None, background = None):
        self.pangolayout.set_text(text)
        xx, yy = self.pangolayout.get_pixel_size()
        area.draw_layout(gc, x, y, self.pangolayout, foreground, background)
        return xx, yy
        
    def measure_text(self, text):
        self.pangolayout.set_text(text)
        xx, yy = self.pangolayout.get_pixel_size()
        return xx, yy
	
    def area_expose_cb(self, area, event):
        #print "expose", area, event, len(self.coords)
        colormap = gtk.widget_get_default_colormap()        
        style = area.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        gcx = gtk.gdk.GC(area.window); gcx.copy(self.gc)
        gcr = gtk.gdk.GC(area.window); gcr.copy(self.gc)
        gcr.set_foreground(colormap.alloc_color("#ff0000"))
        gcg = gtk.gdk.GC(area.window); gcg.copy(self.gc)
        gcg.set_foreground(colormap.alloc_color("#00ff00"))
        gcb = gtk.gdk.GC(area.window); gcb.copy(self.gc)
        gcb.set_foreground(colormap.alloc_color("#0000ff"))
        
        if len(self.coords) > 1:
            # Estabilish boundary numbers
            self.maxx = 0; self.maxy = 0; self.minx = 0; self.miny = 0
            for aa, bb, cc in self.coords:
                if self.maxy < bb: self.maxy = bb
                if self.miny > bb: self.miny = bb
                if self.maxx < aa: self.maxx = aa
                if self.minx > aa: self.minx = aa
                    
            #print "Drawing Coords:", len(self.coords)
            olda = self.coords[0][0]; oldb = self.coords[0][1]
            cnt = 0
            for aa, bb, cc in self.coords:
                self.draw_line(area, gcr, olda, oldb, aa, bb)
                olda = aa; oldb = bb
                cnt += 1
    
        if len(self.coords2) > 1:
            olda = self.coords2[0][0]; oldb = self.coords2[0][1]
            cnt = 0
            for aa, bb, cc in self.coords2:
                self.draw_line(area, gcg, olda, oldb, aa, bb)
                olda = aa; oldb = bb
                cnt += 1

        if len(self.coords3) > 1:
            olda = self.coords3[0][0]; oldb = self.coords3[0][1]
            cnt = 0
            for aa, bb, cc in self.coords3:
                self.draw_line(area, gcb, olda, oldb, aa, bb)
                olda = aa; oldb = bb
                cnt += 1
        
        # Draw axes        
        gcr.set_foreground(colormap.alloc_color("#000000"))
        ww, hh = area.window.get_size()
        area.window.draw_line(gcr, 10, hh/2, ww-10, hh/2)
        area.window.draw_line(gcr, 10, 10, 10, hh-10)
        ah = 1; aw = 1
        
        for aa in range(10, ww - 10, 10):
            area.window.draw_line(gcr, aa, hh/2 - ah, aa, hh/2 + ah)
                
        for aa in range(hh/2, 10, -10):
            area.window.draw_line(gcr, 10-aw, aa, 10 + ah, aa)
            
        for aa in range(hh/2, hh - 10, 10):
            area.window.draw_line(gcr, 10-aw, aa, 10 + ah, aa)
          
        vhh = hh - 40   # Leave space on top / buttom
        
        # Draw text
        if self.maxy and self.maxx:
            raty = float((hh/2 - 20)) / self.maxy
            ratx = float((ww - 20)) / self.maxx
        
            self.draw_text(area.window, gcr, 20, 10, str(self.minx) + " ...  " + str(self.maxx) \
                        + "      " + "%0.3f" % self.miny +  " ...  " + "%0.3f" % self.maxy)
        
            str2 = "xx = %f yy = %f " % (self.ex / ratx, ((hh/2) - self.ey) / raty)
            ww2, hh2 = self.measure_text(str2)
            self.draw_text(area.window, gcr, ww - ww2 - 20, hh - hh2, str2)
        
    def invalidate(self):
        rect = self.window.get_allocation()
        #print "Invalidate", rect
        self.window.window.invalidate_rect(rect, True)

    def  OnExit(self, arg, srg2 = None):
        self.exit_all()
            
    def exit_all(self):
        gtk.main_quit()
            
    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        pass
        
    def button_press_event(self, win, event):
        #print "key_press_event", win, event
        pass
            
# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()    
    gtk.main()











