#!/usr/bin/env python

import signal, os, time, sys
import gobject, gtk, gconf

import peddoc
import pedconfig
from pedmenu import *
from pedui import *
from pedutil import *

STATUSCOUNT = 5             # Length of the styatus bar timeout (in sec)

treestore = None
notebook = None
      
#def scroll(aa, bb):
#    print aa, bb

# -----------------------------------------------------------------------
# Create document

class edPane(gtk.VPaned):  

    def __init__(self, buff, focus = False):

        pos = gconf.client_get_default().get_int(pedconfig.conf.config_reg + "/vpaned")
        if pos == 0: pos = 120

        gtk.VPaned.__init__(self)
        self.set_border_width(5)
        self.set_position(pos)
        self.vbox = edwin(buff, True); 
        self.add2(self.vbox)           
        self.vbox2 = edwin(buff, False, True)
        self.add1(self.vbox2)   
        
        # Shortcuts to access the editor windows
        self.area  = self.vbox.area
        self.area2 = self.vbox2.area
        
# -----------------------------------------------------------------------
# Create main document widget window with scroll bars

class edwin(gtk.VBox):

    def __init__(self, buff, focus = False, readonly = False):
        
        global notebook, mained

        gtk.VBox.__init__(self)

        area  = peddoc.pedDoc(buff, mained, focus, readonly)        
        #print "created", area, mained
        
        # Give access to notebook and main editor window
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
    
        self.full = False
        self.statuscount = 0
        self.alt = False
        register_stock_icons()

        global mained
        mained = self

        # Create the toplevel window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window = window
        
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();

        if pedconfig.conf.full_screen:
            window.set_default_size(www, hhh)
        else: 
            xx = gconf.client_get_default().get_int(pedconfig.conf.config_reg + "/xx")    
            yy = gconf.client_get_default().get_int(pedconfig.conf.config_reg + "/yy")    

            ww = gconf.client_get_default().get_int(pedconfig.conf.config_reg + "/ww")    
            hh = gconf.client_get_default().get_int(pedconfig.conf.config_reg + "/hh")    
    
            if ww == 0 or hh == 0:
                window.set_position(gtk.WIN_POS_CENTER)
                window.set_default_size(7*www/8, 5*hhh/8)
                window.move(www / 32, hhh / 10)                
            else:
                window.set_default_size(ww, hh)
                window.move(xx, yy)        
        
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

        window.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )

        #window.set_events(  gtk.gdk.ALL_EVENTS_MASK)
        
        window.connect("window_state_event", self.update_resize_grip)
        window.connect("destroy", OnExit)

        window.connect("key-press-event", self.area_key)
        window.connect("key-release-event", self.area_key)

        #window.connect("set-focus", self.area_focus)
        window.connect("focus-in-event", self.area_focus_in)
        window.connect("focus-out-event", self.area_focus_out)
        window.connect("window-state-event", self.area_winstate)

        #window.connect("area-focus-event", self.area_focus_in)
        #window.connect("event", self.area_event)
        #window.connect("enter-notify-event", self.area_enter)
        #window.connect("leave-notify-event", self.area_leave)
        #window.connect("event", self.unmap)
        
        global notebook
        
        # Create note for the main window, give access to it for all
        notebook = gtk.Notebook()
        self.notebook = notebook
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
        
        self.hpanepos = gconf.client_get_default(). \
                            get_int(pedconfig.conf.config_reg + "/hpaned")
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
            vpaned.area.fname = os.path.realpath(aa)
            
            # Create backup
            hhh = hash_name(vpaned.area.fname) + ".org"           
            xfile = pedconfig.conf.config_dir + "/" + hhh
            if not os.path.isfile(xfile):
                try:
                    writefile(xfile, buff)                
                except:
                    print "Cannot create backup file"

            notebook.append_page(vpaned)               
            vpaned.area.set_tablabel()
            
        if cnt == 0:
            #print "No valid file on command line, creating new", os.getcwd()
            aa = pedconfig.conf.UNTITLED
            vpaned = edPane([])
            vpaned.area.fname = os.path.realpath(aa)
            notebook.append_page(vpaned)                           
            vpaned.area.set_tab_label()
            
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

    # --------------------------------------------------------------------

    def area_winstate(self, arg1, arg2):
        pass
        #print "area_winstate", arg1, arg2
        #print "state", self.window.get_state()
    
    def unmap(self, arg1, arg2):
        print "unmap", arg1, arg2 

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
        pedconfig.conf.keyh.reset()        
        # Focus on main doc
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        if vcurr:
            self.window.set_focus(vcurr.vbox.area)

    def area_focus_out(self, win, act):
        pass
        #print  "area focus out", win, act   
         
    # Note message handlers:
   
    def  note_focus_in(self, win, act):
        pass
        #print "note_focus_in", win, act
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        if vcurr:
            self.window.set_focus(vcurr.vbox.area)
        
    def note_enter_notify(self, win):
        pass
        #print "note_enter_notify", win

    def  note_grab_focus_cb(self, win):
        #print "note_grab_focus_cb", win
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        if vcurr:
            self.window.set_focus(vcurr.vbox.area)
        
    def  note_swpage_cb(self, tabx, page, num):
        #print "note_swpage", num
        vcurr = tabx.get_nth_page(num)
        self.window.set_title("pyedit: " + vcurr.area.fname);
        self.window.set_focus(vcurr.vbox.area)        
        #self.update_statusbar("Switched to '{1:s}'".
        #                        format(num, vcurr.area.fname))
                
    def  note_page_cb(self, tabx, child, num):
        pass
        #print "note_page"

    def  note_focus_cb(self, tabx, foc):
        #print "note_focus_cb"
        vcurr = notebook.get_nth_page(notebook.get_current_page())
        if vcurr:
            self.window.set_focus(vcurr.vbox.area)
       
    def  note_create_cb(self, tabx, page, xx, yy):
        pass
        #print "note_create"

    # Note message handlers end
    def activate_qhelp(self, action):
        self.update_statusbar("Showing quick help")        
        pid = os.spawnlp(os.P_NOWAIT, "/usr/bin/pangview.py", "pangview", "README")
                    
    def dlg_keys(self, arg1, arg2):
        if  arg2.type == gtk.gdk.KEY_PRESS:
            if arg2.keyval == gtk.keysyms.x or arg2.keyval == gtk.keysyms.X:
                if arg2.state & gtk.gdk.MOD1_MASK:
                    arg1.destroy()
    
    def activate_about(self, action):
        self.update_statusbar("Showing About Dialog")        
        dialog = gtk.AboutDialog()
        dialog.set_name(" PyEdit - Python Editor ")
        dialog.connect("key-press-event", self.dlg_keys)
        dialog.connect("key-release-event", self.dlg_keys)

        dialog.set_version("1.0");
        comm = "\nPython based easily configurable editor.\n"\
            "\nRunning pygtk %d.%d.%d\n" % gtk.pygtk_version
        dialog.set_comments(comm);
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

        #dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
        #    gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
        #    'Action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        #dialog.connect ("response", lambda d, r: d.destroy())
        #dialog.show()

        strx = action.get_name()
        #print strx

        if strx == "New":
            aa = pedconfig.conf.UNTITLED
            vpaned = edPane([])
            vpaned.area.fname = os.path.realpath(aa)
            global notebook
            self.notebook.append_page(vpaned)                           
            vpaned.area.set_tablabel()

            #label = gtk.Label(" " + os.path.basename(aa) + " ")
            #self.notebook.set_tab_label(vpaned, label)        
            self.window.show_all()

            # Make it current
            nn = notebook.get_n_pages(); 
            if nn:
                vcurr = notebook.set_current_page(nn-1)
                vcurr = notebook.get_nth_page(nn-1)
                self.window.set_focus(vcurr.vbox.area)
           
        if strx == "Open":
            #print "open"
            but =   "Cancel", gtk.BUTTONS_CANCEL, "Open File", gtk.BUTTONS_OK
            fc = gtk.FileChooserDialog("Open file", self.window, \
                gtk.FILE_CHOOSER_ACTION_OPEN, but)
            fc.set_default_response(gtk.BUTTONS_OK)
            fc.connect("response", self.done_open_fc)                
            #fc.set_current_name(self.fname)
            fc.run()    
        
        if strx == "Save":
            vcurr = notebook.get_nth_page(notebook.get_current_page())
            vcurr.area.save()

        if strx == "SaveAs":
            vcurr = notebook.get_nth_page(notebook.get_current_page())
            vcurr.area.saveas()

        if strx == "Close":
            cc = notebook.get_n_pages()
            nn = notebook.get_current_page()
            vcurr = notebook.get_nth_page(nn)
            vcurr.area.closedoc()
     
            # Wrap around       
            if nn == 0: mm = cc - 1
            else:       mm = nn - 1
                
            notebook.set_current_page(mm)                        
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            self.window.set_focus(vcurr2.vbox.area)                   
            notebook.remove_page(nn)
            self.window.show_all()               

        if strx == "Copy":
            #print "copy"
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.ctrl_c(vcurr2.area)

        if strx == "Cut":
            #print "cut"
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.ctrl_x(vcurr2.area)

        if strx == "Paste":
            #print "paste"
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.ctrl_v(vcurr2.area)

        if strx == "Goto":
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.alt_g(vcurr2.area)

        if strx == "Find":
            print "find"
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.ctrl_f(vcurr2.area)

        if strx == "Record":
            #print "record"
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.f7(vcurr2.area)

        if strx == "Play":
            #print "record"
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.f8(vcurr2.area)

        if strx == "Animate":
            #print "record"
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.f6(vcurr2.area, True)

    def done_open_fc(self, win, resp):
        #print "done_open_fc", win, resp
        if resp == gtk.BUTTONS_OK:
            fname = win.get_filename()
            if not fname:
                #print "Must have filename"
                self.update_statusbar("No filename specified")                    
                pass
            else:
                #print "opening '"+ fname + "'"        
                self.update_statusbar("Opening file '{0:s}'".format(fname))
                try:            
                    buff = readfile(fname)
                except:
                    self.update_statusbar("Cannot read file '{0:s}'".format(fname))
                    #print "Cannot read file '" + fname , "'"
                    return

                self.update_statusbar("Opened file '{0:s}'".format(fname))
                vpaned = edPane(buff)
                vpaned.area.fname = os.path.realpath(fname)
                # Create backup
                hhh = hash_name(vpaned.area.fname) + ".org"           
                xfile = pedconfig.conf.config_dir + "/" + hhh
                if not os.path.isfile(xfile):
                    try:
                        writefile(xfile, buff)                
                    except:
                        print "Cannot create backup file"

                global notebook
                self.notebook.append_page(vpaned)                           
                vpaned.area.set_tablabel()
                self.window.show_all()

                # Make it current
                nn = notebook.get_n_pages(); 
                if nn:
                    vcurr = notebook.set_current_page(nn-1)
                    vcurr = notebook.get_nth_page(nn-1)
                    self.window.set_focus(vcurr.vbox.area)                   
        win.destroy()        

    def activate_exit(self, action):
        #print "activate_exit called"        
        OnExit(self.window)

    def activate_quit(self, action):
        #print "activate_quit called"        
        OnExit(self.window, False)
                 
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

    def update_statusbar2(self, xx = 0, yy = 0, ins = 0):
        # Always update line / col
        if ins: str2 = "INS"
        else: str2 ="OVR"
        strx2 = "Ln: {0:d}   Col: {1:d} {2:s}".format(yy, xx, str2)

        self.statusbar2.pop(0)
        self.statusbar2.push(0, strx2)
       
    def update_statusbar(self, strx):
        # Clear any previous message, underflow is allowed
        self.statusbar.pop(0)
        if not strx: 
            self.statusbar.push("Idle")
            return

        self.statusbar.push(0, strx)
        self.statuscount = STATUSCOUNT
        pass

    def update_resize_grip(self, widget, event):
        #print "update state", event, event.changed_mask
        #self.window.set_focus(notebook)
 
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED | gtk.gdk.WINDOW_STATE_FULLSCREEN
        if (event.changed_mask & mask):
            self.statusbar.set_has_resize_grip(not (event.new_window_state & mask))

