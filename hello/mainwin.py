#!/usr/bin/env python

'''Application main window class
Demonstrates a typical application window, with menubar, toolbar, statusbar, 
            split pane, app position memory. '''

import signal, os, time
import gobject, gtk

import pydoc

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
 
winx = 12

# ------------------------------------------------------------------------
#  Define Application Main Window claass

class AppMainWindow(gtk.Window):

    global winx
 
    def getwinx(self):
        return  winx
   
    def __init__(self, parent=None):

        register_stock_icons()
        #winx = 11
       
        # Create the toplevel window
        gtk.Window.__init__(self)

        winx = 14; #self #.get_window();
                
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        #self.set_title(self.__class__.__name__)
        self.set_default_size(800, 600)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Hello App");

        merge = gtk.UIManager()
        self.set_data("ui-manager", merge)
        merge.insert_action_group(self.__create_action_group(), 0)
        self.add_accel_group(merge.get_accel_group())
        
        try:
            mergeid = merge.add_ui_from_string(ui_info)
        except gobject.GError, msg:
            print "Building menus failed: %s" % msg

        bar = merge.get_widget("/MenuBar")
        bar.show()

        table = gtk.Table(1, 4, False)
        self.add(table)

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

        # Create document
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_shadow_type(gtk.SHADOW_IN)

        table.attach(sw,
            # X direction           Y direction
            0, 1,                   2, 3,
            gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            0,                      0)

        #sw.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE | gtk.PARENT_SENSITIVE)
        #sw.add (self.area)

        area = pydoc.HelloDoc()
        sw.add_with_viewport(area);
      
        # Create statusbar
        self.statusbar = gtk.Statusbar()
        table.attach(self.statusbar,
            # X direction           Y direction
            0, 1,                   3, 4,
            gtk.EXPAND | gtk.FILL,  0,
            0,                      0)

        # Show text widget info in the statusbar
        #buffer = contents.get_buffer()
        #buffer.connect("changed", self.update_statusbar)
        #mark_set_callback = (lambda buffer, new_location, mark:
        #   self.update_statusbar(buffer))

        # cursor moved
        #buffer.connect("mark_set", mark_set_callback)

        self.connect("window_state_event", self.update_resize_grip)
        self.connect("destroy", OnExit)
        #self.update_statusbar(buffer)

        self.show_all()
        winx = self

        # Set the signal handler for 1s tick
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(1)

# ------------------------------------------------------------------------

    def __create_action_group(self):
        # GtkActionEntry
        entries = (
          ( "FileMenu", None, "_File" ),               # name, stock id, label
          ( "PreferencesMenu", None, "_Preferences" ), # name, stock id, label
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
            "_About", "<control>A",                    # label, accelerator
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
        dialog = gtk.AboutDialog()
        dialog.set_name("Hello World")
        dialog.set_version("1.0");
        dialog.set_comments("\nPyGTK Extended Hello\n");
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
        print "Exit called"        
        gtk.main_quit()

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

    def update_statusbar(self, buffer):
        # clear any previous message, underflow is allowed
        #self.statusbar.pop(0)
        #count = buffer.get_char_count()
        #iter = buffer.get_iter_at_mark(buffer.get_insert())
        #row = iter.get_line()
        #col = iter.get_line_offset()
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

        print "OnExit called \"" + arg.get_title() + "\""
        arg.set_title("Exiting ...")
        time.sleep(5);         
         
def handler(signum, frame):
        #print 'Signal handler called with signal', signum
        signal.alarm(1)
    


