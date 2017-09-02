#!/usr/bin/env python

# example wheelbarrow.py

import os, pygtk, gobject, pango

#pygtk.require('2.0')

import gtk

# XPM
WheelbarrowFull_xpm = [
"48 48 64 1",
"       c None",
".      c #DF7DCF3CC71B",
"X      c #965875D669A6",
"o      c #71C671C671C6",
"O      c #A699A289A699",
"+      c #965892489658",
"@      c #8E38410330C2",
"#      c #D75C7DF769A6",
"$      c #F7DECF3CC71B",
"%      c #96588A288E38",
"&      c #A69992489E79",
"*      c #8E3886178E38",
"=      c #104008200820",
"-      c #596510401040",
";      c #C71B30C230C2",
":      c #C71B9A699658",
">      c #618561856185",
",      c #20811C712081",
"<      c #104000000000",
"1      c #861720812081",
"2      c #DF7D4D344103",
"3      c #79E769A671C6",
"4      c #861782078617",
"5      c #41033CF34103",
"6      c #000000000000",
"7      c #49241C711040",
"8      c #492445144924",
"9      c #082008200820",
"0      c #69A618611861",
"q      c #B6DA71C65144",
"w      c #410330C238E3",
"e      c #CF3CBAEAB6DA",
"r      c #71C6451430C2",
"t      c #EFBEDB6CD75C",
"y      c #28A208200820",
"u      c #186110401040",
"i      c #596528A21861",
"p      c #71C661855965",
"a      c #A69996589658",
"s      c #30C228A230C2",
"d      c #BEFBA289AEBA",
"f      c #596545145144",
"g      c #30C230C230C2",
"h      c #8E3882078617",
"j      c #208118612081",
"k      c #38E30C300820",
"l      c #30C2208128A2",
"z      c #38E328A238E3",
"x      c #514438E34924",
"c      c #618555555965",
"v      c #30C2208130C2",
"b      c #38E328A230C2",
"n      c #28A228A228A2",
"m      c #41032CB228A2",
"M      c #104010401040",
"N      c #492438E34103",
"B      c #28A2208128A2",
"V      c #A699596538E3",
"C      c #30C21C711040",
"Z      c #30C218611040",
"A      c #965865955965",
"S      c #618534D32081",
"D      c #38E31C711040",
"F      c #082000000820",
"                                                ",
"          .XoO                                  ",
"         +@#$%o&                                ",
"         *=-;#::o+                              ",
"           >,<12#:34                            ",
"             45671#:X3                          ",
"               +89<02qwo                        ",
"e*                >,67;ro                       ",
"ty>                 459@>+&&                    ",
"$2u+                  ><ipas8*                  ",
"%$;=*                *3:.Xa.dfg>                ",
"Oh$;ya             *3d.a8j,Xe.d3g8+             ",
" Oh$;ka          *3d$a8lz,,xxc:.e3g54           ",
"  Oh$;kO       *pd$%svbzz,sxxxxfX..&wn>         ",
"   Oh$@mO    *3dthwlsslszjzxxxxxxx3:td8M4       ",
"    Oh$@g& *3d$XNlvvvlllm,mNwxxxxxxxfa.:,B*     ",
"     Oh$@,Od.czlllllzlmmqV@V#V@fxxxxxxxf:%j5&   ",
"      Oh$1hd5lllslllCCZrV#r#:#2AxxxxxxxxxcdwM*  ",
"       OXq6c.%8vvvllZZiqqApA:mq:Xxcpcxxxxxfdc9* ",
"        2r<6gde3bllZZrVi7S@SV77A::qApxxxxxxfdcM ",
"        :,q-6MN.dfmZZrrSS:#riirDSAX@Af5xxxxxfevo",
"         +A26jguXtAZZZC7iDiCCrVVii7Cmmmxxxxxx%3g",
"          *#16jszN..3DZZZZrCVSA2rZrV7Dmmwxxxx&en",
"           p2yFvzssXe:fCZZCiiD7iiZDiDSSZwwxx8e*>",
"           OA1<jzxwwc:$d%NDZZZZCCCZCCZZCmxxfd.B ",
"            3206Bwxxszx%et.eaAp77m77mmmf3&eeeg* ",
"             @26MvzxNzvlbwfpdettttttttttt.c,n&  ",
"             *;16=lsNwwNwgsvslbwwvccc3pcfu<o    ",
"              p;<69BvwwsszslllbBlllllllu<5+     ",
"              OS0y6FBlvvvzvzss,u=Blllj=54       ",
"               c1-699Blvlllllu7k96MMMg4         ",
"               *10y8n6FjvllllB<166668           ",
"                S-kg+>666<M<996-y6n<8*          ",
"                p71=4 m69996kD8Z-66698&&        ",
"                &i0ycm6n4 ogk17,0<6666g         ",
"                 N-k-<>     >=01-kuu666>        ",
"                 ,6ky&      &46-10ul,66,        ",
"                 Ou0<>       o66y<ulw<66&       ",
"                  *kk5       >66By7=xu664       ",
"                   <<M4      466lj<Mxu66o       ",
"                   *>>       +66uv,zN666*       ",
"                              566,xxj669        ",
"                              4666FF666>        ",
"                               >966666M         ",
"                                oM6668+         ",
"                                  *4            ",
"                                                ",
"                                                "
]

