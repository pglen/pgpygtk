#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, pango, math, traceback, subprocess
import gzip, zlib, zipfile, re

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")

import  pubdisp, pubhtml

from    pubparse import TocHTMLParser, HTML_Recurse
from    pubutil import Config, print_exception, usleep, withps

# ------------------------------------------------------------------------
# Read epub, save files in data_dir directory

def readepub(zf):
    global mw, basefile, ht, conf
    
    names = [];  allnames = []
    
    mw.waitcursor(True)
    for aa in zf.infolist():
        #print aa.filename, aa.file_size, 
        # Extract    
        if conf.extract:
            try:
                dd = conf.data_dir + "/" + basefile + "/" + os.path.split(aa.filename)[0]
                if not os.path.isdir(dd):
                    os.makedirs(dd)
                fh  = zf.open(aa.filename)
                fff = dd + "/" + os.path.basename(aa.filename)
                
                # Only extract once:
                if not os.path.isfile(fff):
                    mw.prog.set_text("Extracting '" + aa.filename + "'")
                    usleep(1)
                    fh2 = open(fff, "w+")
                    while 1:
                        sss = fh.readline() 
                        if sss == "": break
                        fh2.write(sss)
                    fh2.close()
            except:
                print_exception("Cannot extract file")
                
        if os.path.splitext(aa.filename)[1].find("htm") >= 0:
            names.append(aa.filename)
        allnames.append(aa.filename)
            
    #print
    #names.sort(cmp)
    #print names  
    
    found = False
    for aa in allnames:
        if "toc.ncx" in aa:
            #print "Found toc", aa
            found = True
            fh = zf.open(aa)
            ht = TocHTMLParser(mw)
            while 1:
                sss = fh.readline()
                if sss == "": break
                ht.feed(sss)
                mw.add_text(sss, True)
            break
        
    # No TOC Open and parse all the [x]htm[l] files
    if not found:        
        nnn = "000";  mw.update_tree("Start", nnn); mw.add_text_mark(nnn)
        for bbb in names:    
            openHTML(zf, bbb)
        nnn = "999";  mw.update_tree("End", nnn);   mw.add_text_mark(nnn)

    mw.waitcursor(False)

# ------------------------------------------------------------------------
def  openHTML2(fname):

    global gzf
    ret = False
    #print "openHTML2", fname
    try:
        ret = openHTML(gzf, fname, False)
        gobject.timeout_add(100, size_tick)
    except:
        pass
    return ret
    
# ------------------------------------------------------------------------
def  openHTML(zf, fname, mark = True):

    # Is it a tagged link?
    ppp = fname.find("#")
    spl = []
    if spl >= 0:
        spl = fname.split("#")
        fname = spl[0]
        
    # Not loaded, load
    if mw.fname != fname:
        mw.clear(); mw.clear(True); found = False; fh = None
        try:           
            fh = zf.open(fname)
            found = True
        except:
            #print "searching for", fname, sys.exc_info()
            # Search for it ...
            for aa in zf.infolist():
                #print aa.filename, fname
                if os.path.basename(aa.filename) == fname:
                    try:
                        fh = zf.open(aa.filename)
                    except:
                        print_exception("No Zip File")
                        return
                    found = True
                    break
                    
        if not found: return False
            
        try:
            #ht = MyHTMLParser(mw)
            ht = pubhtml.HTML_Parser()
            ht.mw = mw; ht.mark = mark; ht.fh = fh
            
            mw.waitcursor(True)
            while 1:
                sss = fh.readline()
                if sss == "": break
                if ht.feed(sss):
                    break
                mw.add_text(sss, True)
            mw.fname = fname
            mw.waitcursor(False)
        except:
            print_exception("Parsing HTML")
        
    # Jump to tag, if any
    if len(spl) > 1:
        #print "Jumping to", "'" + spl[1] + "'"
        mm = mw.buffer_1.get_mark(spl[1])
        if mm:
            mw.view.scroll_to_mark(mm, 0.0, True, 0, 0)
    return True  
  
# ------------------------------------------------------------------------

def reader_tick():
    readepub(zf)
    openHTML2(ht.firstlink)
    mw.gohome()

def size_tick():
    mw.apply_size()
    mw.prog.set_text(mw.fname)
    
# ------------------------------------------------------------------------
# Main          

def main(zf):
    global mw, conf
    
    mw = pubdisp.PubView(conf)
    mw.fname = ""; mw.loader = openHTML2;
    mw.callback =  openHTML2
    gobject.timeout_add(100, reader_tick)
    
    gtk.main()

version = 1.0

# ------------------------------------------------------------------------

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -p        - Port to use (default: 9999)"
    print "            -v        - Verbose"
    print "            -q        - Quiet"
    print "            -h        - Help"
    print
    sys.exit(0)

def pversion():
    print os.path.basename(sys.argv[0]), "Version", version
    sys.exit(0)
 
    # option, var_name, initial_val, function
optarr = \
    ["d:",  "debug",        0,      None],      \
    ["v",   "verbose",      0,      None],      \
    ["q",   "quiet",        0,      None],      \
    ["x",   "extract",      0,      None],      \
    ["f",   "fullscreen",   0,      None],      \
    ["V",   None,           None,   pversion],  \
    ["h",   None,           None,   phelp]      \

conf = Config(optarr)

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
    
    global basefile, gzf

    args = conf.comline(sys.argv[1:])
   
    if len(args) < 1:
        print "Usage: pyepub.py ebookfile"
        sys.exit(1)
        
    basefile = os.path.basename(args[0])
    basefile = os.path.splitext(basefile)[0]
    basefile = basefile.translate(string.maketrans(" {}()", "_____"))
    
    conf.data_dir = os.path.expanduser("~/.pyepub")
    try:   os.mkdir(conf.data_dir)
    except: pass
    
    try:
        conf.fname = args[0]
        zf = zipfile.ZipFile(args[0])
    except:
        zf = None
        print_exception("Cannot open zipfile")

    gzf = zf
    main(zf)