def OnExit(arg, prompt = True):

    #print "onexit"
    arg.set_title("Exiting ...")

    # Save UI related data
    pos = mained.hpaned.get_position()
    pos = max(pos, 1)
    gconf.client_get_default().set_int\
                    (pedconfig.conf.config_reg + "/hpaned", pos)    

    firstpage = notebook.get_nth_page(0)
    if firstpage:
        pos = firstpage.get_position()
        pos = max(pos, 1)
        gconf.client_get_default().set_int\
                    (pedconfig.conf.config_reg + "/vpaned", pos)    

    # Do not save ful screen coordinates (use F11)
    if not mained.full:
        xx, yy = mained.window.get_position()
        gconf.client_get_default().set_int\
                        (pedconfig.conf.config_reg + "/xx", xx)    
        gconf.client_get_default().set_int\
                        (pedconfig.conf.config_reg + "/yy", yy)    

        ww, hh = mained.window.get_size()        

        gconf.client_get_default().set_int\
                        (pedconfig.conf.config_reg + "/ww", ww)    
        gconf.client_get_default().set_int\
                        (pedconfig.conf.config_reg + "/hh", hh)    
    
    # Prompt for save files
    nn = notebook.get_n_pages(); cnt = 0
    while True:
        if cnt >= nn: break
        ppp = notebook.get_nth_page(cnt)
        #print "page:", ppp.area
        if prompt:
            ppp.area.prompt_save(False)
        else:
            # Rescue to temporary:
            if ppp.area.changed:
                hhh = hash_name(ppp.area.fname) + ".txt"           
                xfile = pedconfig.conf.config_dir + "/" + hhh
                writefile(xfile, ppp.area.text)                
        cnt += 1 

    # Exit here
    gtk.main_quit()

    #print "OnExit called \"" + arg.get_title() + "\""

