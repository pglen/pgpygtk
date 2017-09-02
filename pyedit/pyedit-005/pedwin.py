#!/usr/bin/env python

import signal, os, time, sys
import gobject, gtk, gconf

import peddoc
import pedconfig
from pedmenu import *
from pedui import *
from pedutil import *

UNTITLED = "untitled.txt"

#actionx = None; arg1 = None; arg2 = None
treestore = None
      
def scroll(aa, bb):
    print aa, bb

# -----------------------------------------------------------------------
# Create document

class edPane(gtk.VPaned):  

    def __init__(self, buff, focus = False):

        pos = gconf.client_get_default().get_int("/apps/pyedit/vpaned")
        if pos == 0: pos = 120

        gtk.VPaned.__init__(self)
        self.set_border_width(5)
        self.set_position(pos)
        self.vbox = edwin(buff, True); 
        self.add2(self.vbox)           
        self.vbox2 = edwin(buff, False, True)
        self.add1(self.vbox2)   
        self.area = self.vbox.area
        
# -----------------------------------------------------------------------
# Create main document widget window with scroll bars

class edwin(gtk.VBox):

    def __init__(self, buff, focus = False, readonly = False):
        
        global notebook, mained

        gtk.VBox.__init__(self)

        area  = peddoc.pedDoc(buff, mained, focus, readonly)        
        #print "created", area, mained
        
        # Give access to nb
        area.notebook = notebook
        area.mained = mained
                       
        frame = gtk.Frame(); frame.add(area)        
        hbox = gtk.HBox()
        hbox.pack_start(frame, True, True)
        hbox.pack_end(area.vscroll, False, False)        

        self.pack_start(hbox, True, True)
        self.pack_end(area.hscroll, False, False)

        # Make it acessable:
        self.area = area

# ------------------------------------------------------------------------
#  Define Application Main Window claass

