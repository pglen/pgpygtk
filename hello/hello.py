#!/usr/bin/env python

import gobject
import gtk
import mainwin

def main():

    mw = mainwin.AppMainWindow()
    #print mw.getwinx(), mainwin.winx, 12

    #mw.get_window()
    #gc = gtk.gdk.GC(win)
    #ww = gtk.Window.get_window(mainwin.AppMainWindow)
    #ww.draw_rectangle(gc, True, 10,10, 10,10)

    print "Started App"
    gtk.main()
    print "Exited app"
            

if __name__ == '__main__':
    main()
