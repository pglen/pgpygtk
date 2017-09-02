#!/usr/bin/env python

import os, sys, getopt, signal, array
import gobject, gtk, pango, time, traceback

from timeit import Timer
from random import *

#from pyimgutils import *

import treehand, img_main
    
try:
    import pyimgrec.imgrec as imgrec
except:
    print_exception("import imgrec")
    print "Cannot import imgrec, using py implementation"

# ------------------------------------------------------------------------
# This is open source image recognition program. Written in python with
# plugins in 'C'

version = 0.12
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
        window.set_title("Python Image Recognition")
        window.set_position(gtk.WIN_POS_CENTER)
        self.smrc = None
        self.narr = []
        #ic = gtk.Image(); ic.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
        #window.set_icon(ic.get_pixbuf())
        
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
         
        window.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
         
        window.connect("destroy", self.OnExit)
        window.connect("button-press-event", self.area_button)        
        window.connect("key-press-event", self.key_press_event)        
        window.connect("configure-event", self.config_event)        

        self.pangolayout = self.window.create_pango_layout("a")        
        try:
            window.set_icon_from_file("icon.png")
        except:
            pass
       
        disp = gtk.gdk.display_get_default()
        scr = disp.get_default_screen()
        ptr = disp.get_pointer()
        mon = scr.get_monitor_at_point(ptr[1], ptr[2])
        geo = scr.get_monitor_geometry(mon)   
        www = geo.width; hhh = geo.height
        xxx = geo.x;     yyy = geo.y
        
        # Resort to old means of getting screen w / h
        if www == 0 or hhh == 0:
            www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
            
        #print www, hhh
        self.wwww = 3 * www / 4;  self.hhhh = 3 * hhh / 4
        
        self.hbox_s = gtk.HBox()
        self.hbox_s2 = gtk.HBox()
        self.hbox = gtk.HBox()
        self.mainbox = gtk.HBox()
        self.hbox2 = gtk.HBox()
        self.hbox3 = gtk.HBox()
        
        self.area = img_main.img_main(self) 
        self.vport = gtk.Viewport()
        self.scroller = gtk.ScrolledWindow()
        
        
        self.vport.add(self.area)
        self.scroller.add(self.vport)                 
        self.mainbox.add(self.scroller)
        
        try:
            # Load default image(s)
            #self.load("images/african.jpg")
            #self.load("images/IMG_0823.jpg")
            #self.load("images/shapes.png")
            #self.load("images/shapex.png")
            self.load("images/untitled.png")
            #self.load("images/star.png")
            #self.load("images/IMG_0827.jpg")
            #self.load("images/enrolled.pgm")
        except:
            print_exception("Load Image")
            msg("Cannot load file " + self.fname)
            
        pix = self.area.image.get_pixbuf()
        iww = pix.get_width(); ihh = pix.get_height()
        
        if iww > self.wwww or ihh > self.hhhh:
            self.scroller.set_size_request(self.wwww, self.hhhh)
        else:
            self.scroller.set_size_request(iww + 30, ihh + 30)
        
        vbox2 = gtk.VBox()
        self.tree = treehand.TreeHand(self.tree_sel_row)
        vbox2.pack_start(self.tree.stree, True)
        
        #self.area3 = gtk.DrawingArea()
        #vbox2.pack_start(self.area3)
        
        lab2 = gtk.Label("Test Image")
        vbox2.pack_start(lab2, False)
        self.img = gtk.Image(); self.img.set_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_DIALOG)
        frame = gtk.Frame(); frame.add(self.img)
        vbox2.pack_start(frame, True)
        self.lab = gtk.Label("idle")
        vbox2.pack_start(self.lab, False)
        
        self.mainbox.add(vbox2)
        
        self.buttons(self.hbox, window)
        self.buttons2(self.hbox2, window)
        self.checks(self.hbox3, window)
                
        self.spacer(self.hbox_s, False)                
        self.spacer(self.hbox_s2, False)                
        
        self.vbox = gtk.VBox(); 
        
        self.vbox.pack_start(self.hbox_s, False)
        self.vbox.pack_start(self.mainbox, True)
        self.vbox.pack_start(self.hbox_s2, False)
        self.vbox.pack_start(self.hbox, False)
        self.vbox.pack_start(self.hbox2, False)
        self.vbox.pack_start(self.hbox3, False)
        
        window.add(self.vbox)
        
        # Move to current monitor corner
        #xxx, yyy = window.get_position()
        #window.move(xxx, 65)
    
    def set_small_text(self, txt):
        self.lab.set_text(txt)
    
    def clear_small_img(self, color = 0x000000ff):
        # Only get this once after resize
        if not self.smrc:
            self.smrc = self.img.get_allocation()
            
        rc = self.img.get_allocation()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8,  rc.width, rc.height)
        pixbuf.fill(color)
        self.img.set_from_pixbuf(pixbuf)
        rc = self.mainbox.get_allocation()
        self.mainbox.window.invalidate_rect(rc, False)
        
    def fill_small_img(self, img):
    
        # Only get this once after resize
        if not self.smrc:
            self.smrc = self.img.get_allocation()
        #print "fill small", self.smrc.width, self.smrc.height
        nnn = img.get_pixbuf().scale_simple(self.smrc.width, self.smrc.height, 
                    gtk.gdk.INTERP_NEAREST)
        self.img.set_from_pixbuf(nnn)
        #self.mainbox.show_now()
        rc = self.mainbox.get_allocation()
        self.mainbox.window.invalidate_rect(rc, False)
                
    
    # --------------------------------------------------------------------
    def checks(self, hbox, window):
        
        self.spacer(hbox, True )
        
        self.check1 = gtk.CheckButton(" Draw Grid ")
        self.check1.connect("clicked", self.check_hell, window)
        hbox.pack_start(self.check1, False)
        
        self.spacer(hbox, False )
        
        self.check2 = gtk.CheckButton(" _Click heaven ")
        self.check2.connect("clicked", self.check_hell, window)
        hbox.pack_start(self.check2, False)

        self.spacer(hbox, False )

        self.radio1 = gtk.RadioButton(None, " Flood ")
        self.radio1.connect("clicked", self.check_hell, window)
        hbox.pack_start(self.radio1, False)
        
        self.spacer(hbox, False )

        self.radio2 = gtk.RadioButton(self.radio1, " Rect Flood ")
        self.radio2.connect("clicked", self.check_hell, window)
        hbox.pack_start(self.radio2, False)
        
        self.spacer(hbox, False )

        self.radio3 = gtk.RadioButton(self.radio1, " Walk ")
        self.radio3.connect("clicked", self.check_hell, window)
        hbox.pack_start(self.radio3, False)
        
        self.spacer(hbox, True )
        
    def check_hell(self, arg, ww):
        '''print "check1", self.check1.get_active()
        print "check2", self.check2.get_active()
        print "radio1", self.radio1.get_active()
        print "radio2", self.radio2.get_active()'''
        print 
        
    # --------------------------------------------------------------------
    # Load image
    
    def load(self, fname):
    
        self.fname = fname
        self.area.load(fname)
        #self.area.get_img()
        
    # --------------------------------------------------------------------    
    def buttons(self, hbox, window):
    
        self.spacer(hbox, True )
        
        butt1 = gtk.Button(" _Load Image ")
        butt1.connect("clicked", self.load_image, window)
        hbox.pack_start(butt1, False)
        
        self.spacer(hbox)
        
        butt1 = gtk.Button(" Save _Image ")
        butt1.connect("clicked", self.save_image, window)
        hbox.pack_start(butt1, False)
        
        self.spacer(hbox)
        
        butt1 = gtk.Button(" _Analize Image ")
        butt1.connect("clicked", self.anal_image, window)
        hbox.pack_start(butt1, False)
    
        self.spacer(hbox)
        
        butt3 = gtk.Button(" _Refresh Image ")
        butt3.connect("clicked", self.refr_image, window)
        hbox.pack_start(butt3, False)
    
        self.spacer(hbox)
        
        butt4 = gtk.Button(" _Magnifier ")
        butt4.connect("clicked", self.mag_image, window)
        hbox.pack_start(butt4, False)
        
        self.spacer(hbox)
        
        butt5 = gtk.Button(" _Clear Annote ")
        butt5.connect("clicked", self.clear_annote, window)
        hbox.pack_start(butt5, False)
        self.spacer(hbox)
        
        butt6 = gtk.Button(" Save Shape ")
        butt6.connect("clicked", self.save_shape, window)
        hbox.pack_start(butt6, False)
        
        self.spacer(hbox, True )

    def buttons2(self, hbox, window):
    
        self.spacer(hbox, True )
        
        butt6 = gtk.Button(" _Normalize ")
        butt6.connect("clicked", self.norm, window)
        hbox.pack_start(butt6, False)
        
        self.spacer(hbox)

        butt7 = gtk.Button(" _Brighten ")
        butt7.connect("clicked", self.bri, window)
        hbox.pack_start(butt7, False)
        
        self.spacer(hbox)
        
        butt8 = gtk.Button(" _Darken ")
        butt8.connect("clicked", self.dar, window)
        hbox.pack_start(butt8, False)
        
        self.spacer(hbox)
        
        butt9 = gtk.Button(" _Walk ")
        butt9.connect("clicked", self.walk, window)
        hbox.pack_start(butt9, False)

        self.spacer(hbox)
        
        butt9 = gtk.Button(" _Edge ")
        butt9.connect("clicked", self.edge, window)
        hbox.pack_start(butt9, False)

        self.spacer(hbox)
        
        butt91 = gtk.Button(" _Smooth ")
        butt91.connect("clicked", self.smooth, window)
        hbox.pack_start(butt91, False)

        self.spacer(hbox)
        
        butt92 = gtk.Button(" Blan_k ")
        butt92.connect("clicked", self.blank, window)
        hbox.pack_start(butt92, False)

        self.spacer(hbox)
        
        butt99 = gtk.Button(" E_xit ")
        butt99.connect("clicked", self.exit, window)
        hbox.pack_start(butt99, False)
        
        self.spacer(hbox, True )
        
        
    def exit(self, butt, window):
        self.OnExit(1)
    
    def blank(self, butt, window):
        self.area.blank_image()
        
    def smooth(self, butt, window):
        self.area.smooth_image()
        
    def dar(self, butt, window):
        self.area.dar_image()
        
    def bri(self, butt, window):
        self.area.bri_image()
         
    def norm(self, butt, window):
        #print "Norm" #,butt, window
        self.area.norm_image()
        
    def walk(self, butt, window):
        #print "Walk" #,butt, window
        self.area.walk_image(2, 2)
        
    def edge(self, butt, window):
        #print "Walk" #,butt, window
        self.area.edge_image()
        
    def spacer(self, hbox, flag = False ):
        lab14 = gtk.Label(" "); 
        hbox.pack_start(lab14, flag )
        
    # Refresh image from original    
    def mag_image(self, area, a3):
        self.area.toggle_mag()
        
    # Paint the image
    def area_motion(self, area, event):    
        #print  "area_motion", event.x, event.y
        pass
        #gc.set_line_attributes(6, gtk.gdk.LINE_SOLID,gtk.gdk.CAP_NOT_LAST, gtk.gdk.JOIN_MITER)
        #gc.set_foreground(colormap.alloc_color("#aaaaaa"))
        #winn.draw_line(gc, 0, 7, rc.width, rc.height+7 )
        #gc.set_foreground(colormap.alloc_color("#ffffff"))
        #winn.draw_line(gc, 0, 0, rc.width, rc.height)
        
    def load_image(self, arg, ww):
        self.fname = ofd("Open Image File").result
        if not self.fname:
            return
        try:
            self.load(self.fname)
        except:
            msg("Cannot load file:\n%s" % self.fname)
        
    def save_image(self, arg, ww):
        fname = ofd("Save Image File", 
                gtk.FILE_CHOOSER_ACTION_SAVE).result
        if not fname:
            return
        try:
            if fname[-4:] != ".jpg":
                fname += ".jpg"
            pix = self.area.image2.get_pixbuf()
            pix.save(fname, "jpeg", {"quality":"100"});
        except:
            print sys.exc_info()
            msg("Cannot save file:\n%s" % fname)
        
    def anal_image(self, win, a3):
        self.area.anal_image()
                
    def refr_image(self, arg, ww):
        self.area.refresh()
        self.area.invalidate()
        
    def invalidate(self):
        self.area.invalidate()
        
    def config_event(self, win, event):
        rc = self.window.get_allocation()
        #print "rc", rc
        if rc.width != event.width or rc.height != event.height:
            #print "config_event resize", event
            self.smrc = None
        
    def  area_button(self, win, event):
        #print "main", event
        #self.fill_small_img(self.area.image2)
        pass     
        
    def clear_annote(self, win, a3):     
        self.area.clear_annote()
        #self.set_small_text("annote cleared")
        
    def save_shape(self, win, a3):     
        print "Save shape data", len(self.narr)
        
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
        #print "main key_press_event", win, event
        if event.state & gtk.gdk.MOD1_MASK:       
            if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
                sys.exit(0) 
                           
        if event.keyval == gtk.keysyms.Escape:
            self.mag = False 
            self.invalidate()
                
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
        print "PyImgRec running on", "'" + os.name + "'", \
            "GTK", gtk.gtk_version, "PyGtk", gtk.pygtk_version
                                                                                  
    mainwin = MainWin()    
    mainwin.window.show_all()    
    
    if autohide:
        mainwin.window.iconify()
    gtk.main()






















