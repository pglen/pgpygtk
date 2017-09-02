#!/usr/bin/env python

# Action Handler for find

import  time, datetime
import gtk

import peddoc, pedync, pedconfig

from pedutil import *

# Adjust to taste. Estimated memory usage is 50 * MAX_LOG bytes
# Fills up slowly, so not a big issue. Delete ~/.pyedit/pylog.txt if 
# you would like to free the memory used by log
MAX_LOG  = 2000


accum = []

# Print as 'print' would, but replicate to log. This class replicate stdout
# and replicates stdout to regular fd, and puts an entry onto accum.

class fake_stdout():

    def __init__(self):
        self.old_stdout = os.fdopen(sys.stdout.fileno(), "w")
        self.flag = True
        self.dt = datetime.datetime(1990, 1, 1);

    def write(self, *args):
        global accum
        strx = ""
        if self.flag:
            dt2 = self.dt.now()
            strx =  dt2.strftime("%d/%m/%y %H:%M:%S ")
            self.flag = False 
        
        for aa in args:
            if type(aa) == 'tuple':
                for bb in aa:
                    self.old_stdout.write(str(bb) + " ")
                    strx += str(bb)
            else: 
                self.old_stdout.write(str(aa))
                strx +=  str(aa)   
        
        if strx.find("\n") >= 0:
            self.flag = True 
            
        accum.append(strx)
        self.limit_loglen()       

    def limit_loglen(self):
        global accum
        xlen = len(accum)
        if xlen == 0: return
        if xlen  <  MAX_LOG: return
        self.old_stdout.write("limiting loglen " + str(xlen))
        for aa in range(MAX_LOG / 5):
            try:
                del (accum[0])
            except:
                pass

# Persistance for logs. Disable if you wish.

def  save_log():
    pass
    
def load_log():
    pass
                        
# A quick window to dispat what is in accum
                    
def show_log():
    
    win2 = gtk.Window()
    try:
        win2.set_icon_from_file(get_img_path("pyedit_sub.png"))
    except:
        print( "Cannot load log icon")

    win2.set_position(gtk.WIN_POS_CENTER)
    win2.set_default_size(800, 600)
    
    tit = "pyedit:log"        
    win2.set_title(tit)
    
    win2.set_events(    
                    gtk.gdk.POINTER_MOTION_MASK |
                    gtk.gdk.POINTER_MOTION_HINT_MASK |
                    gtk.gdk.BUTTON_PRESS_MASK |
                    gtk.gdk.BUTTON_RELEASE_MASK |
                    gtk.gdk.KEY_PRESS_MASK |
                    gtk.gdk.KEY_RELEASE_MASK |
                    gtk.gdk.FOCUS_CHANGE_MASK )

    win2.connect("key-press-event", area_key, win2)
    win2.connect("key-release-event", area_key, win2)

    win2.lab = gtk.TextView()
    win2.lab.set_editable(False)
    tb = win2.lab.get_buffer()
    iter = tb.get_iter_at_offset(0)
    global accum
    for aa in accum:
        tb.insert(iter, aa)
    
    scroll = gtk.ScrolledWindow(); scroll.add(win2.lab)
    frame = gtk.Frame(); frame.add(scroll)
    win2.add(frame)
    win2.show_all()
    
# ------------------------------------------------------------------------

def area_key(area, event, dialog):

    if  event.type == gtk.gdk.KEY_PRESS:
        if event.keyval == gtk.keysyms.Escape:
            #print "Esc"
            area.destroy()

    if  event.type == gtk.gdk.KEY_PRESS:
        if event.keyval == gtk.keysyms.Return:
            #print "Ret"
            area.destroy()

        if event.keyval == gtk.keysyms.Alt_L or \
                event.keyval == gtk.keysyms.Alt_R:
            area.alt = True;
            
        if event.keyval == gtk.keysyms.x or \
                event.keyval == gtk.keysyms.X:
            if area.alt:
                area.destroy()
                              
    elif  event.type == gtk.gdk.KEY_RELEASE:
        if event.keyval == gtk.keysyms.Alt_L or \
              event.keyval == gtk.keysyms.Alt_R:
            area.alt = False;











































































































