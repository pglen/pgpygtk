#!/usr/bin/env python

import sys, os, pygtk, gobject, pango, gtk

class View(gtk.Window):

    def keypress(self, win, key):
        #print key.keyval        

        if key.keyval == 65307:
            gtk.main_quit()
            return False

        if key.keyval == 32:
            print "Space"
                        
            return False
        
    # When invoked (via signal delete_event), terminates the application
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self, strx="No Content to display"):

        gtk.Window.__init__(self)

        #window = gtk.Window(gtk.WINDOW_POPUP)
        window = gtk.Window()
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)
        window.set_decorated(False)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
           
        mask = gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.KEY_PRESS_MASK | \
               gtk.gdk.KEY_RELEASE_MASK

        window.set_events(window.get_events() | mask)
        
        window.connect("delete_event", self.close_application)
        #window.connect("button_press_event", self.close_application)
        window.connect("key-press-event", self.keypress)

        hbox = gtk.HBox() ; hbox.show()

        # ----------------------------------------------------------------
        # Header
        frame2 = gtk.Frame()
        frame2.show()
        #frame2.set_border_width(10)
        
        label2 = gtk.Label();  label2.set_text( " Header " )
        label2.show()
        frame2.add(label2)

        label1 = gtk.Label(); label1.set_text("  "); label1.show()
        
        label3 = gtk.Label(); label3.set_text("     "); label3.show()
        
        hbox.pack_start(label1, False)
        hbox.add(frame2)
        hbox.pack_start(label3, False)

        # ----------------------------------------------------------------
        # Body

        ws = gtk.ScrolledWindow()
        ws.set_border_width(10)
        ws.show()

        vbox = gtk.VBox();  vbox.show()

        #label = gtk.Label()
        #label.set_markup(strx)
        #label.show()
        buffer = gtk.TextBuffer()
        self.text_view = gtk.TextView(buffer)
        self.drawing = gtk.DrawingArea()
        #layout =  self.drawing.create_pango_layout()
        
        strx = sys.argv[1]    
        f = open(strx)
        buf = f.read()

        try:
            attrlist = pango.parse_markup(buf)
        except:
            print "Cannot load file"
         
        #print buf
        #buffer.insert_at_cursor(buf)

        
        frame = gtk.Frame()        
        frame.show()

        ws.add_with_viewport(self.text_view)
        ws.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        frame.add(vbox)
        vbox.pack_start(hbox, False)
        vbox.add(ws)

        window.add(frame); 
                
        window.set_default_size(2*gtk.gdk.screen_width()/3, 2*gtk.gdk.screen_height()/3 )
        window.grab_focus()

        #window.move(gtk.gdk.screen_width() - (pixmap.get_size()[0] + 20), 40 )      
        window.show()


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    strx = sys.argv[1]    
    f = open(strx)
    buf = f.read()
    f.close()
        
    View(buf)
    main()


