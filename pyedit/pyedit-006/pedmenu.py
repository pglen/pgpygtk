#!/usr/bin/env python


import gtk

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

def rclick_print(self, arg):
    print "Hello ", arg.name

def rclick_quit(self, arg):
    print "Quit ", arg.name
    
rclick_menu = (
            ( "/New",           None,         rclick_print, 0, None ),
            ( "/Open",          "<control>O", rclick_print, 0, None ),
            ( "/Save",          "<control>S", rclick_print, 0, None ),
            ( "/Save _As",       None,        None, 0, None ),
            ( "/sep1",     None,         None, 0, "<Separator>" ),
            
            ( "/_File",         None,         None, 0, "<Branch>" ),
            ( "/File/_New",     "<control>N", rclick_print, 0, None ),
            ( "/File/_Open",    "<control>O", rclick_print, 0, None ),
            ( "/File/_Save",    "<control>S", rclick_print, 0, None ),
            ( "/File/Save _As", None,         None, 0, None ),            
            ( "/File/sep1",     None,         None, 0, "<Separator>" ),
            ( "/File/Quit",     "<control>Q", rclick_quit , 0, None ),
            
            ( "/_Options",      None,         None, 0, "<Branch>" ),
            ( "/Options/Test",  None,         None, 0, None ),
            
            ( "/_Help",         None,         None, 0, "<LastBranch>" ),
            ( "/_Help/About",   None,         None, 0, None ),
            ( "/sep1",     None,         None, 0, "<Separator>" ),
            ( "/Exit",          "<alt>x",        rclick_quit, 0, None ),
            )
    
# ------------------------------------------------------------------------

def create_action_group(self):
    # GtkActionEntry
    entries = (
      ( "FileMenu", None, "_File" ),               # name, stock id, label
      ( "EditMenu", None, "_Edit" ),                # name, stock id, label
      ( "PreferencesMenu", None, "Se_ttings" ),     # name, stock id, label
      ( "NavMenu", None, "N_avigation" ),            # name, stock id, label
      ( "MacrosMenu", None, "_Macros" ),            # name, stock id, label
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
      ( "Close", gtk.STOCK_CLOSE,                   # name, stock id
        "_Close","<control>W",                      # label, accelerator
        "Close a file",                             # tooltip
        self.activate_action ),
      ( "Save", gtk.STOCK_SAVE,                    # name, stock id
        "_Save","<control>S",                      # label, accelerator
        "Save current file",                       # tooltip
        self.activate_action ),
      ( "SaveAs", gtk.STOCK_SAVE,                  # name, stock id
        "Save _As...", "<control><shift>S",        # label, accelerator
        "Save to a file",                          # tooltip
        self.activate_action ),
      ( "Quit", gtk.STOCK_QUIT,                      # name, stock id
        "_Quit (No Save)", "<control>Q",             # label, accelerator
        "Quit program, abandon files",               # tooltip
         self.activate_quit ),
      ( "Exit", gtk.STOCK_QUIT,                      # name, stock id
        "_Exit", "<alt>X",                           # label, accelerator
        "Exit program, save files",                  # tooltip
         self.activate_exit ),

      ( "Cut", gtk.STOCK_COPY,                       # name, stock id
        "C_ut   \tCtrl-C", "",                         # label, accelerator
        "Cut selection to clipboard",                # tooltip
         self.activate_action ),

       ( "Copy", gtk.STOCK_COPY,                      # name, stock id
        "_Copy   \tCtrl-C", "",                         # label, accelerator
        "Copy selection to clipboard",                # tooltip
         self.activate_action ),

      ( "Paste", gtk.STOCK_PASTE,                     # name, stock id
        "_Paste  \tCtrl-V", "",                         # label, accelerator
        "Paste clipboard into text",                  # tooltip
         self.activate_action ),

      ( "Goto", gtk.STOCK_MEDIA_FORWARD,              # name, stock id
        "Goto Line\tAlt-G", "",                              # label, accelerator
        "Goto line in file",                          # tooltip
         self.activate_action ),

      ( "Find", gtk.STOCK_MEDIA_FORWARD,              # name, stock id
        "Find in file \tCtrl-F", "",                           # label, accelerator
        "Find line in file",                          # tooltip
         self.activate_action ),

      ( "Record", gtk.STOCK_MEDIA_RECORD,          # name, stock id
        "Start/Stop Record\tF7", "",               # label, accelerator
        "Record macro",                            # tooltip
         self.activate_action ),
      ( "Play", gtk.STOCK_MEDIA_PLAY,            # name, stock id
        "Play Macro        \tF8", "",                     # label, accelerator
        "Play macro",                           # tooltip
         self.activate_action ),
      ( "Animate", None,                        # name, stock id
        "_Animate", None,                       # label, accelerator
        "Play macro with animation effect",      # tooltip
         self.activate_action ),
      ( "Savemacro", None,                        # name, stock id
        "Save macro", None,                       # label, accelerator
        "Save macro to file",      # tooltip
         self.activate_action ),
      ( "Loadmacro", None,                        # name, stock id
        "Load macro", None,                       # label, accelerator
        "Load macro from file",      # tooltip
         self.activate_action ),

      ( "Colors", None,                        # name, stock id
        "Set Colors", None,                       # label, accelerator
        "Set Editor window colors",      # tooltip
         self.activate_action ),

      ( "Fonts", None,                          # name, stock id
        "Set fonts", None,                      # label, accelerator
        "Set Editor window fonts",              # tooltip
         self.activate_action ),

      ( "About", None,                             # name, stock id
        "_About", "",                              # label, accelerator
        "About",                                   # tooltip
        self.activate_about ),
      ( "QuickHelp", None,                         # name, stock id
        "_Quick Help", "",                         # label, accelerator
        "Show quick help",                         # tooltip
        self.activate_qhelp ),
      ( "Help", None,                             # name, stock id
        "_Help", "",                              # label, accelerator
        "Show help",                              # tooltip
        self.activate_qhelp ),
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
    #action_group.add_toggle_actions(toggle_entries)
    #action_group.add_radio_actions(color_entries, COLOR_RED, self.activate_radio_action)
    #action_group.add_radio_actions(shape_entries, SHAPE_OVAL, self.activate_radio_action)

    return action_group

