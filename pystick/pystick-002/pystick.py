#!/usr/bin/env python

import os, sys, getopt, signal
import gobject, gtk, pango

import random, time
import yellow, treehand, sticked, pysql

# ------------------------------------------------------------------------
# This is open source sticker program. Written in python. 

version = 1.0
verbose = False
xstr = ""

# Where things are stored (backups, orgs, macros)
config_dir = os.path.expanduser("~/.pystick")

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

# ------------------------------------------------------------------------

class MainWin():

    def __init__(self):
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Python Stickies")
        window.set_position(gtk.WIN_POS_CENTER)
        
        #ic = gtk.Image(); ic.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_BUTTON)
        #window.set_icon(ic.get_pixbuf())
        
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
        window.set_default_size(www/2, hhh/2)
        
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
         
        window.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )
         
        # W1           
        window.connect("destroy", self.OnExit)
        window.connect("key-press-event", self.key_press_event)        
        window.connect("button-press-event", self.area_button)        
        
        window.set_icon_from_file("icon.png")
        
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        
        lab1 = gtk.Label("");  hbox.pack_start(lab1)
        
        tree = treehand.TreeHand(self.tree_sel_row)
        self.tree = tree
        vbox.pack_start(tree.stree)
        
        butt1 = gtk.Button(" _New Sticky ")
        butt1.connect("clicked", self.show_new, window)
        hbox.pack_start(butt1, False)
        
        butt1d = gtk.Button(" _Edit Sticky ")
        butt1d.connect("clicked", self.edit_stick, window)
        hbox.pack_start(butt1d, False)
        
        butt2 = gtk.Button(" _Search ")
        butt2.connect("clicked", self.search, window)
        hbox.pack_start(butt2, False)
    
        butt22 = gtk.Button(" Show _All ")
        butt22.connect("clicked", self.show_all_sticks, window)
        hbox.pack_start(butt22, False)
        
        butt21 = gtk.Button(" Show _One ")
        butt21.connect("clicked", self.show_one, window)
        hbox.pack_start(butt21, False)
        
        lab2 = gtk.Label("");  hbox.pack_start(lab2)
        vbox.pack_start(hbox, False)
        
        hbox2 = gtk.HBox()
        
        lab3 = gtk.Label("");  hbox2.pack_start(lab3)
        
        butt3 = gtk.Button(" _Hide All ")
        butt3.connect("clicked", self.hide_all, window)
        hbox2.pack_start(butt3, False)
    
        butt31 = gtk.Button(" H_ide One ")
        butt31.connect("clicked", self.hide_one, window)
        hbox2.pack_start(butt31, False)
        
        butt43 = gtk.Button(" _Delete One ")
        butt43.connect("clicked", self.del_one, window)
        hbox2.pack_start(butt43, False)
        
        butt4 = gtk.Button(" Hide _Main ")
        butt4.connect("clicked", self.hide_main, window)
        hbox2.pack_start(butt4, False)
        
        butt41 = gtk.Button(" _Keep Above ")
        butt41.connect("clicked", self.above_one, window)
        hbox2.pack_start(butt41, False)
        
        butt5 = gtk.Button(" E_xit ")
        butt5.connect("clicked", self.exit_all)
        hbox2.pack_start(butt5, False)
    
        lab4 = gtk.Label("");  hbox2.pack_start(lab4)
        vbox.pack_start(hbox2, False)
        window.add(vbox)
        
    def exit_all(self, area):
        gtk.main_quit()

    def next(self, org):
        print "next", org.head
                    
    def show_all_sticks(self, area, me):
        rr = stickdb.getheads()
        for bb in rr:
            if stickdb.getshow(bb[0]):
                found = False 
                for aa in yellow.slist.data:
                    if aa.head == bb[0]:
                        found = True 
                        tt = stickdb.getpos(aa.head)
                        if tt:
                            aa.window.xx = tt[0]; aa.window.yy = tt[1]  
                            
                        aa.window.move(aa.window.xx, aa.window.yy)
                        aa.window.present()
                        yellow.usleep(1)
                        break
                if not found:
                    ss = stickdb.get(bb[0])
                    if ss:
                        aa = yellow.stickWin(window2, ss[1], ss[2])
                        
        #me.present()
    
    def show_one(self, area, me):
        global xstr
        # Already Shown?
        found = False 
        for aa in yellow.slist.data:
            if aa.head == xstr:
                found = True 
                aa.window.move(aa.window.xx, aa.window.yy)
                aa.window.present()
                #aa.window.set_keep_above(True)
                yellow.usleep(1)
                
        if not found:  
            rr = stickdb.get(xstr)
            if rr:
                aa = yellow.stickWin(window2, rr[1], rr[2])
                stickdb.putshow(aa.head, 1)        
        stickdb.putpos(aa.head, aa.window.xx, aa.window.yy)        
                
        #me.present()
        
    def del_one(self, area, me):
        global xstr, mainwin
        for aa in yellow.slist.data:
            if aa.head == xstr:
                aa.window.hide()
        rr = stickdb.getheads()
        for aa in rr: 
            if aa[0] == xstr:
                print "del", aa[0]
                stickdb.rmone(aa[0])
                break
        heads = []
        rr = stickdb.getheads()
        for aa in rr: 
            heads.append(aa[0])
        mainwin.tree.update_treestore(heads)
                             
    def above_one(self, area, me):
        global xstr
        found = False
        rr = stickdb.getheads()
        for aa in yellow.slist.data:
            if aa.head == xstr:
                found = True 
                aa.window.move(aa.window.xx, aa.window.yy)
                aa.window.present()
                aa.window.set_keep_above(True)
                yellow.usleep(1)
                stickdb.putshow(aa.head, 1)        
                
        if not found:        
            rr = stickdb.get(xstr)
            if rr:
                aa = yellow.stickWin(window2, rr[1], rr[2])
                aa.window.set_keep_above(True)
                yellow.usleep(1)
                stickdb.putshow(aa.head, 1)        
            
        me.present()
                             
    def hide_one(self, area, me):
        global xstr
        for aa in yellow.slist.data:
            if aa.head == xstr:
                aa.window.hide()
                yellow.usleep(1)
                stickdb.putshow(aa.head, 0)        
                print "hide", aa.head, stickdb.getshow(aa.head)        
                
        me.present()
    
    def done_dlg(self, dlg):
    
        global window2, stickdb
        head = dlg.head.get_text()
        buff = dlg.text.get_buffer()
        ss = buff.get_start_iter(); ee = buff.get_end_iter()
        text = buff.get_text(ss, ee)
        #print  "done_dlg", head, text
        stickdb.put(head, text)
        stickdb.putshow(head, 1)        
        
        found = False 
        for aa in yellow.slist.data:
            if aa.head == xstr:
                found = True 
                print "update", head, text
                aa.head = head
                aa.text = text
                aa.window.head = head
                aa.window.text = text
                
                aa.invalidate()
                yellow.usleep(1)
                aa.window.show()
                
        if not found:
            print "creating", head
            cc = yellow.stickWin(window2, head, text)
            pp = stickdb.getpos(head)        
            if pp:
                cc.window.xx = pp[0]; cc.window.yy = pp[1]   
            aa.window.move(aa.window.xx, aa.window.yy)
            
        self.window.present()
        
    def edit_stick(self, area, me):
        global xstr, stickdb
        dd = stickdb.get(xstr)
        se = sticked.StickEd(me, self.done_dlg, xstr, dd[1])
        #print "edit_stick", 
     
    def show_new(self, area, me):
        se = sticked.StickEd(me, self.done_dlg)
        #print "new", se
        
    def search(self, area, me):
        print "search"
    
    def hide_all(self, area, me):
        #print "hide_all"
        for aa in yellow.slist.data:
            #gtk.gdk.Window.hide(aa.window.get_window())
            aa.window.hide()
                             
    def hide_main(self, area, me):
        print "hide_main"
        me.iconify()
    
    def area_button(self, area, event):
        #print "main butt"
        return False 
    
    def tree_sel_row(self, xtree):
        #print tree
        global xstr
        sel = xtree.get_selection()    
        xmodel, xiter = sel.get_selected_rows()
        for aa in xiter:
            xstr = xmodel.get_value(xmodel.get_iter(aa), 0)    
            break
    
    def key_press_event(self, area, event):
        #print "main keypress" #, area, event
        '''if event.state & gtk.gdk.MOD1_MASK:       
            if event.keyval == gtk.keysyms.ESC:
                sys.exit(0)    
        '''
        return False

    def OnExit(self, aa):
        gtk.main_quit()
            
            
