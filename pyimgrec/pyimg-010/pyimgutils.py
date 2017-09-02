#!/usr/bin/env python

import os, sys, getopt, signal, array
import gobject, gtk, pango, time

# pyimgutils
# --------------------------------------------------------------------

class ofd():

    def __init__(self, msg = "Open File"):
        self.result = None
        self.old    = os.getcwd()
        butt =   "Cancel", gtk.BUTTONS_CANCEL, "OK", gtk.BUTTONS_OK
        fc = gtk.FileChooserDialog(msg, None, \
                        gtk.FILE_CHOOSER_ACTION_OPEN, butt)
        fc.set_current_folder(self.old)
        fc.set_default_response(gtk.BUTTONS_OK)
        fc.connect("response", self._done_opendlg)                
        fc.run()   
        
    def _done_opendlg(self, win, resp):
        os.chdir(self.old)        
        if resp == gtk.BUTTONS_OK:        
            try:
                fname = win.get_filename()
                if not fname:
                    msg("Must have filename")
                else:         
                    self.result = fname
            except:
                msg("Cannot open")
        win.destroy()                

# --------------------------------------------------------------------

def msg(xstr, xtype = gtk.MESSAGE_INFO):
    md = gtk.MessageDialog(flags=gtk.DIALOG_MODAL,
                type=xtype, buttons=gtk.BUTTONS_OK)
    md.set_markup(xstr); 
    md.run(); 
    md.destroy()
       

