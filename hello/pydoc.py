#!/usr/bin/env python

import signal, os, time, gobject, gtk, string

#global hello = 1234

#print __name__

def print_hello(self, arg):
    print "Hello ", arg.name,  HelloDoc.num
    hello.draw_lines(310, 10)
    
menu_items = (
            ( "/New",           None,         print_hello, 0, None ),
            ( "/Open",          "<control>O", print_hello, 0, None ),
            ( "/Save",          "<control>S", print_hello, 0, None ),
            ( "/Save _As",       None,        None, 0, None ),
            ( "/sep1",     None,         None, 0, "<Separator>" ),
            
            ( "/_File",         None,         None, 0, "<Branch>" ),
            ( "/File/_New",     "<control>N", print_hello, 0, None ),
            ( "/File/_Open",    "<control>O", print_hello, 0, None ),
            ( "/File/_Save",    "<control>S", print_hello, 0, None ),
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

class HelloDoc(gtk.DrawingArea):

    num = 10
    
    def __init__(self):
        
        #print hello
        # Create the widget
        gtk.DrawingArea.__init__(self)
        self.pangolayout = self.create_pango_layout("")
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)

        self.set_events(gtk.gdk.POINTER_MOTION_MASK |
                                gtk.gdk.POINTER_MOTION_HINT_MASK |
                                gtk.gdk.BUTTON_PRESS_MASK |
                                gtk.gdk.BUTTON_RELEASE_MASK |
                                gtk.gdk.KEY_PRESS_MASK |
                                gtk.gdk.KEY_RELEASE_MASK )

        #self.set_events( gtk.gdk.ALL_EVENTS_MASK )

        self.connect("expose-event", self.area_expose_cb)
        self.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        self.connect("key-release-event", self.area_key)
        self.connect("focus", self.area_focus)

    # Drawing primitives       
    def draw_point(self, x, y):
        self.window.draw_point(self.gc, x+30, y+30)
        self.pangolayout.set_text("Point")
        self.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_points(self, x, y):
        points = [(x+10,y+10), (x+10,y), (x+40,y+30),
                 (x+30,y+10), (x+50,y+10)]
        self.window.draw_points(self.gc, points)
        self.pangolayout.set_text("Points")
        self.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_line(self, x, y):
        self.window.draw_line(self.gc, x+10, y+10, x+20, y+30)
        self.pangolayout.set_text("Line")
        self.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_lines(self, x, y):
        points = [(x+10,y+10), (x+10,y), (x+40,y+30),
                  (x+30,y+10), (x+50,y+10)]
        self.window.draw_lines(self.gc, points)
        self.pangolayout.set_text("Lines")
        self.window.draw_layout(self.gc, x+5, y+50, self.pangolayout)
        return

    def draw_segments(self, x, y):
        segments = ((x+20,y+10, x+20,y+70), (x+60,y+10, x+60,y+70),
            (x+10,y+30 , x+70,y+30), (x+10, y+50 , x+70, y+50))
        self.window.draw_segments(self.gc, segments)
        self.pangolayout.set_text("Segments")
        self.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def draw_rectangles(self, x, y):
        self.window.draw_rectangle(self.gc, False, x, y, 80, 70)
        self.window.draw_rectangle(self.gc, True, x+10, y+10, 20, 20)
        self.window.draw_rectangle(self.gc, True, x+50, y+10, 20, 20)
        self.window.draw_rectangle(self.gc, True, x+20, y+50, 40, 10)
        self.pangolayout.set_text("Rectangles")
        self.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def draw_arcs(self, x, y):
        self.window.draw_arc(self.gc, False, x+10, y, 70, 70,
                                  0, 360*64)
        self.window.draw_arc(self.gc, True, x+30, y+20, 10, 10,
                                  0, 360*64)
        self.window.draw_arc(self.gc, True, x+50, y+20, 10, 10,
                                   0, 360*64)
        self.window.draw_arc(self.gc, True, x+30, y+10, 30, 50,
                                  210*64, 120*64)
        self.pangolayout.set_text("Arcs")
        self.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def draw_pixmap(self, x, y):
        pixmap, mask = gtk.gdk.pixmap_create_from_xpm(
            self.window, self.style.bg[gtk.STATE_NORMAL], "list-med.png.xpm")

        self.window.draw_drawable(self.gc, pixmap, 0, 0, x+15, y+25,
                                      -1, -1)
        self.pangolayout.set_text("Pixmap")
        self.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return 

    def draw_polygon(self, x, y):
        points = [(x+10,y+60), (x+10,y+20), (x+40,y+70),
                  (x+30,y+30), (x+50,y+40)]
        self.window.draw_polygon(self.gc, True, points)
        self.pangolayout.set_text("Polygon")
        self.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def draw_rgb_image(self, x, y):
        b = 80*3*80*['\0']
        for i in range(80):
            for j in range(80):
                b[3*80*i+3*j] = chr(255-3*i)
                b[3*80*i+3*j+1] = chr(255-3*abs(i-j))
                b[3*80*i+3*j+2] = chr(255-3*j)
        buff = string.join(b, '')
        self.window.draw_rgb_image(self.gc, x, y, 80, 80,
                                gtk.gdk.RGB_DITHER_NONE, buff, 80*3)

        self.pangolayout.set_text("RGB Image")
        self.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def area_expose_cb(self, area, event):
        #print "area expose event called"
        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
        self.draw_point(10,10)
        self.draw_points(110, 10)
        self.draw_line(210, 10)
        self.draw_lines(310, 10)
        self.draw_segments(10, 100)
        self.draw_rectangles(110, 100)
        self.draw_arcs(210, 100)
        self.draw_pixmap(310, 100)
        self.draw_polygon(10, 200)
        self.draw_rgb_image(110, 200)
        return True

    def area_motion(self, area, event):
        #print "motion event", event
        pass

    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            ttt = "Press right"
            #print "Right Click at x=", event.x, "y=", event.y
            self.poprclick(area, event)                       
        else:
            ttt = "Release"

        #print "button event ", "type = ", ttt, "x= ", event.x, \
        #    "y= ", event.y, "button = ", event.button
                
        self.grab_focus()

    def area_key(self, area, event):
        #print "key event", area, event
        pass

    def area_focus(self, area, event):
        print "area focus", area, event

    def poprclick(self, widget, event):

        #print "Making rclick"
        mm = self.build_menu(self.window, menu_items)
        mm.popup(None, None, None, event.button, event.time)

        # Create a new menu-item with a name...
        #menu = gtk.Menu()
        #menu.append(self.create_menuitem("Menu 1", self.menuitem_response1))
        #menu.append(self.create_menuitem("Menu 2", self.menuitem_response2))
        #menu.append(self.create_menuitem("Menu 3", self.menuitem_response3))
        #menu.popup(None, None, None, event.button, event.time)

    def menuitem_response1(self, widget, string):
        self.draw_segments(10, 200)
        print "response1 %s" % string

    def menuitem_response2(self, widget, string):
        print "response2 %s" % string

    def menuitem_response3(self, widget, string):
        print "response3 %s" % string

    def activate_action(self, action):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
            'You activated action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def  create_menuitem(self, string, action):
        menu_items = gtk.MenuItem(string)
        menu_items.connect("activate", action, string);
        menu_items.show()        
        return menu_items
   
        # Create the menubar and toolbar
        action_group = gtk.ActionGroup("DocWindowActions")
        action_group.add_actions(entries)
      
        return action_group

    def build_menu(self, window, items):

        accel_group = gtk.AccelGroup()

        # This function initializes the item factory.
        # Param 1: The type of menu - can be MenuBar, Menu,
        #          or OptionMenu.
        # Param 2: The path of the menu.
        # Param 3: A reference to an AccelGroup. The item factory sets up
        #          the accelerator table while generating menus.
        item_factory = gtk.ItemFactory(gtk.Menu, "<pydoc>", accel_group)

        # This method generates the menu items. Pass to the item factory
        #  the list of menu items
        item_factory.create_items(items)

        # Attach the new accelerator group to the window.
        #window.add_accel_group(accel_group)

        # need to keep a reference to item_factory to prevent its destruction
        self.item_factory = item_factory
        # Finally, return the actual menu bar created by the item factory.
        return item_factory.get_widget("<pydoc>")

 