class WheelbarrowExample:
    # When invoked (via signal delete_event), terminates the application
    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create the main window, and attach delete_event signal to terminate
        # the application.  Note that the main window will not have a titlebar
        # since we're making it a popup.
        window = gtk.Window(gtk.WINDOW_POPUP)
        window.set_flags(gtk.CAN_FOCUS | gtk.SENSITIVE)

        window.connect("delete_event", self.close_application)
        window.set_events(window.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        window.set_events(window.get_events() | gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)
        window.connect("button_press_event", self.close_application)
        window.connect("key-press-event", self.close_application)

        ww = 320; hh = 100

        #window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        window.move(gtk.gdk.screen_width() - (ww + 20), 40 )
        window.show()

        # Now for the pixmap and the image widget
        #pixmap, mask = gtk.gdk.pixmap_create_from_xpm_d(
        #    window.window, None, WheelbarrowFull_xpm)

        #pixmap = gtk.gdk.pixbuf_new_from_file("/usr/share/pixmaps/gnome-logo-large.png")
        
        #image = gtk.image_new_from_file("/usr/share/pixmaps/gnome-logo-large.png")
        #image = gtk.image_new_from_file("/usr/share/pixmaps/gnome-background-image.png")
        image = gtk.image_new_from_file("/usr/share/pixmaps/gnome-tigert.png")
        fname = os.getcwd()+ "/rect.png"
        #print fname
        #image = gtk.image_new_from_file(fname)
        #pixbuff = image.get_pixbuf()
        #print image

        #pixbuff = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 300, 300);
        #pixbuff.fill(0xfffaafff)

        pixmap = gtk.gdk.Pixmap(window.window, ww, hh, depth=-1)
        gc = gtk.gdk.GC(pixmap)

        colormap = window.get_colormap()
        color = colormap.alloc_color("#ff8080")
        gc.set_foreground(color)
        pixmap.draw_rectangle(gc, True, 0, 0, ww, hh)
        
        color = colormap.alloc_color("#000000")
        gc.set_foreground(color)
        gc.line_width = 4
        gc.cap_style = gtk.gdk.CAP_ROUND

        #pixmap.draw_line(gc, 10, 10, ww-10, hh-10)
        #pixmap.draw_line(gc, ww-10, 10, 10, hh-10)
   
        cairo = pixmap.cairo_create()
        lay = cairo.create_layout()        
        fd = pango.FontDescription()       
        fd.set_size(14*1024)        
        lay.set_font_description(fd)

        lay.set_text("Please set Password for 'user' ")
        dim = lay.get_pixel_size()

        pixmap.draw_layout(gc, pixmap.get_size()[0] / 2 - dim[0] / 2,
                     pixmap.get_size()[1] / 2 - dim[1], lay)

        lay.set_text("Please set Password for 'root'")
        dim = lay.get_pixel_size()
        
        pixmap.draw_layout(gc, pixmap.get_size()[0] / 2 - dim[0] / 2,
                     pixmap.get_size()[1] / 2, lay)

        image2 = gtk.Image()
        image2.set_from_pixmap(pixmap, None)        
        image2.show()

        #rect = gtk.gdk.Rectangle(100, 100, 200, 200)
        #region = gtk.gdk.region_rectangle(rect)
        #window.shape_combine_region(region, 0, 0)        
        
        # To display the image, we use a fixed widget to place the image
        fixed = gtk.Fixed()
        fixed.put(image, 0, 0)
        window.add(fixed)
        fixed.show()

        maskmap = gtk.gdk.Pixmap(window.window, ww, hh, depth=-1)
        gc = gtk.gdk.GC(maskmap)        

        gc.set_rgb_fg_color(gtk.gdk.Color(0, 0, 0))                     
        maskmap.draw_rectangle(gc, True, 0, 0, ww, hh)
        
        gc.set_rgb_fg_color(gtk.gdk.Color(0xffff,0xffff,0xffff))             
        maskmap.draw_rectangle(gc, True, 20, 20, ww-40, hh-40)
        
        maskbuff = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, ww, hh)
        maskbuff.get_from_drawable(maskmap,  gtk.gdk.colormap_get_system(), \
                        0, 0, 0, 0, ww, hh)        
                
        maskbuff.add_alpha(True, 0, 0, 0);

        mask2, mask3 = maskbuff.render_pixmap_and_mask()    
            
        #image3 = gtk.Image()
        #image3.set_from_pixmap(mask2, None)        
        #image3.show()
        #fixed.put(image3, 0, 0)
        # This masks out everything except for the image itself
        #window.shape_combine_mask(mask3, 0, 0)
               
        # show the window
        window.show()

def desktop_expose(area, event):         
    print "desktop event called"        
    #desktop.draw_rectangle(gc, True, 0, 0, 300, 300)        

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    WheelbarrowExample()
    main()
