#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, pango, math, traceback, subprocess
import gzip, zlib, zipfile, re

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")

import  pubdisp, pubhtml, epubsql

from    pubparse import TocHTMLParser, ConHTMLParser, HTML_Recurse
from    pubutil import Config, print_exception, usleep, withps

# ------------------------------------------------------------------------
# Callbacks from the parser

def contentcb(label, attr):

    global mw, conf
    if not conf.nogui:
        mw.update_tree(label, attr)

def content2cb(label, attr):

    global mw, conf
    if not conf.nogui:
        mw.update_tree(label, attr)
    #print label, attr

def getimagecb(fname):

    global gzf, conf
    fullname  = ""
    #print "Image callback", "'" + fname + "'"
    fh = None
    try:
        fh = gzf.open(fname)
        fullname = fname
    except:
        # Search for it ...
        for aa in zf.infolist():
            if os.path.basename(aa.filename) == fname:
                fullname = aa.filename
                try:
                    fh = gzf.open(aa.filename)
                except:
                    print_exception("No image File")
                    return
                break
                
    # Extract image file
    dd = conf.data_dir + "/" + conf.basefile + "/" + os.path.split(fullname)[0]
    if not os.path.isdir(dd):
        os.makedirs(dd)
    fname2 = dd + "/" + os.path.basename(fullname)
    if not os.path.isfile(fname2):
        try:
            fh2 = open(fname2, "w")
            while True:
                buff = fh.read()
                if len(buff) == 0: break
                fh2.write(buff)
            fh.close(); fh2.close()      
        except:
            print_exception("Cannot load image", fname)
            return   
            
    pixbuf = gtk.gdk.pixbuf_new_from_file(fname2)
    return pixbuf

# ------------------------------------------------------------------------
# Read epub, save files in data_dir directory

def readepub(zf):

    global mw, conf
    
    names = [];  allnames = []
    
    if not conf.nogui:
        mw.waitcursor(True)
    
    if conf.extract:
        print "Extracting epub to:", conf.data_dir + "/" + conf.basefile + "/"
                
    # Locate root meta data              
    try:
        md = zf.open("META-INF/container.xml")
        if conf.rootf:
            print md.read()
    except:
        print "No meta data, guessing";
                
    for aa in zf.infolist():
        if conf.list:
            print aa.filename, aa.file_size
        # Extract    
        if conf.extract:
            try:
                dd = conf.data_dir + "/" + conf.basefile + "/" + os.path.split(aa.filename)[0]
                if not os.path.isdir(dd):
                    os.makedirs(dd)
                fh  = zf.open(aa.filename)
                fff = dd + "/" + os.path.basename(aa.filename)
                
                # Only extract once:
                if not os.path.isfile(fff):
                    if not conf.nogui:
                        tt = "Extracting '" + aa.filename + "'"
                        mw.prog.set_text(tt[-18])
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
        
    found = False
    ht = None;   ht2 = None
    for aa in allnames:
        if "toc.ncx" in aa:
            #print "Found toc", aa
            found = True
            fh = zf.open(aa)
            ht = TocHTMLParser(contentcb)
            conf.ht = ht
            while 1:
                sss = fh.readline()
                if sss == "": break
                ht.feed(sss)
                if conf.header:
                    print sss,
                if not conf.nogui:
                    mw.add_text(sss, True)
            break
        
    if 1: 
        for aa in allnames:
            if "content.opf" in aa:
                if not conf.nogui:
                    mw.update_tree("Legacy Entries:", [])
                #print "Found content", aa
                found = True
                fh = zf.open(aa)
                ht2 = ConHTMLParser(content2cb)
                while 1:
                    sss = fh.readline()
                    if sss == "": break
                    if conf.header:
                        print sss,
                    ht2.feed(sss)
                    if conf.header:
                        print sss,
                    if not conf.nogui:
                        mw.add_text(sss, True)
                break
        
    auth = ""; title = ""
    try: auth = ht.auth
    except: pass
    try:
        if auth == "": auth = ht2.auth
    except: pass
    try: title = ht.title
    except: pass
    try:
        if title == "": title = ht2.title
    except: pass
        
    if conf.title:
        print "'" + auth + "'  '" + title + "'"
                
    if not conf.nogui:
        old = mw.get_title()
        mw.set_title(old + " '" + auth + "'  '" + title + "'")
    
    if conf.nogui:
        return
   
    # No TOC Open and parse all the [x]htm[l] files
    if not found:        
        nnn = "000";  mw.update_tree("Start of Book", nnn); mw.add_text_mark(nnn)
        for bbb in names:    
            openHTML(zf, bbb)
        nnn = "999";  mw.update_tree("End", nnn);   mw.add_text_mark(nnn)

    mw.waitcursor(False)
    return ht
    
