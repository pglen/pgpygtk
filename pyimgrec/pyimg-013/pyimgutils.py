#!/usr/bin/env python

import os, sys, getopt, signal, array
import gobject, gtk, pango, time, traceback

# ------------------------------------------------------------------------
# Print an exception as the system would print it

def print_exception(xstr):
    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt: 
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print "Could not print trace stack. ", sys.exc_info()
    print cumm

# pyimgutils
# --------------------------------------------------------------------

class ofd():

    def __init__(self, msg = "Open File", 
                mode=gtk.FILE_CHOOSER_ACTION_OPEN):
        self.result = None
        self.old    = os.getcwd()
        butt =   "Cancel", gtk.BUTTONS_CANCEL, "OK", gtk.BUTTONS_OK
        fc = gtk.FileChooserDialog(msg, None, mode, butt)
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
       
# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        gtk.main_iteration_do(False)        
      