class EdMainWindow():
    
    def __init__(self, fname, parent, names):
    
        self.statuscount = 0
        self.alt = False
        register_stock_icons()

        global mained
        mained = self

        # Create the toplevel window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window = window

        window.set_position(gtk.WIN_POS_CENTER)
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
      
        if pedconfig.pedconfig.full_screen:
            window.set_default_size(www, hhh)
        else: 
            window.set_default_size(7*www/8, 5*hhh/8)
            window.move(www / 32, hhh / 10)        

        window.set_icon_from_file(get_img_path("pyedit.png"))
        merge = gtk.UIManager()
        window.set_data("ui-manager", merge)
        merge.insert_action_group(create_action_group(self), 0)
        window.add_accel_group(merge.get_accel_group())
        
        try:
            mergeid = merge.add_ui_from_string(ui_info)
        except gobject.GError, msg:
            print "Building menus failed: %s" % msg

        bar = merge.get_widget("/MenuBar")
        bar.show()

        window.set_events(    gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )

        window.connect("window_state_event", self.update_resize_grip)
        window.connect("destroy", OnExit)

        window.connect("key-press-event", self.area_key)
        window.connect("key-release-event", self.area_key)

        #window.connect("set-focus", self.area_focus)
        window.connect("focus-in-event", self.area_focus_in)
        window.connect("focus-out-event", self.area_focus_out)

        #window.connect("area-focus-event", self.area_focus_in)
        #window.connect("event", self.area_event)
        #window.connect("enter-notify-event", self.area_enter)
        #window.connect("leave-notify-event", self.area_leave)
        window.connect("delete-event", self.unmap)
        
        global notebook
        
        # Create note for the main window, give access to it for all
        notebook = gtk.Notebook()
        notebook.popup_enable()
        notebook.set_scrollable(True)

        #notebook.add_events(gtk.gdk.FOCUS_CHANGE_MASK)
        notebook.add_events(gtk.gdk.ALL_EVENTS_MASK)

        notebook.connect("switch-page", self.note_swpage_cb)
        notebook.connect("focus-in-event", self.note_focus_in)

        # Futile attempts        
        #notebook.connect("change-current-page", self.note_page_cb)
        #notebook.connect("grab-focus", self.note_grab_focus_cb)        
        #notebook.connect("focus", self.note_focus_cb)
        #notebook.connect("create-window", self.note_create_cb)
        #notebook.connect("enter-notify-event", self.note_enter_notify)

        table = gtk.Table(2, 4, False)
        window.add(table)

        table.attach(bar,
            # X direction #          # Y direction
            0, 1,                      0, 1,
            gtk.EXPAND | gtk.FILL,     0,
            0,                         0);

        bar = merge.get_widget("/ToolBar"); bar.set_tooltips(True)
        bar.show()
        table.attach(bar,
            # X direction #       # Y direction
            0, 1,                   1, 2,
            gtk.EXPAND | gtk.FILL,  0,
            0,                      0)
        
        hpaned = gtk.HPaned(); hpaned.set_border_width(5)      
        
        scroll = gtk.ScrolledWindow()
        treeview = self.create_tree()
        treeview.connect("row-activated",  self.tree_sel)
        treeview.connect("cursor-changed",  self.tree_sel_row)
        self.treeview = treeview

        scroll.add(treeview)
        frame2 = gtk.Frame(); frame2.add(scroll)
        hpaned.add(frame2)
        
        self.hpanepos = gconf.client_get_default().get_int("/apps/pyedit/hpaned")
        if self.hpanepos == 0: self.hpanepos = 200
        hpaned.set_position(self.hpanepos)
        hpaned.pack2(notebook)
        self.hpaned = hpaned

        # Create statusbars
        self.statusbar = gtk.Statusbar()
        self.statusbar2 = gtk.Statusbar()
        hpane2 = gtk.HPaned()
        
        hpane2.set_position(self.get_width() - 200)
        hpane2.pack2(self.statusbar2)
        hpane2.pack1(self.statusbar)

        cnt = 0    
        # Read in buffers
        for aa in names:    
            #print "loading file: ", aa
            try:            
                buff = readfile(aa)
                cnt += 1
            except:
                print "Cannot read file '" + aa , "'"
                continue
            
            vpaned = edPane(buff)
            #vpaned.fname = os.path.realpath(aa)
            vpaned.area.fname = os.path.realpath(aa)
            notebook.append_page(vpaned)               
            #hbox = gtk.HBox()
            #img = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_DIALOG)
            label = gtk.Label(" " + os.path.basename(aa) + " ")
            #hbox.pack_start(label)
            #hbox.pack_end(img)
            notebook.set_tab_label(vpaned, label)
            
        if cnt == 0:
            #print "No valid file on command line, creating new", os.getcwd()
            aa = UNTITLED
            vpaned = edPane([])
            #vpaned.fname = os.path.realpath(aa)
            vpaned.area.fname = os.path.realpath(aa)
            notebook.append_page(vpaned)                           
            label = gtk.Label(" " + os.path.basename(aa) + " ")
            notebook.set_tab_label(vpaned, label)
        
        # Main Pane
        table.attach(hpaned,
            # X direction           Y direction
            0, 1,                   2, 3,
            gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            0,                      0)
        table.attach(hpane2,
        #table.attach(self.statusbar,
            # X direction           Y direction
            0, 1,                   3, 4,
            gtk.EXPAND | gtk.FILL,  0,
            0,                      0)
        window.show_all()

        # Set the signal handler for 1s tick
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(1)
        self.update_statusbar("Initial")

    def unmap(self):
        print "unmap"
    # --------------------------------------------------------------------
    def tree_sel_row(self, xtree):
        sel = xtree.get_selection()
        xmodel, xiter = sel.get_selected()
        xstr = xmodel.get_value(xiter, 0)        
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        vcurr.area.locate(xstr)
   
    def tree_sel(self, xtree, xiter, xpath):
        pass
        print "tree_sel", xtree, xiter, xpath
        # Focus on main doc
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        self.window.activate_focus()
        self.window.set_focus(vcurr.vbox.area)

    # Call key handler
    def area_key(self, area, event):
        pass
        # Inspect key press before treeview gets it
        if self.window.get_focus() == self.treeview:
            # Do key down:
            if  event.type == gtk.gdk.KEY_PRESS:
                if event.keyval == gtk.keysyms.Alt_L or \
                        event.keyval == gtk.keysyms.Alt_R:
                    self.alt = True;

                if event.keyval >= gtk.keysyms._1 and event.keyval <= gtk.keysyms._9:
                    print "pedwin Alt num", event.keyval - gtk.keysyms._1
                     # Focus on main doc
                    vcurr = notebook.get_nth_page(notebook.get_current_page())
                    self.window.set_focus(vcurr.vbox.area)
                               
            elif  event.type == gtk.gdk.KEY_RELEASE:
                if event.keyval == gtk.keysyms.Alt_L or \
                      event.keyval == gtk.keysyms.Alt_R:
                    self.alt = False;
            
    def get_height(self):
        xx, yy = self.window.get_size()
        return yy

    def get_width(self):
        xx, yy = self.window.get_size()
        return xx

    def start_tree(self):

        global treestore

        if not treestore:
            treestore = gtk.TreeStore(str)
        
        # Delete previous contents
        try:      
            while True:
                root = treestore.get_iter_first() 
                if not root:
                    break 
                treestore.remove(root)                           
        except:
            print  "strt_tree", sys.exc_info()
            pass
        
        piter = treestore.append(None, ["Extracting .."])
        treestore.append(piter, ["None .."])

    # --------------------------------------------------------------------
    def create_tree(self, text = None):
        
        global treestore
        self.start_tree()
        
        # create the TreeView using treestore
        tv = gtk.TreeView(treestore)

        # create a CellRendererText to render the data
        cell = gtk.CellRendererText()

        # create the TreeViewColumn to display the data
        tvcolumn = gtk.TreeViewColumn('Functions')

        # add the cell to the tvcolumn and allow it to expand
        tvcolumn.pack_start(cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        tvcolumn.add_attribute(cell, 'text', 0)
        
        # add tvcolumn to treeview
        tv.append_column(tvcolumn)
    
        return tv

    # --------------------------------------------------------------------
    def update_treestore(self, text):

        global treestore
        # Delete previous contents
        try:      
            while True:
                root = treestore.get_iter_first()
                if not root:
                    break 
                treestore.remove(root)                           
        except:
            print  "update_tree", sys.exc_info()
            pass
        
        if not text:
            return
        
        try:
            for line in text:
                piter = treestore.append(None, [cut_lead_space(line)])
        except:
            pass
            #print  sys.exc_info()
    # --------------------------------------------------------------------
    # Handlers:

    def area_event(self, win, act):
        print  "pedwin area event", win, act   

    def area_leave(self, win, act):
        pass
        #print  "pedwin area leave", win, act   
    
    def area_enter(self, win, act):
        pass
        #print  "pedwin area enter", win, act   
   
    def area_focus(self, win, act):
        pass
        #print  "pedwin area focus", win, act   

    def area_focus_in(self, win, act):
        #print  "area focus in", win, act   
        # This was needed as pygtk leaves the alt key hanging
        pedconfig.pedconfig.keyh.reset()        
        # Focus on main doc
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        self.window.set_focus(vcurr.vbox.area)

    def area_focus_out(self, win, act):
        pass
        #print  "area focus out", win, act   
         
    # Note message handlers:
   
    def  note_focus_in(self, win, act):
        pass
        #print "note_focus_in", win, act
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        self.window.set_focus(vcurr.vbox.area)
        
    def note_enter_notify(self, win):
        pass
        #print "note_enter_notify", win

    def  note_grab_focus_cb(self, win):
        #print "note_grab_focus_cb", win
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        self.window.set_focus(vcurr.vbox.area)
        
    def  note_swpage_cb(self, tabx, page, num):
        #print "note_swpage", num
        vcurr = tabx.get_nth_page(num)
        self.window.set_title("pyedit: " + vcurr.area.fname);
        self.window.set_focus(vcurr.vbox.area)        
        self.update_statusbar("Switched to '{1:s}'".
                                format(num, vcurr.area.fname))
                
    def  note_page_cb(self, tabx, child, num):
        pass
        #print "note_page"

    def  note_focus_cb(self, tabx, foc):
        #print "note_focus_cb"
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        self.window.set_focus(vcurr.vbox.area)
       
    def  note_create_cb(self, tabx, page, xx, yy):
        pass
        #print "note_create"

    # Note message handlers end
    def activate_qhelp(self, action):
        self.update_statusbar("Showing quick help")        
        pid = os.spawnlp(os.P_NOWAIT, "/usr/bin/pangview.py", "pangview", "README")
                    
    
    def activate_about(self, action):
        self.update_statusbar("Showing About Dialog")        
        dialog = gtk.AboutDialog()
        dialog.set_name("PyEdit - Python Editor")
        dialog.set_version("1.0");
        dialog.set_comments("\nPython based configurable editor\n");
        dialog.set_copyright("\302\251 Copyright Peter Glen")

        img_dir = os.path.join(os.path.dirname(__file__), 'images')
        img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')

        try:
	        pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)
            #print "loaded pixbuf"
                dialog.set_logo(pixbuf)
    
        except gobject.GError, error:
            print "Cannot load logo for about dialog";

        #dialog.set_website("")
        ## Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def activate_action(self, action):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
            'You activated action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def activate_quit(self, action):
        #print "activate_quit called"        
        OnExit(self.window)
                 
    def activate_radio_action(self, action, current):
        active = current.get_active()
        value = current.get_current_value()

        if active:
            dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
                "You activated radio action: \"%s\" of type \"%s\".\nCurrent value: %d" %
                (current.get_name(), type(current), value))

            # Close dialog on user response
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.show()

    def update_statusbar2(self, xx = 0, yy = 0):
        # Always update line / col
        strx2 = "Ln: {0:d}   Col: {1:d}".format(yy, xx)
        self.statusbar2.pop(0)
        self.statusbar2.push(0, strx2)
       
    def update_statusbar(self, strx):
        # Clear any previous message, underflow is allowed
        self.statusbar.pop(0)
        if not strx: 
            self.statusbar.push("Idle")
            return

        self.statusbar.push(0, strx)
        self.statuscount = 3
        pass

    def update_resize_grip(self, widget, event):
        #print "update state", event, event.changed_mask
        #self.window.set_focus(notebook)
 
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED | gtk.gdk.WINDOW_STATE_FULLSCREEN
        if (event.changed_mask & mask):
            self.statusbar.set_has_resize_grip(not (event.new_window_state & mask))

