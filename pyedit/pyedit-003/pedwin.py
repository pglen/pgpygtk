#!/usr/bin/env python

import signal, os, time, sys
import gobject, gtk
import peddoc
from threading import Timer

from edmenu import *
import pedconfig

actionx = None; arg1 = None; arg2 = None
mained = None;
newfoc = None; newwin = None

ui_info = \
'''<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='New'/>
      <menuitem action='Open'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <separator/>
      <menuitem action='Quit'/>
      <menuitem action='Exit'/>
    </menu>
    <menu action='PreferencesMenu'>
      <menu action='ColorMenu'>
        <menuitem action='Red'/>
        <menuitem action='Green'/>
        <menuitem action='Blue'/>
      </menu>
      <menu action='ShapeMenu'>
        <menuitem action='Square'/>
        <menuitem action='Rectangle'/>
        <menuitem action='Oval'/>
      </menu>
      <menuitem action='Bold'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='About'/>
    </menu>
  </menubar>

  <toolbar  name='ToolBar'>
    <toolitem action='New'/>
    <toolitem action='Open'/>
    <toolitem action='Quit'/>
    <separator/>
    <toolitem action='Logo'/>
  </toolbar>
</ui>'''
 
def scroll(aa, bb):
    print aa, bb

# -----------------------------------------------------------------------
# Create document

class edPane(gtk.VPaned):  

    def __init__(self, buff, focus = False):

        gtk.VPaned.__init__(self)
        self.set_border_width(5)
        self.set_position(120)
        self.vbox = edwin(buff, True); 
        self.add2(self.vbox)           
        self.vbox2 = edwin("skeleton")
        self.add1(self.vbox2)   
        self.area = self.vbox.area
        
# -----------------------------------------------------------------------
# Create main document widget window with scroll bars

class edwin(gtk.VBox):

    def __init__(self, buff, focus = False):
        
        global notebook, mained

        gtk.VBox.__init__(self)

        area  = peddoc.pedDoc(buff, None, None)        
        #print "created", area
        
        # Give access to nb
        area.notebook = notebook
        area.mained = mained
    
        if focus: 
            area.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE | gtk.CAN_DEFAULT)
            #area.grab_focus()        
                   
        frame = gtk.Frame(); frame.add(area)        
        hbox = gtk.HBox()
        hbox.pack_start(frame, True, True)
        hbox.pack_end(area.vscroll, False, False)        

        self.pack_start(hbox, True, True)
        self.pack_end(area.hscroll, False, False)

        # Make it acessable:
        self.area = area

# ------------------------------------------------------------------------

def readfile(strx):
                  
    f = open(strx)
    buff = f.read();
    f.close()
    return buff
      
# ------------------------------------------------------------------------
#  Define Application Main Window claass

