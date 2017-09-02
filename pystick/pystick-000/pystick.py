#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango

# ------------------------------------------------------------------------
# This is open source sticker program. Written in python. 

GAP = 4                 # Gap in pixels
TABSTOP = 4
FGCOLOR  = "#000000"
BGCOLOR  = "#ffff88"              

version = 1.0
verbose = False
# Where things are stored (backups, orgs, macros)
config_dir = os.path.expanduser("~/.pystick")

class stickWin():

    def __init__(self, me, head, text):

        window = gtk.Window(gtk.WINDOW_POPUP)
        window.set_transient_for(me)
        window.set_decorated(False)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(100, 100)
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        #window.connect("motion-notify-event", self.area_motion)        
        window.set_property("destroy-with-parent", True )
        yy = stickDoc(head, text)
        window.add(yy)
        window.show_all()
    
        
class stickDoc(gtk.DrawingArea):

    def __init__(self, head, text):
    
        self.head = head
        self.text = text
        self.gap = GAP
        
        # Parent widget                 
        gtk.DrawingArea.__init__(self)
        self.set_flags(gtk.CAN_FOCUS | gtk.CAN_DEFAULT| gtk.SENSITIVE | gtk.PARENT_SENSITIVE)

        self.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                    gtk.gdk.POINTER_MOTION_HINT_MASK |
                    gtk.gdk.BUTTON_PRESS_MASK |
                    gtk.gdk.BUTTON_RELEASE_MASK |
                    gtk.gdk.KEY_PRESS_MASK |
                    gtk.gdk.KEY_RELEASE_MASK |
                    gtk.gdk.FOCUS_CHANGE_MASK )

        self.colormap = gtk.widget_get_default_colormap()
        self.fgcolor  = self.colormap.alloc_color(FGCOLOR)              
        self.bgcolor  = self.colormap.alloc_color(BGCOLOR)              
         
        self.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
        self.pangolayout = self.create_pango_layout("a")
        
        self.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("expose-event", self.area_expose_cb)
        self.connect("destroy", self.OnExit)

    def area_button(self, area, event):
        self.grab_focus()
        return True

    def area_motion(self, area, event):    
        print "motion event", event.state, event.x, event.y        
        if event.state & gtk.gdk.BUTTON1_MASK:            
            print "drag"

    def setfont(self, fam, size):
    
        fd = pango.FontDescription()
        fd.set_family(fam)
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
                        
    def get_height(self):
        rect = self.get_allocation()
        return rect.height

    def get_width(self):
        rect = self.get_allocation()
        return rect.width
      
    def area_expose_cb(self, area, event):

        #print "area_expose_cb()", event.area.width, event.area.height
        
        # We have a window, goto start pos
        hhh = self.get_height()
        xlen = len(self.text)

        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        #gcr = gtk.gdk.GC(self.window); gcr.copy(self.gc)
        #colormap = gtk.widget_get_default_colormap()        
        gcx.set_foreground(self.fgcolor)
        
        self.setfont("system", 14)
        self.pangolayout.set_text(self.head)            
        x = 2 * self.gap; y = self.gap
        self.window.draw_layout(gcx, x, y, self.pangolayout, self.fgcolor, self.bgcolor)
        cxx, cyy = self.pangolayout.get_pixel_size()
        
        self.setfont("system", 11)
        self.pangolayout.set_text(self.text)            
        x = 2 * self.gap; y += self.cyy + self.cyy / 2
        self.window.draw_layout(gcx, x, y, self.pangolayout, self.fgcolor, self.bgcolor)
        cxx2, cyy2 = self.pangolayout.get_pixel_size()
        
        # Resize if needed:
        rqx = cxx2 + 4 * self.gap; rqy = cyy2 + 2 * self.gap
        aa, bb = self.get_size_request()
        if aa != rqx or bb != rqy:
            self.set_size_request(rqx, rqy)

    def OnExit(self, aa):
        gtk.main_quit()


def help():

    print 
    print "PyStick version: ", version
    print 
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options] [[filename] ... [filenameN]]"
    print 
    print "Options:"
    print 
    print "            -d level  - Debug level 1-10. (Limited implementation)"
    print "            -v        - Verbose (to stdout and log)"
    print "            -c        - Dump Config"
    print "            -h        - Help"
    print

def area_motion(self, area, event):    
    print "window motion event", event.state, event.x, event.y        
    if event.state & gtk.gdk.BUTTON1_MASK:            
        print "drag"

# Start of program:

if __name__ == '__main__':

    try:
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    except: pass
    
    # Let the user know it needs fixin'
    if not os.path.isdir(config_dir):
        print "Cannot access config dir:", config_dir
        sys.exit(1)

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True            
        #if aa[0] == "-x": clear_config = True            
        #if aa[0] == "-c": show_config = True            
        #if aa[0] == "-t": show_timing = True

    if verbose:
        print "PyStick running on", "'" + os.name + "'", \
            "GTK", gtk.gtk_version, "PyGtk", gtk.pygtk_version

    www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
    

    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    #window.set_decorated(False)
    #window.set_position(gtk.WIN_POS_CENTER)
    #window.set_default_size(100, 100)
    window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
     
    yy = stickWin(window, "Hello World", "This is a sticky\n"
        "With new longer and longer and longer and longer and longer and longer and longer lines\n"
                        "Done.")
    window.show_all()
           
    gtk.main()





