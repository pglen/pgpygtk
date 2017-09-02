#!/usr/bin/env python

import signal, os, time
import gobject, gtk
import peddoc

(
  COLOR_RED,
  COLOR_GREEN,
  COLOR_BLUE
) = range(3)

(
  SHAPE_SQUARE,
  SHAPE_RECTANGLE,
  SHAPE_OVAL,
) = range(3)

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

# Create main document widget window with scroll bars
class edwin(gtk.VBox):

    def __init__(self, buff):
        
        gtk.VBox.__init__(self)

        area  = peddoc.pedDoc(buff, None, None)        
        frame = gtk.Frame()
        frame.add(area)        
        hbox = gtk.HBox()
        hbox.pack_start(frame, True, True)
        hbox.pack_end(area.vscroll, False, False)        
        self.pack_start(hbox, True, True)
        self.pack_end(area.hscroll, False, False)

        # Make it visible:
        self.area = area
                        
# ------------------------------------------------------------------------
#  Define Application Main Window claass

class AppMainWindow():

    def __init__(self, buff, fname = None, parent=None):

        register_stock_icons()
       
        # Create the toplevel window
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            window.connect('destroy', lambda *w: gtk.main_quit())
    
        if fname:
            strx = "PyEdit: ''%s''" % fname
        else:
            strx = "PyEdit";
            
        window.set_title(strx);
        window.set_position(gtk.WIN_POS_CENTER)

        #if full:
        #    self.set_default_size(www, hhh)
        #else: 

        www = gtk.gdk.screen_width();
        hhh = gtk.gdk.screen_height();
        #window.set_default_size(3*www/4, 2*hhh/4)

        merge = gtk.UIManager()
        window.set_data("ui-manager", merge)
        merge.insert_action_group(self.__create_action_group(), 0)
        window.add_accel_group(merge.get_accel_group())
        
        try:
            mergeid = merge.add_ui_from_string(ui_info)
        except gobject.GError, msg:
            print "Building menus failed: %s" % msg

        bar = merge.get_widget("/MenuBar")
        bar.show()

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
        vpaned = gtk.VPaned(); vpaned.set_border_width(5)
      
        self.create_tree()

        self.frame2.add(self.tv)
        hpaned.add(self.frame2)
        hpaned.pack2(vpaned)
        hpaned.set_position(120)

        # Create document
        vbox = edwin(buff)
        vpaned.add(vbox)
        vpaned.set_position(120)
           
        vbox2 = edwin(buff)
        vpaned.pack2(vbox2)
   
        table.attach(hpaned,
            # X direction           Y direction
            0, 1,                   2, 3,
            gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            0,                      0)
        
        # Create statusbar
        self.statusbar = gtk.Statusbar()
        table.attach(self.statusbar,
            # X direction           Y direction
            0, 1,                   3, 4,
            gtk.EXPAND | gtk.FILL,  0,
            0,                      0)

        window.connect("window_state_event", self.update_resize_grip)
        window.connect("destroy", OnExit)
       
        # Futile attempts to grab focus        
        #window.activate_default() 
        #vbox2.area.grab_default() 
        #window.set_default(None) 
        #vbox2.area.grab_focus()
        #vbox2.grab_focus() 
        
        # Focus to main editor:
        window.set_focus(vbox2.area)
        window.show_all()
       
        # Set the signal handler for 1s tick
        #signal.signal(signal.SIGALRM, handler)
        #signal.alarm(1)
        self.update_statusbar("Initial")

    def create_tree(self):
        self.treestore = gtk.TreeStore(str)
        #tv = peddoc.pedDoc("Hello\nBuffer\Here")
        #tv = gtk.TreeView()
        # we'll add some data now - 4 rows with 3 child rows each
        for parent in range(4):
          piter = self.treestore.append(None, ['parent %i' % parent])
          for child in range(3):
             self.treestore.append(piter, ['child %i of parent %i' %
                                            (child, parent)])

        # create the TreeView using treestore
        self.frame2 = gtk.Frame()
        self.tv = gtk.TreeView(self.treestore)

        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Functions')

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        
        # add tvcolumn to treeview
        self.tv.append_column(self.tvcolumn)

