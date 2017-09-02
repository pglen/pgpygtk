#!/usr/bin/env python

import gtk

disp = gtk.gdk.display_get_default()
scr = disp.get_default_screen()

#print "num_mon",  scr.get_n_monitors()    
#for aa in range(scr.get_n_monitors()):    
#    print "mon", aa, scr.get_monitor_geometry(aa);
    

# ------------------------------------------------------------------------
# Get current screen (monitor) width and height

def get_screen_wh():

    ptr = disp.get_pointer()
    mon = scr.get_monitor_at_point(ptr[1], ptr[2])
    geo = scr.get_monitor_geometry(mon)
    www = geo.width; hhh = geo.height
    if www == 0 or hhh == 0:
        www = gtk.gdk.get_screen_width();
        hhh = gtk.gdk.get_screen_height();
    return www, hhh    

# ------------------------------------------------------------------------
# Get current screen (monitor) upper left corner xx / yy

def get_screen_xy():

    ptr = disp.get_pointer()
    mon = scr.get_monitor_at_point(ptr[1], ptr[2])
    geo = scr.get_monitor_geometry(mon)
    return geo.x, geo.y


