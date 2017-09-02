#!/usr/bin/env python

import signal, os, time, gobject, gtk, string, pango

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

class pedDoc(gtk.DrawingArea):
    
    def __init__(self, buff, parent, appwin):
        
        # save params
        self.appwin = appwin; self.parwin = parent

        # init vars
        self.width = 0; self.height = 0
        self.arr = []
        self.caret = []; self.caret.append(0); self.caret.append(0)        
        self.text = str.split(buff, "\n")
             
        gtk.DrawingArea.__init__(self)
        self.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        self.pangolayout = self.create_pango_layout("a")

        # Set default background color
        '''colormap = gtk.widget_get_default_colormap()
        color = colormap.alloc_color("#d0d0d0")
        self.modify_bg(gtk.STATE_NORMAL, color)'''

        fd = pango.FontDescription()
        fd.set_size(14*1024); fd.set_family("mono")
        self.pangolayout.set_font_description(fd)

        # Get Pango steps
        self.cxx, self.cyy = self.pangolayout.get_pixel_size()

        self.www = gtk.gdk.screen_width();
        self.hhh = gtk.gdk.screen_height();
        
        # Start up with initial size 
        #self.set_size_request(3*self.www/4, 3*self.hhh/4)
        self.set_size_request(3*self.www/4, 2*self.hhh/4)

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
        self.connect("configure_event", self.configure_event)
        self.connect("size-request", self.size_request)
        self.connect("size-allocate", self.size_alloc)

    def size_request(self, widget, req):
        print "size_request", req

    def size_alloc(self, widget, req):
        print "size_alloc", req

    def configure_event(self, widget, event):
        print "configure_event", event
        self.grab_focus()
        self.width = 0; self.height = 0
        self.invalidate()
        #print self, event
        
    def draw_text(self, x, y, text):
        self.pangolayout.set_text(text)
        xx, yy = self.pangolayout.get_pixel_size()
        self.window.draw_layout(self.gc, x, y, self.pangolayout)
        return xx, yy

    def area_expose_cb(self, area, event):

        #print "area_expose_cb()", event.area.width, event.area.height

        if self.width == 0:
            print "setting new", event.area.width, event.area.height
            self.width = event.area.width
            self.height = event.area.height

        style = self.get_style()
        self.gc = style.fg_gc[gtk.STATE_NORMAL]
    
        maxx = 0; xx = 0; yy = 0
        for aa in self.text:
            dx, dy = self.draw_text(xx, yy, aa)
            self.arr.append([xx, yy]) 
            yy += dy
            if maxx < dx: maxx = dx
    
        #self.set_size_request(3*self.www/4, yy + 30)
        self.set_size_request(maxx + self.cxx, yy + self.cyy)
        self._drawcaret()        
        return True

    # --------------------------------------------------------------------
    # Draw caret

    def _drawcaret(self):

        #print "drawing caret", self.caret[0], self.caret[1], \
        #        self.caret[0] * self.cxx, self.caret[1] * self. cyy  
                
        colormap = gtk.widget_get_default_colormap()
        color = colormap.alloc_color("#008888")
        
        gcx = gtk.gdk.GC(self.window); gcx.copy(self.gc)
        gcx.set_foreground(color)
      
        xx = self.caret[0] * self.cxx #+ self.cxx / 2
        yy = self.caret[1] * self.cyy
        cw = self.cxx / 2

        # Top, left right, buttom
        self.window.draw_line(gcx, xx, yy, xx + cw, yy)
        self.window.draw_line(gcx, xx + 1, yy, xx + 1, yy + self.cyy )
        self.window.draw_line(gcx, xx + 3, yy, xx + 3, yy + self.cyy )
        self.window.draw_line(gcx, xx , yy + self.cyy, xx + cw, yy + self.cyy )

    def area_motion(self, area, event):
        #print "motion event", event
        pass

    # --------------------------------------------------------------------
    def set_caret(self, xx, yy):

        oldx = self.caret[0] * self.cxx; 
        oldy = self.caret[1] * self.cyy

        self.caret[0] = xx; self.caret[1] = yy

        # Low limit
        if self.caret[0] < 0: self.caret[0] = 0
        if self.caret[1] < 0: self.caret[1] = 0

        # High Limit
        xxx, yyy = self.window.get_size()
        xxx /= self.cxx; yyy /= self.cyy

        if self.caret[0] > xxx: self.caret[0] = xxx       
        if self.caret[1] > yyy: self.caret[1] = yyy       

        xx = self.caret[0] * self.cxx
        yy = self.caret[1] * self.cyy

        # Optimize cursor movement
        rect = gtk.gdk.Rectangle(xx, yy, self.cxx * self.cxx /2, self.cyy + 1)
        self.invalidate(rect)

        rect = gtk.gdk.Rectangle(oldx, oldy, self.cxx + self.cxx /2 , self.cyy + 1)
        self.invalidate(rect)

        # Put it back in view:        
        '''xx1, yy1 = self.appwin.get_size()
        px1, py1 = self.appwin.get_position()
        print "size1", xx1, yy1, "pos1", px1, py1

        xx2, yy2 = self.parwin.window.get_size()
        px2, py2 = self.parwin.window.get_position()
        print "size2", xx2, yy2, "pos2", px2, py2'''

        adj = self.parwin.get_vadjustment()
        #print "adj", int(adj.get_value()), int(adj.get_upper()), int(adj.get_lower() )
        #print self.height, self.width
            
        hhh = self.height - 3 * self.cxx
        if  yy > hhh  + adj.get_value():
            adj.set_value(yy - hhh)

        if  adj.get_value() > yy - self.cyy:
            adj.set_value(yy - self.cyy)
        
    def area_button(self, area, event):
        if  event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            ttt = "Press right mouse"
            #print "Right Click at x=", event.x, "y=", event.y
            self.poprclick(area, event)                       
        elif  event.type == gtk.gdk.BUTTON_PRESS and event.button == 1:
            ttt = "Press left mouse"
            print "Left Click at x=", event.x, "y=", event.y
            # Find current line    
            self.set_caret(int(event.x) / self.cxx, 
                                 int(event.y) / self.cyy )                                
        else:
            ttt = "Release"

        #print "button event ", "type = ", ttt, "x= ", event.x, \
        #    "y= ", event.y, "button = ", event.button                
        self.grab_focus()
        return True

    def area_key(self, area, event):
        ret = True
        #print "key event", area, event
        xidx = self.caret[0]; idx =  self.caret[1] 
        if  event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.Up:
                print "Up arrow"
                self.set_caret(self.caret[0], self.caret[1] - 1)
                ret = False

            elif event.keyval == gtk.keysyms.Down:
                self.set_caret(self.caret[0], self.caret[1] + 1)
                ret = False
            elif event.keyval == gtk.keysyms.Left:
                self.set_caret(self.caret[0] - 1, self.caret[1])
                ret = False
            elif event.keyval == gtk.keysyms.Right:
                self.set_caret(self.caret[0] + 1, self.caret[1])
            elif event.keyval == gtk.keysyms.Tab:
                self.set_caret(self.caret[0] + 1, self.caret[1])
            elif event.keyval == gtk.keysyms.Page_Up:
                self.set_caret(self.caret[0], self.caret[1] - 20)
            elif event.keyval == gtk.keysyms.Page_Down:
                self.set_caret(self.caret[0], self.caret[1] + 20)
            elif event.keyval == gtk.keysyms.Return:
                line = self.text[idx][:]                      
                self.text[idx] = line[xidx:];             
                self.text.insert(idx, "")
                self.text[idx] = line[:xidx]                
                self.set_caret(0, self.caret[1] + 1)
                self.invalidate()
            elif event.keyval == gtk.keysyms.Home:
                self.set_caret(0, self.caret[1])
            elif event.keyval == gtk.keysyms.End:
                xlen = len(self.text[idx])
                self.set_caret(xlen, self.caret[1])
            elif event.keyval == gtk.keysyms.BackSpace:
                if self.caret[0] > 0:
                    line = self.text[idx][:]      
                    self.text[idx] = line[:xidx - 1] + line[xidx:]                
                    self.set_caret(self.caret[0] - 1, self.caret[1])
                    self.inval_line()

            elif event.keyval == gtk.keysyms.Delete:
                if len(self.text[idx]):
                    line = self.text[idx][:]      
                    self.text[idx] = line[:xidx] + line[xidx+1:]                
                    self.set_caret(self.caret[0], self.caret[1])
                    self.inval_line()
                else:
                    del (self.text[idx])
                    self.invalidate()
                    
            else:
                print "Other", event.keyval
                line = self.text[idx][:]      
                ccc = ""
                try: ccc = chr(event.keyval) 
                except: pass

                self.text[idx] = line[:xidx] + ccc + line[xidx:]                
                self.set_caret(self.caret[0] + 1, self.caret[1])
                self.inval_line()
                
        #self.grab_focus()
        return True

     # Invalidate current line
    def inval_line(self):
        rect = gtk.gdk.Rectangle(0, self.caret[1] * self.cyy, 
                self.www, self.cyy)
        self.invalidate(rect)
   
    def invalidate(self, rect = None):                        
        if rect == None:
            ww, hh = self.window.get_size()
            rect = gtk.gdk.Rectangle(0,0, ww, hh)
        #print "Invalidate:", rect
        self.window.invalidate_rect(rect, False)

    def area_focus(self, area, event):
        #print "area focus", area, event
        return False

    def poprclick(self, widget, event):
        #print "Making rclick"
        mm = self.build_menu(self.window, rclick_menu)
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

    def create_menuitem(self, string, action):
        rclick_menu = gtk.MenuItem(string)
        rclick_menu.connect("activate", action, string);
        rclick_menu.show()        
        return rclick_menu
   
        # Create the menubar and toolbar
        action_group = gtk.ActionGroup("DocWindowActions")
        action_group.add_actions(entries)      
        return action_group

    def build_menu(self, window, items):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.Menu, "<pydoc>", accel_group)
        item_factory.create_items(items)
        self.item_factory = item_factory
        return item_factory.get_widget("<pydoc>")

 