class EdMainWindow():
    
    def __init__(self, fname, parent, names):
    
        self.statuscount = 0
        register_stock_icons()

        global mained
        mained = self

        # Create the toplevel window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window = window
        
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            window.connect('destroy', lambda *w: gtk.main_quit())
    
        #print "me", window          

        window.set_position(gtk.WIN_POS_CENTER)
        www = gtk.gdk.screen_width(); hhh = gtk.gdk.screen_height();
      
        if pedconfig.pedconfig.full_screen:
            window.set_default_size(www, hhh)
        else: 
            window.set_default_size(7*www/8, 5*hhh/8)
            window.move(www / 16, hhh / 10)        

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
        
        global notebook
        
        # Create note for the main window, give access to it for all
        notebook = gtk.Notebook()
        notebook.popup_enable()
        notebook.set_scrollable(True)

        #notebook.add_events(gtk.gdk.FOCUS_CHANGE_MASK)
        notebook.add_events(gtk.gdk.ALL_EVENTS_MASK)

        notebook.connect("focus-tab", self.note_focus_cb)
        notebook.connect("create-window", self.note_create_cb)
        notebook.connect("change-current-page", self.note_page_cb)
        notebook.connect("switch-page", self.note_swpage_cb)
       
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
        
        tv = self.create_tree()
        frame2 = gtk.Frame()
        
        frame2.add(tv)
        hpaned.add(frame2)
        hpaned.set_position(120)
        hpaned.pack2(notebook)

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
            vpaned.fname = os.path.realpath(aa)
            notebook.append_page(vpaned)               
            label = gtk.Label(" " + os.path.basename(aa) + " ")
            notebook.set_tab_label(vpaned, label)
            
        if cnt == 0:
            #print "No valid file on command line, creating new", os.getcwd()
            aa = "untitled.txt"
            vpaned = edPane("")
            vpaned.fname = os.path.realpath(aa)
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
        #vcurr = notebook.get_nth_page(0)
        #window.set_focus(vcurr.vbox.area)

        # Set the signal handler for 1s tick
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(1)
        self.update_statusbar("Initial")
   
    # Call key handler
    def area_key(self, area, event):
        pass
        #print event
        #return True

    def get_height(self):
        xx, yy = self.window.get_size()
        return yy

    def get_width(self):
        xx, yy = self.window.get_size()
        return xx

    # --------------------------------------------------------------------
    def create_tree(self):
        
        treestore = gtk.TreeStore(str)

        # we'll add some data now - 4 rows with 3 child rows each
        for parent in range(4):
          piter = treestore.append(None, ['parent %i' % parent])
          for child in range(3):
             treestore.append(piter, ['child %i of parent %i' %
                                            (child, parent)])

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
        
    def  note_swpage_cb(self, tabx, page, num):
        #print "note_swpage", num
        vcurr = tabx.get_nth_page(num)
        self.window.set_title("pyedit: " + vcurr.fname);
        #self.window.set_default(vcurr.vbox.area)        
        #self.window.set_focus(vcurr.vbox.area)        
        #self.window.activate_default()        
        #vcurr.vbox.area.grab_focus()        
        self.update_statusbar("Switched to '{1:s}'".
                format(num, vcurr.fname))
        global newwin, newfoc
        newwin = self.window; newfoc = vcurr.vbox.area
        Timer(0, run_async_time, ()).start()
        return True
        
    def  note_page_cb(self, tabx, child, num):
        pass
        print "note_page"

    def  note_focus_cb(self, tabx, foc):
        print "note_focus"

    def  note_create_cb(self, tabx, page, xx, yy):
        print "note_create"

    def activate_about(self, action):
        self.update_statusbar("Showing About Dialog")        
        dialog = gtk.AboutDialog()
        dialog.set_name("PyEdit - Python Editor")
        dialog.set_version("1.0");
        dialog.set_comments("\nPython based configurable editor\n");
        dialog.set_copyright("\302\251 Copyright Peter Glen")

        try:
	        pixbuf = gtk.gdk.pixbuf_new_from_file('gtk-logo-rgb.gif')
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
        #print "Exit called"        
        gtk.main_quit()

    def done_dlg():
        pass

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

    # Callback for cleanup

    
# It's totally optional to do this, you could just manually insert icons
# and have them not be themeable, especially if you never expect people
# to theme your app.

def register_stock_icons():
    ''' This function registers our custom toolbar icons, so they
        can be themed.
    '''
    items = [('demo-gtk-logo', '_GTK!', 0, 0, '')]
    # Register our stock items
    gtk.stock_add(items)

    # Add our custom icon factory to the list of defaults
    factory = gtk.IconFactory()
    factory.add_default()

    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')
    #print img_path
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)
        # Register icon to accompany stock item
     
        # The gtk-logo-rgb icon has a white background, make it transparent
        # the call is wrapped to (gboolean, guchar, guchar, guchar)
        transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
        icon_set = gtk.IconSet(transparent)
        factory.add('demo-gtk-logo', icon_set)

    except gobject.GError, error:
        #print 'failed to load GTK logo ... trying local'
        try:
		    #img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')
		    pixbuf = gtk.gdk.pixbuf_new_from_file('gtk-logo-rgb.gif')
		    # Register icon to accompany stock item
		    # The gtk-logo-rgb icon has a white background, make it transparent
		    # the call is wrapped to (gboolean, guchar, guchar, guchar)
		    transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
		    icon_set = gtk.IconSet(transparent)
		    factory.add('demo-gtk-logo', icon_set)

        except gobject.GError, error:
            print 'failed to load GTK logo for toolbar'
    
def OnExit(arg):
    #print "OnExit called \"" + arg.get_title() + "\""
    arg.set_title("Exiting ...")
    #time.sleep(1);         

def actionx_focus():
    pass
    #arg1.window.set_focus(arg2)        
    #arg2.grab_focus()
                 
def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    
    if pedconfig.pedconfig.pedwin.statuscount:
        pedconfig.pedconfig.pedwin.statuscount -= 1
        if pedconfig.pedconfig.pedwin.statuscount == 0:
            pedconfig.pedconfig.pedwin.update_statusbar("Idle");            
            pedconfig.pedconfig.pedwin.statuscount = 0 
    signal.alarm(1)

# This is a cludge for setting focus on the tab's second edit window.
# We call the timer function so the set_focus is executed in the 
# context of the main thread.

def run_async_time():

    global newwin, newfoc
    #print "From async_time", time.time()
    if newwin:
        newwin.set_focus(newfoc)
        newwin = None               # Run once