# ------------------------------------------------------------------------

backlist = []    

def  openHTMLcb(fname, addback = True):
    global gzf, backlist
    ret = False
    #print "openHTMLcb", fname
    try:
        if addback:
            backlist.append(fname)
        ret = openHTML(gzf, fname, False)
        gobject.timeout_add(100, size_tick)
    except:
        print_exception("Cannot load HTML")
    return ret
    
def backcb():
    global gzf, backlist
    ret = False
    if len(backlist) < 2:
        return ret
    backlist = backlist[:len(backlist)-1]
    fname = backlist[len(backlist)-1]
    ret = openHTMLcb(fname, False)
    return ret    
                    
# ------------------------------------------------------------------------
def  openHTML(zf, fname, mark = True):

    global conf
    found = False; fh = None; spl = []; ht = None
    
    # Is it a link with a tag?
    #ppp = fname.find("#")
    spl = fname.split("#")
          
    # Not loaded, load
    if mw.fname != spl[0]:
        mw.clear(); mw.clear(True); found = False; fh = None
        usleep(1)
        try:           
            fh = zf.open(spl[0])
            found = True
        except:
            #print "searching for", fname
            # Search for it ...
            for aa in zf.infolist():
                #print aa.filename, sp[0]
                if os.path.basename(aa.filename) == spl[0]:
                    #print "found", aa.filename
                    try:
                        fh = zf.open(aa.filename)
                    except:
                        print_exception("No Zip File")
                        return
                    found = True
                    break
        if not found: return False
        try:
            ht = pubhtml.HTML_Parser(conf)
            ht.mw = mw; ht.mark = mark; ht.fh = fh
            ht.getimagecb = getimagecb
            ln = 0
            
            mw.waitcursor(True)
            while 1:
                sss = fh.readline()
                if ln % 10 == 0:
                    mw.prog.set_text("Reading line: %d" % ln)
                    usleep(1)
                ln += 1
                if sss == "": break
                if ht.feed(sss):
                    break
                mw.add_text(sss, True)
            mw.fname = spl[0]
            mw.waitcursor(False)
        except:
            print_exception("Parsing HTML")
        mw.prog.set_text("Done Loading.")
        usleep(10)
          
    # Jump to tag, if any
    if len(spl) > 1:
        #print "Jumping to", "'" + spl[1] + "'"
        mm = mw.buffer_1.get_mark(spl[1])
        if mm:
            ii = mw.buffer_1.get_iter_at_mark(mm)
            mw.buffer_1.place_cursor(ii)
            mw.view.scroll_to_mark(mm, 0.0, True, 0, 0)
    else:
        mw.gohome()
        
    return True  
  
# ------------------------------------------------------------------------

def reader_tick():
    global conf

    readepub(zf)
     # Seen this ebook before?
    if not conf.nogui:
        seb = mw.conf.sql.get(conf.basefile)
        sebini = mw.conf.sql.get(conf.basefile + "_init")
        #print "sebinii", sebini 
        if sebini and sebini != "":
            print "opening remembered link", conf.ht.firstlink
            openHTMLcb(sebini)
            mw.sel_item(seb)
        else:
            print "opening first link", conf.ht.firstlink
            openHTMLcb(conf.ht.firstlink)
    
        # Seen this html before?
        offs = mw.conf.sql.get_int(mw.fname)
        if offs:
            print "seen", mw.fname, offs
            iter = mw.buffer_1.get_iter_at_offset(offs)
            mw.buffer_1.place_cursor(iter)
            mw.view.scroll_to_iter(iter, 0.2) #, True, 0, 0)
       
        if conf.read:
            mw.read_tts(None)
        
def size_tick():
    pass
    mw.apply_size()
    #mw.prog.set_text(mw.fname[-18:])
    
# ------------------------------------------------------------------------
# Main          

def main(zf):

    global mw, conf
    
    if not conf.nogui:
        mw = pubdisp.PubView(conf)
        mw.fname = ""; 
        mw.callback =  openHTMLcb; mw.bscallback = backcb
        
    if  conf.nogui:
        reader_tick()
        
    else:
        gobject.timeout_add(100, reader_tick)
    
    if not conf.nogui:
        gtk.main()

