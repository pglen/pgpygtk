#!/usr/bin/env python

import os, sys, glob, getopt, time
import string, signal, stat, shutil
import gtk, math

import plotmenu

class PlotConfig():
    full_screen = False  
    
class PlotView(gtk.Window):

    hovering_over_link = False
    waiting = False

    coords = []
    
    hand_cursor = gtk.gdk.Cursor(gtk.gdk.HAND2)
    regular_cursor = gtk.gdk.Cursor(gtk.gdk.XTERM)
    wait_cursor = gtk.gdk.Cursor(gtk.gdk.WATCH)
    callback = None
    bscallback = None

    # Create the toplevel window
    def __init__(self, pvg, parent=None):
    
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        #self.set_border_width(0)
        
        try:
            self.set_icon_from_file("images/pieplot.png")
        except:
            try:
                self.set_icon_from_file("/usr/share/pangview/pang.png")
            except:
                print "Cannot load app icon."
            
        www = gtk.gdk.screen_width();
        hhh = gtk.gdk.screen_height();
        
        if pvg.full_screen:
            self.set_default_size(www, hhh)
        else:
            self.set_default_size(3*www/4, 3*hhh/4)
            #self.set_default_size(7*www/8, 7*hhh/8)
        
        self.set_position(gtk.WIN_POS_CENTER)

        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)

        hpaned = gtk.HPaned()
        hpaned.set_border_width(5)
        
        area = gtk.DrawingArea()
        area.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        area.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
        
        area.connect("expose-event", self.area_expose_cb)
        area.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        #self.connect("key-release-event", self.area_key)
        
        #hpaned.add(area)
        
        self.add(area)
        self.show_all()
        
    # Call key handler
    def area_key(self, area, event):
        #print "key", area, event
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.x or \
                    event.keyval == gtk.keysyms.X:
                if event.state  & gtk.gdk.MOD1_MASK:
                    area.destroy()
           
    def area_expose_cb(self, area, event):
        #print "expose", area, event, len(self.coords)
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
        ww, hh = area.window.get_size()
        area.window.draw_line(gcr, 10, hh/2, ww-10, hh/2)
        area.window.draw_line(gcr, 10, 10, 10, hh-10)
        
        for aa in range(10, ww - 10, 10):
            area.window.draw_line(gcr, aa, hh/2 - 3, aa, hh/2 + 3)
                
        for aa in range(hh/2, 10, -10):
            area.window.draw_line(gcr, 10-3, aa, 10 + 3, aa)
            
        for aa in range(hh/2, hh - 10, 10):
            area.window.draw_line(gcr, 10-3, aa, 10 + 3, aa)
          
        vhh = hh - 20   # Leave space on top / buttom
        
        # Draw curves
        oldyy = -math.cos(math.radians(0)) * vhh /  + hh/2
        oldxx = 0
        for xx in range(ww - 10):
            yy = -math.cos(math.radians(xx*2)) * vhh / 2 + hh/2
            #area.window.draw_point(gcr, xx+10, yy)
            area.window.draw_line(gcr, int(oldxx+10), int(oldyy),
                int( xx+10), int(yy))
            oldxx = xx; oldyy = yy
        
        if 1:
            oldyy = -math.cos(math.radians(0)) * vhh / 2 + hh/2
            oldxx = 0
            gcr.set_foreground(colormap.alloc_color("#00ff00"))
            for xx in range(ww - 10):
                yy = -math.sin(math.radians(xx*2)) * vhh / 2 + hh/2
                #area.window.draw_point(gcr, xx+10, yy)
                area.window.draw_line(gcr, oldxx+10, oldyy, xx+10, yy)
                oldxx = xx; oldyy = yy
            
        if 0:
            gcr.set_foreground(colormap.alloc_color("#0000ff"))
            for xx in range(ww - 10):
                try:
                    yy = -math.tan(math.radians(xx*2)) * hh / 30 + hh/2
                    area.window.draw_point(gcr, xx+10, yy)
                except:
                    pass
            
            gcr.set_foreground(colormap.alloc_color("#00ffff"))
            for xx in range(ww - 10):
                try:
                
                    yy = -math.asin(math.radians(xx*2)) * hh / 3 + hh/2
                    area.window.draw_point(gcr, xx+10, yy)
                except:
                    pass
                    
    def area_motion(self, area, event):    
        #print "motion", area, event
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
    
    def build_menu(self, window, items):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.Menu, "<pydoc>", accel_group)
        item_factory.create_items(items)
        self.item_factory = item_factory
        return item_factory.get_widget("<pydoc>")

    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                self.coords.append((event.x, event.y, 0))
                print "Left Click at x=", event.x, "y=", event.y
                self.ldown = True 
            if event.button == 3:
                print "Right Click at x=", event.x, "y=", event.y
                mm = self.build_menu(self.window, plotmenu.rclick_menu)
                mm.popup(None, None, None, event.button, event.time)


        elif  event.type == gtk.gdk.BUTTON_RELEASE:
            if event.button == 1:
                print "Left Release at x=", event.x, "y=", event.y
                self.ldown = False 
                #self.coords.append((event.x, event.y, 0))

            if event.button == 3:
                print "Right Release at x=", event.x, "y=", event.y

def help():

    print "Usage: " + sys.argv[0] + " [options] file_regex"
    print "Options:    -v        - Verbose"
    print "            -h        - Help"
    print

def main():
    pv = PlotView(PlotConfig)
    #PangoView()
    gtk.main()

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
 
    startdir = os.getcwd()
    
    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "lufhvdxe:")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True 
        if aa[0] == "-f": showfiles = True 
        if aa[0] == "-d": showdirs = True 
        if aa[0] == "-u": showdupes = True 
        if aa[0] == "-x": delx = True 
        if aa[0] == "-l": skiplinks = True 
        
        if aa[0] == "-e": 
            execfile = string.split(aa[1])
            #print execfile
            
    #if len(args) < 1:
    #    help(); exit(0);
        
    main()




