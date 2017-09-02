#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango
import random, time

BGCOLOR  = "#888888"

CLEAR   = 0
TEXT    = 1
RECT    = 2
CIRC    = 3

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

        try:
            window.set_icon_from_file("icon.png")
        except:
            pass

        self.txtarr = []                      
        self.pangolayout = self.window.create_pango_layout("a")

        self.addcirc(400, 400, 400, 400, "#555555")
        self.addtext(10, 10,  "hello")
        self.addtext(20, 20,  "hello again", "#ff0000", 36)
        self.addtext(228, 58, "Greeen", "#cccccc", 200)
        
        self.addrect(430, 755, 200, 200, "#ff0000")
        self.addrect(530, 755, 100, 100, "#cccccc")
        self.addrect(630, 755, 100, 100, "#0000ff")
        self.addrect(730, 755, 100, 100, "#00ff00")

        self.addtext(220, 50, "Greeen", "#00ff00", 200)
        self.addtext(120, 500, "Black Roman", "#000000", 160, "times")
        
        self.addtext(20, 800, "Resudial default display")
        self.addcirc(730, 855, 100, 100, "#ffff00")
       
        #window.add(vbox)
        window.show_all()

    def setfont(self, fam, size):
        fd = pango.FontDescription()
        if fam:
            fd.set_family(fam)
        if size:
            fd.set_size(size * pango.SCALE); 
        self.pangolayout.set_font_description(fd)

    def addtext(self, xx, yy, xstr, fontcol = "#000000", \
                                        fontsize = 12, fontfam = None):
        self.txtarr.append((TEXT, xx, yy, xstr, fontcol, fontsize, fontfam))

    def addrect(self, xx, yy, ww, hh, col = "#000000"):
        self.txtarr.append((RECT, xx, yy, ww, hh, col))

    def addcirc(self, xx, yy, ww, hh, col = "#000000"):
        self.txtarr.append((CIRC, xx, yy, ww, hh, col))

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

    def area_expose_cb(self, area, event):
        #print "area_expose_cb()", event.area.width, event.area.height
        
        # We have a window, goto start pos
        hhh = self.get_height();  www = self.get_width()
        #print "www", www, "hhh", hhh
        style = self.window.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        colormap = gtk.widget_get_default_colormap()        
        gcr = gtk.gdk.GC(self.window.window); gcr.copy(self.gc)
        gcr.set_foreground(colormap.alloc_color(BGCOLOR))
        self.window.window.draw_rectangle(gcr, True, 0, 0, www - 1, hhh - 1)
        
        gct = gtk.gdk.GC(self.window.window); gcr.copy(self.gc)
        
        foreground = None; background = None
        for aa in self.txtarr:
            print aa
            
            if aa[0] == TEXT:
                self.setfont(aa[6], aa[5])
                try:
                    foreground = colormap.alloc_color(aa[4])
                except: pass
                self.pangolayout.set_text(aa[3])            
                self.window.window.draw_layout(gct, aa[1], aa[2], \
                            self.pangolayout, foreground, background)
                
            if aa[0] == RECT:
                try:
                    foreground = colormap.alloc_color(aa[5])
                except: pass
                
                gcr.set_foreground(colormap.alloc_color(foreground))
                self.window.window.draw_rectangle(gcr, True, aa[1], aa[2], \
                                    aa[3], aa[4])
            
            if aa[0] == CIRC:
                try:
                    foreground = colormap.alloc_color(aa[5])
                except: pass
                
                gcr.set_foreground(colormap.alloc_color(foreground))
                self.window.window.draw_arc(gcr, True, aa[1], aa[2], \
                                    aa[3], aa[4], 0, 360 * 64)
            
        return True
            
# ------------------------------------------------------------------------    
# Start of program:

if __name__ == '__main__':

    mainwin = MainWin()    
    gtk.main()








