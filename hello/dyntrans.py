#!/usr/bin/env python

import os, pygtk, gobject, pango, gtk

class RoundRect:

    # When invoked (via signal delete_event), terminates the application
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def roundrect(self, pixmap, gc, rr, ww, hh):

        if rr > ww or rr > hh:
            raise ValueError, "Radius cannot be larger then width or height"

        pixmap.draw_arc(gc, True, 0, 0, rr, rr, 00, 360*64)
        pixmap.draw_arc(gc, True, ww-rr, 0, rr, rr, 00, 360*64)
        pixmap.draw_arc(gc, True, 0, hh-rr, rr, rr, 00, 360*64)
        pixmap.draw_arc(gc, True, ww-rr, hh-rr, rr, rr, 00, 360*64)

        pixmap.draw_rectangle(gc, True, rr/2, 0, ww-rr, rr)
        pixmap.draw_rectangle(gc, True, rr/2, hh-rr, ww-rr, hh)
        pixmap.draw_rectangle(gc, True, 0, rr/2, ww, hh-rr)
        
    def __init__(self, ww = 300, hh = 200, rr = 0):

        if rr == 0:
            rr = min(ww,hh) / 2;

        window = gtk.Window(gtk.WINDOW_POPUP)
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)

        window.set_events(window.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        window.set_events(window.get_events() | gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)
        
        window.connect("delete_event", self.close_application)
        window.connect("button_press_event", self.close_application)
        window.connect("key-press-event", self.close_application)

        #window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        window.show()
        colormap = window.get_colormap()
        
        # Calculate text size



        image = gtk.Image()
        
        pixbuff = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, ww, hh);
        #pixbuff.fill(0xffff90ff)
        #image.set_from_pixbuf(pixbuff)         
               
        pixmap, mask = pixbuff.render_pixmap_and_mask() 
        gc = gtk.gdk.GC(pixmap)
        
        color = colormap.alloc_color("#00aa00")
        gc.set_foreground(color)
        pixmap.draw_rectangle(gc, True, 0, 0, ww, hh)
        
        color = colormap.alloc_color("#ffff90")
        gc.set_foreground(color)

        self.roundrect(pixmap, gc, rr, ww, hh)
                
        pixbuff2 = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, ww, hh);
        pixbuff2.get_from_drawable(pixmap, pixmap.get_colormap(), 0, 0, 0, 0, ww, hh)

        pixbuff3 = pixbuff2.add_alpha(True, 0x00, 0xaa, 0x00)

        pixmap, mask = pixbuff3.render_pixmap_and_mask() 
        gc = gtk.gdk.GC(pixmap)
        
        color = colormap.alloc_color("#000000")
        gc.set_foreground(color)

        cairo = pixmap.cairo_create()
        lay = cairo.create_layout()        

        fd = pango.FontDescription()       
        fd.set_size(12*1024)        
        lay.set_font_description(fd)

        #lay.set_text("Please set <b>Password</b> for 'user' ")
        lay.set_markup("Please set <b>Password</b> for 'user\nhere'" \
        "<span foreground=\"blue\" size=\"100\">Blue text</span> is <i>cool</i>")

        #lay.parse_markup("Please set <b>Password</b> for 'user\nhere' ")
        dim = lay.get_pixel_size()

        pixmap.draw_layout(gc, pixmap.get_size()[0] / 2 - dim[0] / 2,
                     pixmap.get_size()[1] / 2 - dim[1] / 2, lay)

        image.set_from_pixmap(pixmap, mask)
        image.show()

        fixed = gtk.Fixed(); fixed.put(image, 0, 0)
        window.add(fixed); fixed.show()

        # This masks out everything except for the image itself
        #if mask != None:
        #    window.shape_combine_mask(mask, 0, 0)
      
        window.move(gtk.gdk.screen_width() - (pixmap.get_size()[0] + 20), 40 )      
        window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    RoundRect(600, 300)
    main()


