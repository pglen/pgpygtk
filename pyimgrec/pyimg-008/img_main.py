#!/usr/bin/env python

import os, sys, getopt, signal, array
import gobject, gtk, pango, time, random

import  flood
import  flood_diff

import  pyimgrec.imgrec as imgrec
#import  treehand

MAG_SIZE    = 300
DIVIDER     = 32                    # How many divisions
TRESH       = 20                    # Color difference

# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        gtk.main_iteration_do(False)        

# ------------------------------------------------------------------------

class img_main(gtk.DrawingArea):
    
    def __init__(self, wwww, hhhh):
        
        gtk.DrawingArea.__init__(self);
        
        #self.divider = DIVIDER; 
        self.divider = hhhh-1; 
        self.wwww = wwww; self.hhhh = hhhh
        self.set_size_request(wwww, hhhh)
        
        self.annote = []; self.aframe = []; self.atext = []    
        
        self.mag = False 
        self.event_x = self.event_y = 0
        self.image = None
        self.colormap = gtk.widget_get_default_colormap()
                
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
         
         #self.area.set_events(gtk.gdk.ALL_EVENTS_MASK)

        self.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )

        self.connect("key-press-event", self.key_press_event)        
        self.connect("button-press-event", self.area_button)        
        self.connect("expose-event", self.expose)
        self.connect("motion-notify-event", self.area_motion)
        
    def add_to_dict(self, xdic, hor, ver, med):
        try:
            xdic[hor][ver] = med
        except KeyError:
            xdic[hor] = {}
            xdic[hor][ver] = med
        except:
            print sys.exc_info()
            
    def area_motion(self, area, event):    
        #print  event.x, event.y
        if self.mag:
            self.event_x = event.x
            self.event_y = event.y
            self.invalidate()

    # Paint the image
    def expose(self, area, a3):
    
        rc = self.get_allocation()
        self.stepx = rc.width/self.divider; 
        self.stepy = rc.height/self.divider;
        
        winn = self.window
        #rc = area.get_allocation()
        gc = gtk.gdk.GC(winn);
        #colormap = gtk.widget_get_default_colormap()        
        winn.draw_pixbuf( gc, self.image2.get_pixbuf(), 0, 0, 0, 0)
     
        # Paint annotations:
        for xx, yy, txt in self.atext:
            self.pangolayout.set_text(txt)
            winn.draw_layout(gc, xx, yy, self.pangolayout) 
    
        colormap = gtk.widget_get_default_colormap() 
        
        for xx, yy, col in self.aframe:
            gc.set_foreground(colormap.alloc_color("#%06x" % (col & 0xffffff) ))
            winn.draw_rectangle(gc, False, xx*self.stepx, yy*self.stepy,
                                self.stepx, self.stepy)
            #winn.draw_line(gc, xx*self.stepx, yy*self.stepy,
            #                    (xx+1)*self.stepx, (yy+1)*self.stepy)
            
        for xx, yy, func in self.annote:
            func(winn)
            
        if self.mag:
            print  "paint mag:", self.event_x, self.event_y
            
            iw2 = self.image2.get_pixbuf().get_width()
            ih2 = self.image2.get_pixbuf().get_height()
            #print "mag", iw2, ih2
            mags = MAG_SIZE    
            rendx =  self.event_x - mags/2; 
            if rendx < 0: rendx = 0
            rendy =  self.event_y - mags/2; 
            if rendy < 0: rendy = 0
            src_x = self.event_x  / self.scalef - mags/2
            if src_x < 0: src_x = 0
            src_y = self.event_y  / self.scalef - mags/2 
            if src_y < 0: src_y = 0
            magsx = mags
            if rendx + magsx > self.wwww: magsx = self.wwww - rendx
            magsy = mags
            if rendy + magsy > self.hhhh: magsh = self.hhhh - rendy

            print int(src_x), int(src_y), int(rendx), int(rendy), \
                            int(magsx), int(magsy)
            
            winn.draw_pixbuf(gc, self.image.get_pixbuf(), 
                        int(src_x), int(src_y), int(rendx), int(rendy),  \
                            int(magsx), int(magsy))
   
    # --------------------------------------------------------------------
    def key_press_event(self, win, event):
    
        #print "img key_press_event", win, event
        if event.state & gtk.gdk.MOD1_MASK:       
            if event.keyval == gtk.keysyms.x or event.keyval == gtk.keysyms.X:
                sys.exit(0) 
                           
        if event.keyval == gtk.keysyms.Escape:
            self.mag = False 
            self.invalidate()
         
    def clear_annote(self):     
        self.annote = []
        self.atext = []
        self.aframe = []
        self.invalidate()

    def  area_button(self, win, event):
        rc = self.get_allocation()
        #print "img button", event.x, event.y, rc.width, rc.height
        stepx = rc.width/self.divider; stepy = rc.height/self.divider;
        #print event.x / stepx,      event.y / stepy
        self.anal_image(int(event.x / stepx), int(event.y / stepy))
        pass    
       
    def toggle_mag(self):
        print "toggle_mag"
        self.mag = not self.mag
        if self.mag and self.event_x == 0:
            rc = self.get_allocation()
            self.event_x = rc.width/2; self.event_y = rc.height/2
        self.invalidate()

    def invalidate(self):
        winn = self.window
        ww, hh = winn.get_size()
        rect = gtk.gdk.Rectangle(0, 0, ww, hh)
        winn.invalidate_rect(rect, False)
    
    # Refresh image from original    
    def get_img(self):
        iw = self.image.get_pixbuf().get_width()
        ih = self.image.get_pixbuf().get_height()
        ww, hh = self.get_size_request()
        if iw > ih:  
            self.scalef = float(ww)/iw
        else:        
            self.scalef = float(hh)/ih
            iww = iw * scalef
            
        #print "Image Size:", iw, ih, "Window Size:", ww, hh, "Scale:", self.scalef
        
        self.image.get_pixbuf().scale(self.image2.get_pixbuf(), 0, 0, ww, hh, 
                            0, 0, self.scalef, self.scalef, gtk.gdk.INTERP_TILES)  
    
    # --------------------------------------------------------------------            
    # Using an arrray to manipulate the underlying buffer
    
    def anal_image(self, xxx = -1, yyy = -1):
    
        # Get img props.
        pixb =  self.image2.get_pixbuf()
        iw = pixb.get_width(); ih = pixb.get_height()
        #print "img dim", iw, ih
        
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            arr = pixb.get_pixels_array()
            
        #imgrec.verbose = 1
        imgrec.anchor(arr)
        
        #print "dims", imgrec.dim1, imgrec.dim2, imgrec.dim3
        #print "width", imgrec.width, "height", imgrec.height
        
        hstep = imgrec.width / self.divider; vstep = imgrec.height / self.divider
        
        # Interpret defaults:
        if xxx == -1: xxx = self.divider/2
        if yyy == -1: yyy = self.divider/2

        print "Anal image", xxx, yyy, hstep, vstep
        
        # Draw grid 
        '''for xx in range(self.divider):
            hor = xx * hstep
            imgrec.line(hor, 0, hor, imgrec.height, 0xff888888)
        for yy in range(self.divider):
            ver = yy * vstep
            imgrec.line(0, ver, imgrec.width, ver, 0xff888888)'''
        
        # Get an array of median values
        xcnt = 0; ycnt = 0; darr = {}; 
        for yy in range(self.divider):
            xcnt = 0
            for xx in range(self.divider):
                hor = xx * hstep; ver = yy * vstep
                med = imgrec.median(hor, ver, hor + hstep, ver + vstep)
                #imgrec.blank(hor, ver, hor + hstep, ver + vstep, med)
                med &= 0xffffff;  # Mask out alpha
                
                # Remember it in a dict
                self.add_to_dict(darr, xcnt, ycnt, med)
                xcnt += 1
            ycnt += 1; 
                    
        # Set up flood fill
        fparm = flood.floodParm(self.divider, darr);
        fparm.hstep = hstep; fparm.vstep = vstep
        fparm.tresh = TRESH               
        
        # Progress feedback
        fparm.inval = self.show_prog;    
        fparm.colx = int(random.random() * 0xffffff) 
        flood.flood(xxx, yyy, fparm)
        #flood_diff.flood_diff(xxx, yyy, fparm)
        
        # Reference position
        self.aframe.append((xxx, yyy, 0x0000ff))
        #print "ref", xxx, yyy
        
        # Display final image
        self.show_prog(fparm)
        self.invalidate()
        
    def show_prog(self, fparm):
        rc = self.get_allocation()
        minx =  rc.width;  miny = rc.height;  maxx = maxy = 0
        #print "Showing progress:"
        for aa in fparm.spaces.keys():
            #print aa,
            if fparm.spaces[aa]:
                self.aframe.append((aa[0], aa[1], fparm.colx))
                if minx > aa[0]: minx = aa[0]
                if miny > aa[1]: miny = aa[1]
                if maxx < aa[0]: maxx = aa[0] 
                if maxy < aa[1]: maxy = aa[1]
                 
        #print "inval", minx * self.stepx, miny * self.stepy,  \
        #                (maxx + 1)* self.stepx, (maxy+1) * self.stepy
        rect = gtk.gdk.Rectangle(minx * self.stepx, miny * self.stepy, 
                        (maxx + 1) * self.stepx, (maxy + 1)  * self.stepy)
        self.window.invalidate_rect(rect, False)
        
        #self.invalidate()
        usleep(.01)

