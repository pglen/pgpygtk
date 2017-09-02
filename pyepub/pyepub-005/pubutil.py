#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import traceback
import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")

# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the class      

class Config:

    def __init__(self, optarr):
        self.optarr = optarr

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            optletters += aa[0]
        #print optletters    
        # Create defaults:
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        except getopt.GetoptError, err:
            print "Invalid option(s) on command line:", err
            return ()
            
        #print "opts", opts, "args", args
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print "match", aa, self.optarr[bb]
                    if len(self.optarr[bb][0]) > 1:
                        #print "arg", self.optarr[bb][1], aa[1]
                        if self.optarr[bb][2] != None: 
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print "set", self.optarr[bb][1], self.optarr[bb][2]
                        if self.optarr[bb][2] != None: 
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print "call", self.optarr[bb][3]
                        if self.optarr[bb][3] != None: 
                            self.optarr[bb][3]()
        return args

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

# ------------------------------------------------------------------------
# Never mind

def cmp(aa, bb):
    aaa = os.path.basename(aa);  bbb = os.path.basename(bb)
    pat = re.compile("[0-9]+")
    ss1 = pat.search(aaa)
    ss2 = pat.search(bbb)
    
    if(ss1 and ss2):
        aaaa = float(aaa[ss1.start(): ss1.end()])
        bbbb = float(bbb[ss2.start(): ss2.end()])
        #print aaa, bbb, aaaa, bbbb
        if aaaa == bbbb:
            return 0
        elif aaaa < bbbb:
            return -1
        elif aaaa > bbbb:
            return 1
        else:
            #print "crap"
            pass
    else:        
        if aaa == bbb:
            return 0
        elif aaa < bbb:
            return -1
        elif aaa > bbb:
            return 1
        else:
            #print "crap"
            pass
    
# ------------------------------------------------------------------------
# Show a regular message:

def message(strx, title = None, icon = gtk.MESSAGE_INFO):

    dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
        icon, gtk.BUTTONS_CLOSE, strx)
       
    if title:
        dialog.set_title(title)
    else:
        dialog.set_title("Dialog")

    # Close dialog on user response
    dialog.connect("response", lambda d, r: d.destroy())
    dialog.show()

# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        gtk.main_iteration_do(False)        



