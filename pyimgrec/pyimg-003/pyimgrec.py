#!/usr/bin/env python

import os, sys, getopt, signal, array
import gobject, gtk, pango, time
from timeit import Timer
from random import *

import treehand
import pyimgrec.imgrec as imgrec

# ------------------------------------------------------------------------
# This is open source image recognition program. Written in python with
# plugins in 'C'

version = 0.2
verbose = False
xstr = ""

# Profile line, use it on bottlenecks
#got_clock = time.clock()   
# profiled code here
#print  "Str", time.clock() - got_clock        

# Where things are stored (backups, orgs, macros)
config_dir = os.path.expanduser("~/.pyimgrec")

def help():

    print 
    print "PyImgRec version: ", version
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

# ------------------------------------------------------------------------

class MainWin():

    def __init__(self):
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Python Stickies")
        window.set_position(gtk.WIN_POS_CENTER)
        
        #ic = gtk.Image(); ic.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
        #window.set_icon(ic.get_pixbuf())
        
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        #window.set_default_size(www/2, hhh/2)
        
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
        #window.connect("button-press-event", self.area_button)        
        
        try:
            window.set_icon_from_file("icon.png")
        except:
            pass
        
        vbox = gtk.VBox(); hbox = gtk.HBox()
        
        self.spacer(hbox, True )
        
        self.wwww = 2 * www / 3
        self.hhhh = 2 * hhh / 3
        
        self.area = gtk.DrawingArea()
        self.area.set_size_request(self.wwww, self.hhhh)
        self.area.connect("expose-event", self.expose)
        
        self.image = gtk.Image()
        #self.image.set_from_file("african.jpg")
        #self.image.set_from_file("IMG_0823.jpg")
        self.image.set_from_file("IMG_0827.jpg")
        
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, self.wwww, self.hhhh)
        self.image2 = gtk.Image()
        self.image2.set_from_pixbuf(pixbuf)
        self.get_img()
        
        hbox2 = gtk.HBox()
        self.spacer(hbox2)
        hbox2.add(self.area)
        
        self.tree = treehand.TreeHand(self.tree_sel_row)
        hbox2.add(self.tree.stree)
        vbox.pack_start(hbox2)
        
        #lab11 = gtk.Label(""); hbox.pack_start(lab11, True )
        
        butt1 = gtk.Button(" _Load Image ")
        butt1.connect("clicked", self.load_image, window)
        hbox.pack_start(butt1, False)
        
        self.spacer(hbox)
        
        butt1 = gtk.Button(" _Analize Image ")
        butt1.connect("clicked", self.anal_image, window)
        hbox.pack_start(butt1, False)
    
        self.spacer(hbox)
        
        butt3 = gtk.Button(" _Refresh Image ")
        butt3.connect("clicked", self.refr_image, window)
        hbox.pack_start(butt3, False)
    
        self.spacer(hbox, True )
        
        vbox.pack_start(hbox, False)
        window.add(vbox)
    
    def spacer(self, hbox, flag = False ):
        lab14 = gtk.Label("  "); 
        hbox.pack_start(lab14, flag )
        
    # Refresh image from original    
    def get_img(self):
    
        iw = self.image.get_pixbuf().get_width()
        ih = self.image.get_pixbuf().get_height()
        
        print "Image Size:", iw, ih, "Window Size:", self.wwww, self.hhhh
        
        iww = self.wwww; ihh = self.hhhh
        if iw > ih:  
            scalex = float(self.wwww)/iw
        else:        
            scalex = float(self.hhhh)/ih
            iww = iw * scalex
            
        self.image.get_pixbuf().scale(self.image2.get_pixbuf(), 0, 0, iww, ihh, 
                            0, 0, scalex, scalex, gtk.gdk.INTERP_TILES)  
        
    # Paint the image
    def expose(self, area, a3):
        winn = self.area.window
        rc = area.get_allocation()
        gc = gtk.gdk.GC(winn);
        colormap = gtk.widget_get_default_colormap()        
        winn.draw_pixbuf( gc, self.image2.get_pixbuf(), 0, 0, 0, 0)
        
        #gc.set_line_attributes(6, gtk.gdk.LINE_SOLID,gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
        #gc.set_foreground(colormap.alloc_color("#aaaaaa"))
        #winn.draw_line(gc, 0, 7, rc.width, rc.height+7 )
        #gc.set_foreground(colormap.alloc_color("#ffffff"))
        #winn.draw_line(gc, 0, 0, rc.width, rc.height)
        
    def load_image(self, arg, ww):
        print "Load image"
        
    def refr_image(self, arg, ww):
        print "Refr image"
        self.get_img()
        winn = self.area.window
        ww, hh = winn.get_size()
        rect = gtk.gdk.Rectangle(0,0, ww, hh)
        winn.invalidate_rect(rect, False)
        
    # --------------------------------------------------------------------            
    # Using an arrray to manipulate the underlying buffer
    
    def anal_image(self, arg, ww):
    
        #print "Anal image"
        
        # Get img props.
        pb =  self.image2.get_pixbuf()
        iw = pb.get_width(); ih = pb.get_height()
        #print "img dim", iw, ih
        
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            arr = pb.get_pixels_array()
            
        #imgrec.verbose = 1
        imgrec.anchor(arr)
        #print "dims", imgrec.dim1, imgrec.dim2, imgrec.dim3
        #imgrec.poly(0xff000000, (10,10, 44,88, 55,200, 110, 400, 200,500))
        #imgrec.poly(0xff000000, (10, 10, 10, 88, 100, 88, 100, 200))
        
        # Profile line, use it on bottlenecks   
        #got_clock = time.clock()   
        #for aa in range(100):
        
        #print "median %x" % imgrec.median(50, 50, 100, 100)
        #imgrec.blank(50, 50, 100, 100, 0xffff0000)
        
        #print "median %x" % imgrec.median(100, 200, 400, 400)
        #imgrec.blank(100, 200, 400, 400, 0xff00ff00)
        #imgrec.grayen(150, 150, 400, 400, 0x30)
        
        #print "median %x" % imgrec.median(200, 200, 600, 500)
        #imgrec.blank(200, 200, 600, 500, 0xff000000)
        #imgrec.frame(460, 180, 800, 500, 0xff000000)
        #imgrec.whiten(480, 190, 790, 460, 0x20)
        
        #imgrec.line(480, 100, 790, 100, 0xff000000)
        #imgrec.line(790, 100, 790, 400, 0xffff0000)
        #imgrec.line(550, 100, 550, 400, 0xff00ff00)
        
        #imgrec.line(350, 100, 350, 400, 0xff00ff00)
        #imgrec.line(370, 400, 370, 100, 0xff000000)
        
        #imgrec.line(650, 120, 850, 120, 0xffffff00)
        #imgrec.line(850, 100, 650, 100, 0xffffffff)
        
        #imgrec.line(450, 200, 650, 300, 0xffffffff)
        #imgrec.line(650, 300, 750, 320, 0xff00ffff)
        
        #imgrec.line(100, 100, 150, 300, 0xff00ffff)
        #imgrec.line(150, 300, 220, 400, 0xffffffff)
        
        #imgrec.line(150, 300, 100, 100, 0xff00ffff)
        #imgrec.line(220, 400, 150, 300, 0xffffffff)
        
        #imgrec.line(550, 400, 650, 100, 0xffffffff)
        #imgrec.line(10, 10, 950, 590,   0xff000000)
        
        for aa in range(100):
            imgrec.poly(int(0xff000000 + random() * 0xffffff),
                       (random() * 960,  
                        random() * 600,
                        random() * 960,
                        random() * 600,
                        random() * 960,
                        random() * 600,
                        random() * 960,
                        random() * 600,)
                        )
        
        
        #print "median %x" % imgrec.median(400, 450, 900, 590)
        #imgrec.blank(400, 450, 900, 590, 0xff0000ff)
        
        #print  "c", time.clock() - got_clock        
        
        #got_clock = time.clock()   
        #for aa in range (ih/4,  3*ih/4):
        #    for bb in range (iw/4, 3*iw/4):
        #        arr[aa][bb] = 0xff
        #print  "py", time.clock() - got_clock        
        
        winn = self.area.window
        ww, hh = winn.get_size()
        rect = gtk.gdk.Rectangle(0,0, ww, hh)
        winn.invalidate_rect(rect, False)
        
    # --------------------------------------------------------------------            
                    
    def exit_all(self, area):
        gtk.main_quit()

    def OnExit(self, aa):
        gtk.main_quit()
            
    def tree_sel_row(self, xtree):
        #print "tree sel"
        global xstr
        sel = xtree.get_selection()    
        xmodel, xiter = sel.get_selected_rows()
        for aa in xiter:
            xstr = xmodel.get_value(xmodel.get_iter(aa), 0)    
            break

    def key_press_event(self, win, event):
        #print win, event
        if event.state & gtk.gdk.MOD1_MASK:       
            if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
                sys.exit(0)            
                
# Start of program:

if __name__ == '__main__':

    global mainwin
    
    autohide = False 
    #print "Imgrec Version", imgrec.version()
    #print "Imgrec Build  ", imgrec.builddate()
    #print "Imgrec   ", imgrec.__dict__
        
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
        opts, args = getopt.getopt(sys.argv[1:], "hva")
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
        if aa[0] == "-a": autohide = True            

    if verbose:
        print "PyStick running on", "'" + os.name + "'", \
            "GTK", gtk.gtk_version, "PyGtk", gtk.pygtk_version

    mainwin = MainWin()    
    mainwin.window.show_all()    
    
    if autohide:
        mainwin.window.iconify()
    gtk.main()






