def OnExit(arg):

    arg.set_title("Exiting ...")

    # Save UI related data
    pos = mained.hpaned.get_position()
    pos = max(pos, 1)
    gconf.client_get_default().set_int\
                    ("/apps/pyedit/hpaned", pos)    

    firstpage = notebook.get_nth_page(0)
    if firstpage:
        pos = firstpage.get_position()
        pos = max(pos, 1)
        gconf.client_get_default().set_int\
                    ("/apps/pyedit/vpaned", pos)    
    
    # Prompt for save files
    global notebook        
    nn = notebook.get_n_pages(); cnt = 0
    while True:
        if cnt >= nn: break
        ppp = notebook.get_nth_page(cnt)
        #print "page:", ppp.area
        if ppp.area.changed:
            ppp.area.prompt_save()
        cnt += 1 

        # Exit here
        gtk.main_quit()

    #print "OnExit called \"" + arg.get_title() + "\""
    
def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    
    if pedconfig.pedconfig.pedwin.statuscount:
        pedconfig.pedconfig.pedwin.statuscount -= 1
        if pedconfig.pedconfig.pedwin.statuscount == 0:
            pedconfig.pedconfig.pedwin.update_statusbar("Idle");            
            pedconfig.pedconfig.pedwin.statuscount = 0 
    signal.alarm(1)


