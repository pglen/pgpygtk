#!/usr/bin/env python
 
import signal, os, time, sys
import gobject, gtk, gconf
import subprocess

import  peddoc, pedconfig, pedofd
import  pedync

# Into our namespace
from    pedmenu import *
from    pedui import *
from    pedutil import *

STATUSCOUNT = 5             # Length of the styatus bar timeout (in sec)

treestore = None
notebook = None
      
#def scroll(aa, bb):
#    print aa, bb

# -----------------------------------------------------------------------
# Create document

class edPane(gtk.VPaned):  

    def __init__(self, buff = [], focus = False):

        pos = gconf.client_get_default().\
                    get_int(pedconfig.conf.config_reg + "/vpaned")
        if pos == 0: pos = 120

        gtk.VPaned.__init__(self)
        self.set_border_width(5)
        self.set_position(pos)
        self.vbox = edwin(buff); 
        self.add2(self.vbox)           
        self.vbox2 = edwin(buff, True)
        self.add1(self.vbox2)   
        
        # Shortcuts to access the editor windows
        self.area  = self.vbox.area
        self.area2 = self.vbox2.area
        
# -----------------------------------------------------------------------
# Create main document widget with scroll bars

class edwin(gtk.VBox):

    def __init__(self, buff, readonly = False):
        
        global notebook, mained

        gtk.VBox.__init__(self)

        area  = peddoc.pedDoc(buff, mained, readonly)        
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
        self.fcount = 0
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

        aa = create_action_group(self)
        merge.insert_action_group(aa, 0)
        window.add_accel_group(merge.get_accel_group())
       
        try:
            mergeid = merge.add_ui_from_string(ui_info)
        except gobject.GError, msg:
            print "Building menus failed: %s" % msg
        
        # Add MRU        
        for cnt in range(6):
            ss = "/sess_%d" % cnt
            fname = gconf.client_get_default().get_string\
                        (pedconfig.conf.config_reg + ss)                
            if fname != "":
                self.add_mru(merge, aa, fname, ss)
                                
        merge_id = merge.new_merge_id()
        merge.add_ui(merge_id, "ui/MenuBar/FileMenu/SaveAs", "", None, gtk.UI_MANAGER_SEPARATOR, False)
                
        mbar = merge.get_widget("/MenuBar")
        mbar.show()

        window.set_events(  gtk.gdk.POINTER_MOTION_MASK |
                            gtk.gdk.POINTER_MOTION_HINT_MASK |
                            gtk.gdk.BUTTON_PRESS_MASK |
                            gtk.gdk.BUTTON_RELEASE_MASK |
                            gtk.gdk.KEY_PRESS_MASK |
                            gtk.gdk.KEY_RELEASE_MASK |
                            gtk.gdk.FOCUS_CHANGE_MASK )

        #window.set_events(  gtk.gdk.ALL_EVENTS_MASK)
        
        global notebook
        
        # Create note for the main window, give access to it for all
        notebook = gtk.Notebook(); self.notebook = notebook
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
            
        table = gtk.Table(2, 4, False)
        window.add(table)

        table.attach(mbar,
            # X direction #          # Y direction
            0, 1,                      0, 1,
            gtk.EXPAND | gtk.FILL,     0,
            0,                         0);

        tbar = merge.get_widget("/ToolBar"); tbar.set_tooltips(True)
        tbar.show()
        table.attach(tbar,
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
        slab = gtk.Label("   ")
        hpane2 = gtk.HPaned()
        
        hpane2.set_position(self.get_width() - 250)
        hpane2.pack2(self.statusbar2)
        shbox = gtk.HBox()
        shbox.pack_start(slab, False)
        shbox.pack_start(self.statusbar)
        hpane2.pack1(shbox)
                        
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

        # ----------------------------------------------------------------
        cnt = 0    
        # Read in buffers
        for aa in names:    
            aaa = os.path.realpath(aa)
            #print "loading file: ", aaa
            vpaned = edPane()
            ret = vpaned.area.loadfile(aaa)
            if not ret:
                self.update_statusbar("Cannot read file '{0:s}'".format(aaa))                                 
                continue
            ret = vpaned.area2.loadfile(aaa)
                
            cnt += 1
            notebook.append_page(vpaned)               
            vpaned.area.set_tablabel()
            
        if cnt == 0:
            #print "No file on command line, creating new", os.getcwd()
            
            fcnt = gconf.client_get_default().get_int\
                        (pedconfig.conf.config_reg + "/cnt")    
            
            # Load old session            
            for nnn in range(fcnt):
                ss = "/sess_%d" % nnn
                fff = gconf.client_get_default().get_string\
                            (pedconfig.conf.config_reg + ss)    
                            
                #print "loading ", fff

                vpaned = edPane()
                ret = vpaned.area.loadfile(fff)
                if not ret:
                    self.update_statusbar("Cannot read file '{0:s}'".format(fff))                                 
                    continue
                    vpaned.area2.loadfile(fff)
                    
                notebook.append_page(vpaned)                           
                vpaned.area.set_tablabel()

        # Show newly created buffers:
        window.show_all()

        # Set last file  
        fff = gconf.client_get_default().get_string\
                        (pedconfig.conf.config_reg + "/curr")
                        
        #print "curr file", fff      
        cc = notebook.get_n_pages()
        for mm in range(cc):
            vcurr = notebook.get_nth_page(mm)
            if vcurr.area.fname == fff:    
                #print "found buff", fff      
                notebook.set_current_page(mm)
                self.window.set_focus(vcurr.vbox.area)                
                break
  
        # Set the signal handler for 1s tick
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(1)
        self.update_statusbar("Initial")

    # --------------------------------------------------------------------

    def add_mru(self, merge, action_group, fname, mru):
    
        sname = os.path.basename(fname)
            
        #gtk.Action(name, label, tooltip, stock_id)
        ac = gtk.Action(mru, sname, fname, None)
        ac.connect('activate', self.activate_action)
        action_group.add_action(ac)
        merge_id = merge.new_merge_id()
        #add_ui(merge_id, path, name, action, type, top)
        merge.add_ui(merge_id, "/MenuBar/FileMenu/SaveAs", \
                    mru, mru, gtk.UI_MANAGER_MENUITEM, False)
        
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
                try:
                    treestore.remove(root)                           
                except:
                    print "Exception on rm treestore"
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

        if not treestore: return
        # Delete previous contents
        try:      
            while True:
                root = treestore.get_iter_first()
                if not root:
                    break 
                try:
                    treestore.remove(root)                           
                except:
                    print "except: treestore remove"    
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
        try:
            rr = get_exec_path("QHELP")
            #pid = os.spawnlp(os.P_NOWAIT, "pangview.py", "pangview",  rr)
            ret = subprocess.Popen(["pangview.py",  rr])
        except:
            pedync.message("\n   Cannot launch the pangview.py utility.   \n\n"
                           "              (Please install)")            
    def activate_about(self, action):
        self.update_statusbar("Showing About Dialog")        
        pedync.about()

    def activate_action(self, action):

        #dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
        #    gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
        #    'Action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        #dialog.connect ("response", lambda d, r: d.destroy())
        #dialog.show()

        strx = action.get_name()
        #print "activate_action", strx

        if strx == "New":
            # Find non existing file
            cnt = self.fcount + 1; fff = ""
            base, ext = os.path.splitext(pedconfig.conf.UNTITLED)
            while True:            
                fff =  "%s_%d.txt" % (base, cnt)
                #print fff
                if not os.path.isfile(fff):
                    break;
                cnt += 1
                
            self.fcount = cnt
            # Touch
            #open(fff, "w").close()
            
            vpaned = edPane([])
            vpaned.area.fname = os.path.realpath(fff)
            global notebook
            notebook.append_page(vpaned)                           
            vpaned.area.set_tablabel()

            #label = gtk.Label(" " + os.path.basename(aa) + " ")
            #notebook.set_tab_label(vpaned, label)        
            self.window.show_all()

            # Make it current
            nn = notebook.get_n_pages(); 
            if nn:
                vcurr = notebook.set_current_page(nn-1)
                vcurr = notebook.get_nth_page(nn-1)
                self.window.set_focus(vcurr.vbox.area)
           
        if strx == "Open":
            #print "open"
            # Traditional open file
            '''but =   "Cancel", gtk.BUTTONS_CANCEL, "Open File", gtk.BUTTONS_OK
            fc = gtk.FileChooserDialog("Open file", self.window, \
                gtk.FILE_CHOOSER_ACTION_OPEN, but)
            fc.set_default_response(gtk.BUTTONS_OK)
            fc.connect("response", self.done_open_fc)                
            #fc.set_current_name(self.fname)
            fc.run()    '''
            # Simplified
            fname = pedofd.ofd("")
            if fname != "":
                self.openfile(fname)
        
        if strx == "Save":
            vcurr = notebook.get_nth_page(notebook.get_current_page())
            vcurr.area.save()

        if strx == "SaveAs":
            vcurr = notebook.get_nth_page(notebook.get_current_page())
            vcurr.area.saveas()

        if strx == "Close":
            self.closedoc()

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
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.f8(vcurr2.area)

        if strx == "Animate":
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.f8(vcurr2.area, True)

        if strx == "Undo":
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.ctrl_z(vcurr2.area)

        if strx == "Redo":
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.ctrl_y(vcurr2.area)

        if strx == "SaveAll":
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.alt_a(vcurr2.area)

        if strx == "Discard Undo":
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                vcurr2.area.delundo() 

        if strx == "NextWin":
            self.nextwin()
            
        if strx == "PrevWin":
            self.prevwin()

        if strx.find("/sess_") >= 0:            
            fname = gconf.client_get_default().get_string\
                        (pedconfig.conf.config_reg + strx)    
            self.openfile(fname)
                                
        if strx == "Help":
            #pedync.message("\n    Help: Work in progress    \n")
            nn2 = notebook.get_current_page()
            vcurr2 = notebook.get_nth_page(nn2)
            if vcurr2:
                pedconfig.conf.keyh.act.f1(vcurr2.area)

        if strx == "Settings":
            pedync.message("\n    Settings: Work in progress    \n")
       
    def closedoc(self):
        cc = notebook.get_n_pages()
        nn = notebook.get_current_page()
        vcurr = notebook.get_nth_page(nn)
        # Disable close
        if vcurr.area.closedoc():
            return
 
        # Wrap around       
        if nn == 0: mm = cc - 1
        else:       mm = nn - 1
            
        notebook.set_current_page(mm)                        
        nn2 = notebook.get_current_page()
        vcurr2 = notebook.get_nth_page(nn2)
        self.window.set_focus(vcurr2.vbox.area)                   
        notebook.remove_page(nn)
        self.window.show_all()               
         
    def  firstwin(self):
        cc = notebook.get_n_pages()
        if cc == 0:
            return
        notebook.set_current_page(0)                        
        nn2 = notebook.get_current_page()
        vcurr2 = notebook.get_nth_page(nn2)
        self.window.set_focus(vcurr2.vbox.area)                   
        self.window.show_all()               

    def  lastwin(self):
        cc = notebook.get_n_pages()
        if cc == 0:
            return
        notebook.set_current_page(cc-1)                        
        nn2 = notebook.get_current_page()
        vcurr2 = notebook.get_nth_page(nn2)
        self.window.set_focus(vcurr2.vbox.area)                   
        self.window.show_all()               
                                
    def  nextwin(self):
        cc = notebook.get_n_pages()
        nn = notebook.get_current_page()
        vcurr = notebook.get_nth_page(nn)
        
        # Wrap around if needed
        if nn == cc - 1: return # mm = 0
        else:       mm = nn + 1            
        notebook.set_current_page(mm)                        
        nn2 = notebook.get_current_page()
        vcurr2 = notebook.get_nth_page(nn2)
        self.window.set_focus(vcurr2.vbox.area)                   
        self.window.show_all()               

    def  prevwin(self):
        cc = notebook.get_n_pages()
        nn = notebook.get_current_page()
        vcurr = notebook.get_nth_page(nn)
        
        # Wrap around if needed
        if nn == 0: return # mm = cc - 1
        else:       mm = nn - 1            
        notebook.set_current_page(mm)                        
        nn2 = notebook.get_current_page()
        vcurr2 = notebook.get_nth_page(nn2)
        self.window.set_focus(vcurr2.vbox.area)                   
        self.window.show_all()               
    
        '''def done_open_fc(self, win, resp):
        #print "done_open_fc", win, resp
        if resp == gtk.BUTTONS_OK:
            fname = win.get_filename()            
            if not fname:
                #print "Must have filename"
                self.update_statusbar("No filename specified")                    
                pass
            else:
                self.openfile(fname)
        win.destroy()'''
                
    def saveall(self):
        #print "saveall"
        # Save all files
        nn = notebook.get_n_pages(); cnt = 0; cnt2 = 0
        while True:
            if cnt >= nn: break
            ppp = notebook.get_nth_page(cnt)                        
            if ppp.area.changed:
                ppp.area.writefile()
                cnt2 += 1
            cnt += 1
                
        self.update_statusbar("%d of %d buffers saved." % (cnt2, nn))                    
                         
    # -------------------------------------------------------------------
    def openfile(self, fname):
    
        # Is it already loaded? ... activate
        nn = notebook.get_n_pages(); 
        for aa in range(nn):
            vcurr = notebook.get_nth_page(aa)
            if vcurr.area.fname == fname:
                self.update_statusbar("Already open, activating '{0:s}'".format(fname))        
                vcurr = notebook.set_current_page(aa)
                vcurr = notebook.get_nth_page(aa)
                self.window.set_focus(vcurr.vbox.area)                   
                return
            
        #print "opening '"+ fname + "'"        
        self.update_statusbar("Opening file '{0:s}'".format(fname))        
        vpaned = edPane()
        ret = vpaned.area.loadfile(os.path.realpath(fname))
        if not ret:
            self.update_statusbar("Cannot read file '{0:s}'".format(fname))             
            return
        vpaned.area2.loadfile(os.path.realpath(fname))
        self.update_statusbar("Opened file '{0:s}'".format(fname))
       
        # Add to the list of buffers
        notebook.append_page(vpaned)                           
        vpaned.area.set_tablabel()
        self.window.show_all()
        # Make it current
        nn = notebook.get_n_pages(); 
        if nn:
            vcurr = notebook.set_current_page(nn-1)
            vcurr = notebook.get_nth_page(nn-1)
            self.window.set_focus(vcurr.vbox.area)                   

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

    # This is the line count / pos status bar
    def update_statusbar2(self, xx = 0, yy = 0, ins = 0, tlen = 0):
        # Always update line / col
        if ins: str2 = "INS"
        else: str2 ="OVR"
        strx2 = "Ln {0:d} Col {1:d} Tot {3:d}  {2:s} ".\
                                format(yy, xx, str2, tlen)

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

# ------------------------------------------------------------------------

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

    # Do not save full screen coordinates (when used F11)
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
  
    # Save current doc:
    vcurr = notebook.get_nth_page(notebook.get_current_page())
    if vcurr:            
        gconf.client_get_default().set_string\
                        (pedconfig.conf.config_reg + "/curr",\
                        vcurr.area.fname)        
          
    # Prompt for save files
    nn = notebook.get_n_pages(); cnt = 0
    while True:
        if cnt >= nn: break
        ppp = notebook.get_nth_page(cnt)
        #print "page:", ppp.area
        ppp.area.saveparms()
      
        ss = "/sess_%d" % cnt
        if cnt < 8:
            gconf.client_get_default().set_string\
                        (pedconfig.conf.config_reg + ss,\
                            ppp.area.fname)                    
        if prompt:
            if ppp.area.changed:
                msg = "\nWould you like to save:\n\n  \"%s\" \n" % ppp.area.fname
                rp = pedync.yes_no_cancel("pyedit: Save File ?", msg)

                if rp == gtk.RESPONSE_YES:   
                    ppp.area.save()
                    
                if rp == gtk.RESPONSE_NO:   
                    #print "gtk.RESPONSE_NO"
                    pass
                if  rp == gtk.RESPONSE_CANCEL or \
                    rp == gtk.RESPONSE_REJECT or \
                    rp == gtk.RESPONSE_CLOSE  or \
                    rp == gtk.RESPONSE_DELETE_EVENT:                
                    return
        else:
            # Rescue to temporary:
            if ppp.area.changed:
                hhh = hash_name(ppp.area.fname) + ".rescue"
                xfile = pedconfig.conf.config_dir + "/" + hhh
                print "Rescuing", xfile
                writefile(xfile, ppp.area.text)                
        cnt += 1 

    gconf.client_get_default().set_int\
                        (pedconfig.conf.config_reg + "/cnt",\
                            cnt)    
                                                           
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