# ------------------------------------------------------------------------    
def handler(signum, frame):

    try:
        #print 'Signal handler called with signal', signum
        global notebook

        if pedconfig.conf.idle:
            pedconfig.conf.idle -= 1
            if pedconfig.conf.idle == 0:
                vcurr = notebook.get_nth_page(notebook.get_current_page())
                # Rescue to save:
                if vcurr:            
                    if vcurr.area.changed:
                        hhh = hash_name(vcurr.area.fname) + ".sav"           
                        xfile = pedconfig.conf.config_dir + "/" + hhh
                        writefile(xfile, vcurr.area.text)             
                        #strx = "Backed up file '{0:s}'".format(xfile)
                        # This will raise exception
                        #self.update_statusbar(strx)
        
        if pedconfig.conf.syncidle:
            pedconfig.conf.syncidle -= 1
            if pedconfig.conf.syncidle == 0:
                vcurr = notebook.get_nth_page(notebook.get_current_page())
                if vcurr:            
                    if vcurr.area.changed:
                        vcurr.area2.text = vcurr.area.text
                        vcurr.area2.invalidate()
                        
        if pedconfig.conf.pedwin.statuscount:
            pedconfig.conf.pedwin.statuscount -= 1
            if pedconfig.conf.pedwin.statuscount == 0:
                pedconfig.conf.pedwin.update_statusbar("Idle.");            
                pedconfig.conf.pedwin.statuscount = 0 
    except:
        print "Exception in timer handler"

    signal.alarm(1)