# ------------------------------------------------------------------------

    def __create_action_group(self):
        # GtkActionEntry
        entries = (
          ( "FileMenu", None, "_File" ),               # name, stock id, label
          ( "PreferencesMenu", None, "_Settings" ), # name, stock id, label
          ( "ColorMenu", None, "_Color"  ),            # name, stock id, label
          ( "ShapeMenu", None, "_Shape" ),             # name, stock id, label
          ( "HelpMenu", None, "_Help" ),               # name, stock id, label
          ( "New", gtk.STOCK_NEW,                      # name, stock id
            "_New", "<control>N",                      # label, accelerator
            "Create a new file",                       # tooltip
            self.activate_action ),
          ( "Open", gtk.STOCK_OPEN,                    # name, stock id
            "_Open","<control>O",                      # label, accelerator
            "Open a file",                             # tooltip
            self.activate_action ),
          ( "Save", gtk.STOCK_SAVE,                    # name, stock id
            "_Save","<control>S",                      # label, accelerator
            "Save current file",                       # tooltip
            self.activate_action ),
          ( "SaveAs", gtk.STOCK_SAVE,                  # name, stock id
            "Save _As...", None,                       # label, accelerator
            "Save to a file",                          # tooltip
            self.activate_action ),
          ( "Quit", gtk.STOCK_QUIT,                    # name, stock id
            "_Quit", "<control>Q",                     # label, accelerator
            "Quitx",                                    # tooltip
             self.activate_quit ),
          ( "Exit", gtk.STOCK_QUIT,                    # name, stock id
            "_Exit", "<alt>X",                         # label, accelerator
            "Exit program",                            # tooltip
             self.activate_quit ),
          ( "About", None,                             # name, stock id
            "_About", "",                              # label, accelerator
            "About",                                   # tooltip
            self.activate_about ),
          ( "Logo", "demo-gtk-logo",                   # name, stock id
             None, None,                              # label, accelerator
            "GTK+",                                    # tooltip
            self.activate_action ),
        );

        # GtkToggleActionEntry
        toggle_entries = (
          ( "Bold", gtk.STOCK_BOLD,                    # name, stock id
             "_Bold", "<control>B",                    # label, accelerator
            "Bold",                                    # tooltip
            self.activate_action,
            True ),                                    # is_active
        )

        # GtkRadioActionEntry
        color_entries = (
          ( "Red", None,                               # name, stock id
            "_Red", "<control><shift>R",               # label, accelerator
            "Blood", COLOR_RED ),                      # tooltip, value
          ( "Green", None,                             # name, stock id
            "_Green", "<control><shift>G",             # label, accelerator
            "Grass", COLOR_GREEN ),                    # tooltip, value
          ( "Blue", None,                              # name, stock id
            "_Blue", "<control><shift>B",              # label, accelerator
            "Sky", COLOR_BLUE ),                       # tooltip, value
        )

        # GtkRadioActionEntry
        shape_entries = (
          ( "Square", None,                            # name, stock id
            "_Square", "<control><shift>S",            # label, accelerator
            "Square",  SHAPE_SQUARE ),                 # tooltip, value
          ( "Rectangle", None,                         # name, stock id
            "_Rectangle", "<control><shift>R",         # label, accelerator
            "Rectangle", SHAPE_RECTANGLE ),            # tooltip, value
          ( "Oval", None,                              # name, stock id
            "_Oval", "<control><shift>O",              # label, accelerator
            "Egg", SHAPE_OVAL ),                       # tooltip, value
        )

        # Create the menubar and toolbar
        action_group = gtk.ActionGroup("AppWindowActions")
        action_group.add_actions(entries)
        action_group.add_toggle_actions(toggle_entries)
        action_group.add_radio_actions(color_entries, COLOR_RED, self.activate_radio_action)
        action_group.add_radio_actions(shape_entries, SHAPE_OVAL, self.activate_radio_action)

        return action_group

    def activate_about(self, action):
        self.update_statusbar("Showing About Dialog")
        
        dialog = gtk.AboutDialog()
        dialog.set_name("PED - Python Editor")
        dialog.set_version("1.0");
        dialog.set_comments("\nPython based advanced editor\n");
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

    def update_statusbar(self, strx):
        # Clear any previous message, underflow is allowed
        self.statusbar.pop(0)
        if not strx: 
            return

        #count = buffer.get_char_count()
        #iter = buffer.get_iter_at_mark(buffer.get_insert())
        #row = iter.get_line()
        #col = iter.get_line_offset()
        self.statusbar.push(0, strx)
        #self.statusbar.push(0,
        #'Cursor at row %d column %d - %d chars in document' % (row, col, count))
        pass

    def update_resize_grip(self, widget, event):
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED | gtk.gdk.WINDOW_STATE_FULLSCREEN
        if (event.changed_mask & mask):
            self.statusbar.set_has_resize_grip(not (event.new_window_state & mask))

    
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

# Callback for cleanup

def OnExit(arg):
        #print "OnExit called \"" + arg.get_title() + "\""
        arg.set_title("Exiting ...")
        #time.sleep(1);         
         
def handler(signum, frame):
        #print 'Signal handler called with signal', signum
        signal.alarm(1)
    


