#!/usr/bin/env python

import os, sys, getopt, signal, array
import gobject, gtk, pango, time

from timeit import Timer
from random import *

import treehand, img_main
import pyimgrec.imgrec as imgrec

import pyimgutils

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
        window.set_title("Python Image Recognition")
        window.set_position(gtk.WIN_POS_CENTER)
        
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

        self.pangolayout = self.window.create_pango_layout("a")        
        try:
            window.set_icon_from_file("icon.png")
        except:
            pass
        
        vbox = gtk.VBox(); hbox = gtk.HBox()
        hbox2 = gtk.HBox()
        
        self.hbox2 = gtk.HBox()
        self.spacer(self.hbox2)
        self.area = img_main.img_main() 
        self.hbox2.add(self.area)
        
        try:
            # Load default image(s)
            #self.load("images/african.jpg")
            #self.load("images/IMG_0823.jpg")
            #self.load("images/IMG_0827.jpg")
            self.load("images/enrolled.pgm")
        except:
            pyimgutils.msg("Cannot load file")
            
        vbox2 = gtk.VBox()
        self.tree = treehand.TreeHand(self.tree_sel_row)
        vbox2.add(self.tree.stree)
        
        #vbox2.add(self.area2)
        self.area3 = gtk.DrawingArea()
        vbox2.add(self.area3)
        
        self.hbox2.add(vbox2)
        vbox.pack_start(self.hbox2)
        
        self.buttons(hbox, window)
        self.buttons2(hbox2, window)
        
        vbox.pack_start(hbox, False)
        vbox.pack_start(hbox2, False)
        window.add(vbox)
        
        # Move to current monitor corner
        xxx, yyy = window.get_position()
        #print xxx, yyy
        
        window.move(xxx, 65)
    
    # --------------------------------------------------------------------
    # Load image
    
    def load(self, fname):
    
        disp = gtk.gdk.display_get_default()
        scr = disp.get_default_screen()
        ptr = disp.get_pointer()
        mon = scr.get_monitor_at_point(ptr[1], ptr[2])
        geo = scr.get_monitor_geometry(mon)   
        www = geo.width; hhh = geo.height
        
        # Resort to old means of getting screen w / h
        if www == 0 or hhh == 0:
            www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
            
        #print www, hhh
        self.wwww = 3 * www / 4;  self.hhhh = 3 * hhh / 4
        
        self.image = gtk.Image()
        self.image.set_from_file(fname)
        
        pix = self.image.get_pixbuf()
        iww = pix.get_width(); ihh = pix.get_height()
        rww = float(iww) / self.wwww;  rhh = float(ihh) / self.hhhh
        aspect = float(iww) / ihh
        #print aspect
        
        # Scale down, keep size
        if aspect > 1: 
            ahh = int(self.wwww * ihh / iww); 
            aww = self.wwww
        else:
            ahh = self.hhhh
            aww = int(self.hhhh * iww / ihh); 
            
        #print self.wwww, self.hhhh, iww, ihh, rww, rhh, aww, ahh
        self.area.set_size_request(aww, ahh)
        
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,      
                True, 8, aww, ahh)                
                                                              
        self.area.image2 = gtk.Image()                         
        self.area.image2.set_from_pixbuf(pixbuf)                
        self.area.image = self.image                            
        self.area.get_img()
        
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

        self.spacer(hbox, True )
        
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
        fname = pyimgutils.ofd("Open Image File").result
        if not fname:
            return
        try:
            self.load(fname)
        except:
            pyimgutils.msg("Cannot load file:\n%s" % fname)
        
    def save_image(self, arg, ww):
        fname = pyimgutils.ofd("Save Image File", 
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
            pyimgutils.msg("Cannot save file:\n%s" % fname)
        
    def anal_image(self, win, a3):
        self.area.anal_image()
                
    def refr_image(self, arg, ww):
        self.area.get_img()
        self.area.invalidate()
        
    def invalidate(self):
        self.area.invalidate()
        
    def  area_button(self, win, event):
        #print "main", event
        pass     
        
    def clear_annote(self, win, a3):     
        self.area.clear_annote()
        
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




