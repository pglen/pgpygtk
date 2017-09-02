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
    print "Hello ", arg.name,  HelloDoc.num
    hello.draw_lines(310, 10)
    
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
            ( "/File/Quit",     "<control>Q", gtk.main_quit, 0, None ),
            
            ( "/_Options",      None,         None, 0, "<Branch>" ),
            ( "/Options/Test",  None,         None, 0, None ),
            
            ( "/_Help",         None,         None, 0, "<LastBranch>" ),
            ( "/_Help/About",   None,         None, 0, None ),
            ( "/sep1",     None,         None, 0, "<Separator>" ),
            ( "/Exit",          "<alt>x",        None, 0, None ),
            )

    
# ------------------------------------------------------------------------

def create_action_group(self):
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