def key_press_event(win, aa):
    print "key_press_event", win, aa
    
            
# Start of program:

if __name__ == '__main__':

    global mainwin, stickdb
    
    autohide = False 
    
    try:
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    except: pass
    
    # Let the user know it needs fixin'
    if not os.path.isdir(config_dir):
        print "Cannot access config dir:", config_dir
        sys.exit(1)

    stickdb = pysql.sticksql(config_dir + "/data")
    
    for bb in range(12):
        stickdb.put("Hello Sticky %d" % bb, "This is a sticky test body %s" % bb)
    
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
        #if aa[0] == "-x": clear_config = True            
        #if aa[0] == "-c": show_config = True            
        #if aa[0] == "-t": show_timing = True

    if verbose:
        print "PyStick running on", "'" + os.name + "'", \
            "GTK", gtk.gtk_version, "PyGtk", gtk.pygtk_version

    mainwin = MainWin()    
    
    # W2
    global window2
    window2 = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window2.set_title("Python Nowin")
    window2.set_position(gtk.WIN_POS_CENTER)
    #window2.connect("key-press-event", key_press_event)        
    window2.mainwin = mainwin
    
    heads = []
    rr = stickdb.getheads()
    for aa in rr: 
        heads.append(aa[0])
        if stickdb.getshow(aa[0]):
            ss = stickdb.get(aa[0])
            yellow.stickWin(window2, ss[1], ss[2])
        
    mainwin.tree.update_treestore(heads)
    
    for aa in rr: 
        if stickdb.getshow(aa[0]):
            tt = stickdb.getpos(aa[0])
            for bb in yellow.slist.data:
                if aa[0] == bb.head:
                    bb.window.move(tt[0], tt[1])
         
    # For testing
    #rr = stickdb.rmall()
                
    window2.show_all()
    window2.hide()
    mainwin.window.show_all()    
    
    if autohide:
        mainwin.window.iconify()
    gtk.main()






