#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time

BGCOLOR  = "#888888"

CLEAR   = 0
TEXT    = 1
LINE    = 2
RECT    = 3
CIRC    = 4

def handler_tick(arg):
    print "handler_tick", arg
    arg.butt.hide()    
    pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
    color = gtk.gdk.Color()
    cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
    arg.window.window.set_cursor(cursor)

class mybox(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self)
        self.txtarr = []                      
        self.pangolayout = self.create_pango_layout("a")
        self.connect("expose-event", self.area_expose_cb)
        
    def setfont(self, fam, size):
        fd = pango.FontDescription()
        if fam:
            fd.set_family(fam)
        if size:
            fd.set_size(size * pango.SCALE); 
        self.pangolayout.set_font_description(fd)
  
    def area_expose_cb(self, area, event):
        rect = self.get_allocation()
        www = rect.width; hhh = rect.height
        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        colormap = gtk.widget_get_default_colormap()        
        gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        gcr.set_foreground(colormap.alloc_color(BGCOLOR))
        self.window.draw_rectangle(gcr, True, 0, 0, www - 1, hhh - 1)
                    
        gct = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        
        foreground = None; background = None
        for aa in self.txtarr:
            if aa[0] == TEXT:
                self.setfont(aa[6], aa[5])
                try:
                    foreground = colormap.alloc_color(aa[4])
                except: pass
                self.pangolayout.set_text(aa[3])            
                self.window.draw_layout(gct, aa[1], aa[2], \
                            self.pangolayout, foreground, background)
                
            if aa[0] == RECT:
                try:
                    foreground = colormap.alloc_color(aa[5])
                except: pass
                
                gcr.set_foreground(colormap.alloc_color(foreground))
                self.window.draw_rectangle(gcr, True, aa[1], aa[2], \
                                    aa[3], aa[4])
            
            if aa[0] == CIRC:
                try:
                    foreground = colormap.alloc_color(aa[5])
                except: pass
                
                gcr.set_foreground(colormap.alloc_color(foreground))
                self.window.draw_arc(gcr, True, aa[1], aa[2], \
                                    aa[3], aa[4], 0, 360 * 64)
            
            if aa[0] == LINE:
                try:
                    foreground = colormap.alloc_color(aa[5])
                except: pass
                gcr.set_foreground(colormap.alloc_color(foreground))
                self.window.draw_line(gcr, aa[1], aa[2], \
                                        aa[3], aa[4])

# ------------------------------------------------------------------------

class MainWin():

    def __init__(self):
    
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        window.set_title("Python Display")
        window.set_position(gtk.WIN_POS_CENTER)
        
        #ic = gtk.Image(); ic.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
        #window.set_icon(ic.get_pixbuf())
        
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        #window.set_default_size(www/2, hhh/2)
        window.fullscreen()
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        window.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
         
        window.connect("destroy", self.OnExit)
        window.connect("key-press-event", self.key_press_event)        
        window.connect("button-press-event", self.button_press_event)        
        window.connect("expose-event", self.area_expose_cb)
        window.connect("event-after", self.after)

        try:
            window.set_icon_from_file("icon.png")
        except:
            pass

        # Drawing surface
        self.vbox = mybox()
        
        self.addline(100, 100, 900, 900, "#00eeee")
        
        #self.addcirc(400, 400, 400, 400, "#555555")
        self.addtext(10, 10,  "hello")
        self.addtext(20, 20,  "hello again", "#ff0000", 36)
        self.addtext(228, 58, "Greeen", "#cccccc", 200)
        
        self.addrect(430, 755, 200, 200, "#ff0000")
        
        self.addrect(630, 755, 100, 100, "#0000ff")
        self.addrect(730, 755, 100, 100, "#00ff00")
        self.addrect(830, 755, 100, 100, "#cccccc")
        
        self.addtext(220, 50, "Greeen", "#00ff00", 200)
        self.addtext(120, 500, "Black Roman", "#000000", 160, "times")
        self.addtext(124, 504, "Black Roman", "#555555", 160, "times")
        
        self.addtext(20, 800, "Resudial default display")
        self.addcirc(730, 855, 600, 100, "#ffff00")
       
        #self.addline(600, 600, 1000, 1400, "#00ee00")
        
        hbox = gtk.HBox(); hbox.set_border_width(4)
        self.butt = gtk.Button(" E_xit ")
        self.butt
        hbox.pack_start(gtk.Label(" "))
        hbox.pack_start(self.butt, False)
        hbox.pack_start(gtk.Label(" "), False)
        
        self.vbox.pack_start(gtk.Label(" "))
        self.vbox.pack_start(hbox, False)
        
        window.add(self.vbox)
        window.show_all()
        gobject.timeout_add(5000, handler_tick, self)

    # Drawing primitives

    def addtext(self, xx, yy, xstr, fontcol = "#000000", \
                                        fontsize = 12, fontfam = None):
        self.vbox.txtarr.append((TEXT, xx, yy, xstr, fontcol, fontsize, fontfam))

    def addrect(self, xx, yy, ww, hh, col = "#000000"):
        self.vbox.txtarr.append((RECT, xx, yy, ww, hh, col))

    def addcirc(self, xx, yy, ww, hh, col = "#000000"):
        self.vbox.txtarr.append((CIRC, xx, yy, ww, hh, col))

    def addline(self, xx, yy, xx2, yy2, col = "#000000"):
        self.vbox.txtarr.append((LINE, xx, yy, xx2, yy2, col))

    def  OnExit(self, arg, srg2 = None):
        self.exit_all()
            
    def exit_all(self):
        gtk.main_quit()
            
    def key_press_event(self, win, event):
        #print "key_press_event", win, event
        if event.keyval == gtk.keysyms.Escape:
            gtk.main_quit()
            #sys.exit(0)
        pass
        
    def button_press_event(self, win, event):
        #print "key_press_event", win, event
        self.window.window.set_cursor(None)
        gobject.timeout_add(5000, handler_tick, self)
        pass
        
    def invalidate(self, rect = None):                        
        if rect == None:
            ww, hh = self.window.get_size()
            rect = gtk.gdk.Rectangle(0,0, ww, hh)
        #print "Invalidate:", rect
        self.window.invalidate_rect(rect, False)

    def get_size(self):
        rect = self.window.get_allocation()
        return rect.width, rect.height

    def get_height(self):
        rect = self.window.get_allocation()
        return rect.height

    def get_width(self):
        rect = self.window.get_allocation()
        return rect.width

    def after(self, widget, event):
        #print "after", widget, event
        if event.type == gtk.gdk.EXPOSE:
            pass
            #print "post expose"
            #self.post_expose_cb(widget, event)

    def area_expose_cb(self, area, event):
        #print "area_expose_cb()", event.area.width, event.area.height
        self.post_expose_cb(area, event)
        #return True
        
    def post_expose_cb(self, area, event):
        hhh = self.get_height();  www = self.get_width()
        style = self.window.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        colormap = gtk.widget_get_default_colormap()        
        gcr = gtk.gdk.GC(self.window.window); gcr.copy(self.gc)
        gcr.set_foreground(colormap.alloc_color(BGCOLOR))
        self.vbox.window.draw_rectangle(gcr, True, 0, 0, www - 1, hhh - 1)
        
            
# ------------------------------------------------------------------------    
# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()    
    gtk.main()