def khelp():
    print
    print os.path.basename(sys.argv[0]), "keyboard shortcuts:"
    print
    print "The Alt Key shortcuts are left hand approximate keys."
    print "F11      - Toggle Fullscreen"
    print "F10      - Toggle Left Side Pane"
    print "F8       - Toggle adjust Pane (left-right) Enter to accept"
    print "F6       - Switch to Left Side (contents) pane"
    print "Shift F6 - Switch to Right Side (documents) pane"
    print "Esc      - Cancel Current operation"
    print "Esc      - Stop reading      --  Esc          - Unfullscreen"
    print "Enter    - Follow link       --  Backspace    - Go back"
    print "Home     - Start of document --  End          - End of document"
    print "PgUp     - Page Up           --  PgDn         - Page Down"
    print "Up Arrow - Move line Up      --  Down Arrow   - Move line Up"
    print "Alt-f    - Find text         --  Alt-x        - Exit program"
    print "Alt-r    - Read from Cursor to end of Doc or  - Read Selection"
    print "Alt-t    - Stop reading" 
    print "Alt-h    - Goto the beginning of document (Home)"
    
    print
    sys.exit(0)
    
# ------------------------------------------------------------------------

version = 1.0

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options] epubfilename"
    print
    print "Options:    -p        - Print Ebook filename"
    print "            -v        - Verbose. More messages"
    print "            -q        - Quiet. Less Messages"
    print "            -x        - Extract Ebook to ~/.pyepub/"
    print "            -t        - Print Ebook author and title"
    print "            -l        - List Ebook content filenames"
    print "            -e        - Show Ebook Header file(s) (ncx,opf)"
    print "            -r        - Show Ebook root file (xml)"
    print "            -s        - Show saved Configuration"
    print "            -a        - Read Ebook via Text to Speech"
    print "            -n        - Nogui, Do not start GUI"
    print "            -k        - Keystrokes Help"
    print "            -h        - Help"
    print
    sys.exit(0)

def pversion():
    print os.path.basename(sys.argv[0]), "Version", version
    sys.exit(0)
 
    # option, var_name, initial_val, function
optarr = \
    ["d:",  "debug",        0,      None],      \
    ["p",   "prname",       0,      None],      \
    ["v",   "verbose",      0,      None],      \
    ["q",   "quiet",        0,      None],      \
    ["x",   "extract",      0,      None],      \
    ["l",   "list",         0,      None],      \
    ["e",   "header",       0,      None],      \
    ["f",   "fullscreen",   0,      None],      \
    ["n",   "nogui",        0,      None],      \
    ["t",   "title",        0,      None],      \
    ["r",   "rootf",        0,      None],      \
    ["s",   "showconf",     0,      None],      \
    ["c",   "cconf",        0,      None],      \
    ["a",   "read",         0,      None],      \
    ["V",   None,           None,   pversion],  \
    ["h",   None,           None,   phelp],     \
    ["k",   None,           None,   khelp]      \

conf = Config(optarr)

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
    
    global gzf

    conf.data_dir = os.path.expanduser("~/.pyepub")
    try:   os.mkdir(conf.data_dir)
    except: pass
    conf.sql = epubsql.epubsql(conf.data_dir + "/data.sql")
    args = conf.comline(sys.argv[1:])
   
    # To show all config vars
    if conf.showconf:    
        if conf.verbose:
            print "Dumping configuration:"
        ss = conf.sql.getall(); 
        for aa in ss: 
            print aa
        sys.exit(0)
    # Clear all config vars
    if conf.cconf:    
        print "Are you sure you want to clear config ? (y/n)"
        aa = sys.stdin.readline()
        if aa[0] == "y":
            print "Removing pyepub configuration ... ",
            conf.sql.rmall()        
            print "OK"
        sys.exit(0)
        
    if len(args) < 1:
        print "Usage: pyepub.py ebookfile"
        sys.exit(1)
        
    basefile = os.path.basename(args[0])
    basefile = os.path.splitext(basefile)[0]
    conf.basefile = basefile.translate(string.maketrans(" {}()", "_____"))
        
    # Requested file name print 
    if conf.prname:
        print args[0]
        
    if not os.path.isfile(args[0]):
        print "File:", "'" + args[0] + "'", "does not exist."
        sys.exit(1)
        
    # Open archive
    try:
        conf.fname = args[0]
        zf = zipfile.ZipFile(args[0])
    except:
        zf = None
        print "Cannot open EPUB file", "'" + args[0] + "'"
        if conf.verbose:
            print_exception("Cannot open zipfile")
        sys.exit(1)

    gzf = zf
    main(zf)

