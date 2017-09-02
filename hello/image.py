#!/usr/bin/env python

# example wheelbarrow.py

import os, pygtk, gobject, pango, gtk

class ImageExample:
    # When invoked (via signal delete_event), terminates the application
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_POPUP)
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)

        window.set_events(window.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        window.set_events(window.get_events() | gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)
        
        window.connect("delete_event", self.close_application)
        window.connect("button_press_event", self.close_application)
        window.connect("key-press-event", self.close_application)

        ww = 200; hh = 100

        #window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        window.show()

        #pixmap = gtk.gdk.pixbuf_new_from_file("/usr/share/pixmaps/gnome-logo-large.png")        
        #image = gtk.image_new_from_file("/usr/share/pixmaps/gnome-logo-large.png")
        #image = gtk.image_new_from_file("/usr/share/pixmaps/gnome-background-image.png")
        #image = gtk.image_new_from_file("/usr/share/pixmaps/gnome-tigert.png")
        #fname = os.getcwd()+ "/rect.png"
        #print fname        
        
        pixbuff = gtk.gdk.pixbuf_new_from_file("rect.png")

        image = gtk.Image()
        
        pixmap, mask3 = pixbuff.render_pixmap_and_mask() 

        gc = gtk.gdk.GC(pixmap)

        colormap = window.get_colormap()
        color = colormap.alloc_color("#000000")
        gc.set_foreground(color)

        cairo = pixmap.cairo_create()
        lay = cairo.create_layout()        
        fd = pango.FontDescription()       
        fd.set_size(12*1024)        
        lay.set_font_description(fd)

        lay.set_text("Please set Password for 'user' ")
        dim = lay.get_pixel_size()

        pixmap.draw_layout(gc, pixmap.get_size()[0] / 2 - dim[0] / 2,
                     pixmap.get_size()[1] / 2 - dim[1] / 2, lay)

        image.set_from_pixmap(pixmap, mask3)
        image.show()

        # To display the image, we use a fixed widget to place the image
        fixed = gtk.Fixed()
        fixed.put(image, 0, 0)
        window.add(fixed)
        fixed.show()

        # This masks out everything except for the image itself
        if mask3 != None:
            window.shape_combine_mask(mask3, 0, 0)
      
        window.move(gtk.gdk.screen_width() - (pixmap.get_size()[0] + 20), 40 )
       
        # show the window
        window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ImageExample()
    main()


