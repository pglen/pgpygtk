#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, pango, math, traceback, subprocess
import gzip, zlib, zipfile, re

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")

import  publib.pubdisp, publib.pubhtml, publib.pubsql

from    publib.pubparse import NcxHTMLParser, OpfHTMLParser
from    publib.pubparse import HTML_Recurse, RootHTMLParser
from    publib.pubutil  import Config, print_exception, usleep, withps

# ------------------------------------------------------------------------
# Globals:

backlist = []    
conf = None

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
# Locate root meta data              

def locateroot():
    global gzf
    rootfile = ""    
    try:
        fh = gzf.open("META-INF/container.xml")
        ht = RootHTMLParser()
        while 1:
            sss = fh.readline()
            if sss == "": break
            ht.feed(sss)
            if conf.rootf:
                print sss,
        rootfile = ht.rootfile
    except:
        print_exception("No meta data")
    return rootfile 

def parse_opf(fname):
    global conf
    ret = ("", "")
    try:
        fh = zf.open(fname)
        ht = OpfHTMLParser(content2cb)
        conf.ht = ht
        while 1:
            sss = fh.readline()
            if sss == "": break
            if conf.header:
                print sss,
            ht.feed(sss)
            if conf.header:
                print sss,
            if not conf.nogui:
                mw.add_text(sss, True)
        ret = (ht.title, ht.auth)
    except:
        print_exception("Cannot parse .opf file")
    return ret
       
def parse_ncx(fname):
    global conf
    ret = "", ""
    try:
        fh = zf.open(fname)
        ht = NcxHTMLParser(contentcb)
        conf.ht = ht
        while 1:
            sss = fh.readline()
            if sss == "": break
            ht.feed(sss)
            if conf.header:
                print sss,
            if not conf.nogui:
                mw.add_text(sss, True)
        ret = ht.title, ht.auth
    except:
        print_exception("Cannot parse .ncx file")
    return ret
            
# ------------------------------------------------------------------------
# Read epub, save files in data_dir directory

def readepub(zf):

    global mw, conf
    
    names = [];  allnames = []
    
    if not conf.nogui:
        mw.waitcursor(True)
    
    if conf.extract:
        print "Extracting epub to:", conf.data_dir + "/" + conf.basefile + "/"
                
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
        
    found = False; ret1 = None; ret2 = None
    
    '''rootfile = locateroot()
    print "rootfile:", rootfile
    if rootfile != "":
        found = True
        if ".ncx" in rootfile:
            ret1 = parse_ncs(rootfile)
        if ".opf" in rootfile:
            ret2 = parse_opf(rootfile)'''
    
    # Hack: to simplify parsing we search for an .ncx and .opf file
    if not found: 
        for aa in allnames:
            if ".ncx" in aa:
                #print "Found toc", aa
                #found = True
                ret1 = parse_ncx(aa)
                break
            
    if not conf.nogui:
        mw.update_tree(" --------- ", "")

    # Fallback
    if not found: 
        for aa in allnames:
            if ".opf" in aa:
                #print "Found opf", aa
                found = True
                ret2 = parse_opf(aa)
                break
    
    # Pick from the two optional places    
    auth = ret1[0]; 
    try:
        if auth == "": auth = ret2[0]
    except: pass
    title = ret1[1];     
    try:   
        if title == "": title = ret2[1]
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
    
# ------------------------------------------------------------------------


def  openHTMLcb(fname, addback = True):
    global conf, gzf, backlist
    ret = False
    #print "openHTMLcb", fname
    conf.recurse = True
    usleep(1)
    try:
        if addback:
            backlist.append(fname)
        ret = openHTML(gzf, fname, False)
        if not mw.stopload:
            gobject.timeout_add(100, size_tick)
    except:
        print_exception("Cannot load HTML")
    conf.recurse = False
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
    conf.recurse = False
    # Is it a link with a tag?
    spl = fname.split("#")
    # Not loaded, load
    if mw.fname != spl[0]:
        mw.clearall(); found = False; fh = None
        usleep(1)
        try:           
            fh = zf.open(spl[0])
            found = True
        except:
            for aa in zf.infolist():
                if os.path.basename(aa.filename) == os.path.basename(spl[0]):
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
            ht = publib.pubhtml.HTML_Parser(conf)
            ht.mw = mw; ht.mark = mark; ht.fh = fh
            ht.getimagecb = getimagecb
            ln = 0
            mw.waitcursor(True)
            while 1:
                if conf.recurse:
                    break
                if mw.stopload:
                    break
                sss = fh.readline()
                if mw.stopload:
                    break
                if ln % 10 == 0:
                    mw.prog.set_text("Reading line: %d" % ln)
                    usleep(1)
                ln += 1
                if sss == "": break
                if conf.recurse:
                    break
                if ht.feed(sss):
                    break
                mw.add_text(sss, True)
            mw.fname = spl[0]
            
            mw.waitcursor(False)
            
        except:
            print_exception("Parsing HTML")
            
        #if  mw.stopload:
        #    return
            
        mw.prog.set_text("Done Loading.")
        usleep(1)
        
    if mw.stopload:
        return
        
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

def html_tick(fname):
    global conf, mw
     
    conf.recurse = False
    try:
        fh = open(fname)
        ht = publib.pubhtml.HTML_Parser(conf)
        ht.mw = mw; ht.fh = fh
        ht.getimagecb = getimagecb
        ln = 0
        
        mw.waitcursor(True)
        while 1:
            if conf.recurse:
                break
            sss = fh.readline()
            if ln % 10 == 0:
                mw.prog.set_text("Reading line: %d" % ln)
                usleep(1)
            ln += 1
            if sss == "": break
            if conf.recurse:
                break
            if ht.feed(sss):
                break
            mw.add_text(sss, True)
        mw.fname = fname
        mw.waitcursor(False)
    except:
        print_exception("Opening HTML")
    
    try:    
        mw.prog.set_text("Done Loading.")
        mw.hpaned.set_position(0)
        mw.gohome()
    except:
        print_exception("Positioning reader")
    

def reader_tick():
    global conf
    try:
        readepub(zf)
        if not conf.nogui:
            # Seen this ebook before?
            seb = mw.conf.sql.get(conf.basefile)
            if seb and seb != "":
                #print "opening remembered file", seb
                openHTMLcb(seb)
                # Seen this html before? Go to offset.
                comp = conf.basefile + "/" + seb
                offs = mw.conf.sql.get(comp)
                if offs != None:
                    #print "seen", mw.fname, offs
                    iter = mw.buffer_1.get_iter_at_offset(int(offs))
                    mw.buffer_1.place_cursor(iter)
                    mw.view.scroll_to_iter(iter, 0.2) #, True, 0, 0)
                # Load last selection
                comp = conf.basefile + "_sel"
                lsel = mw.conf.sql.get(comp)
                mw.sel_tree(lsel)
                #print "lastsel", comp, lsel
            else:
                #print "opening first link", conf.ht.firstlink
                openHTMLcb(conf.ht.firstlink)
            
            # Requested command line read    
            if conf.read:
                mw.read_tts(None)
    except:
        print_exception("Reader tick")            
        
def size_tick():
    #print "size_tick"
    try:
        mw.apply_size()
    except:
        print_exception("Size  tick")            
    
# ------------------------------------------------------------------------
# Main          

def main(zf, fname = None):

    global mw, conf
    
    if not conf.nogui:
        mw = publib.pubdisp.PubView(conf)
        mw.fname = ""; 
        mw.callback =  openHTMLcb; mw.bscallback = backcb
        
    if  conf.nogui:
        reader_tick()
    else:
        if zf:
            gobject.timeout_add(100, reader_tick)
        else:
            gobject.timeout_add(100, html_tick, fname)
    
    if not conf.nogui:
        try:
            gtk.main()
        except:
            print_exception("gtk_main")
            
    #print "gtk_main end"

def khelp():
    print
    print os.path.basename(sys.argv[0]), "keyboard shortcuts:"
    print
    print "   The Alt Key shortcuts are left hand approximate keys."
    print
    print "   F8       - Toggle adjust Pane (left-right) Enter to accept"
    print "   F6       - Switch to Left Side (contents) pane"
    print "   Shift F6 - Switch to Right Side (documents) pane"
    print "   F11      - Toggle Fullscreen --  F10      - Toggle Left Side Pane"
    print "   Esc      - Cancel Current operation"
    print "   Space    - Pager (next page)"
    print "   Space    - (At document end)  Next document"
    print "   Enter    - Follow link       --  Backspace    - Go back"
    print "   Home     - Start of document --  End          - End of document"
    print "   +        - Larger font       --  -            - Smaller font"
    print "   0        - Default font      --  Keypad *     - Default font"
    print "   PgUp     - Page Up           --  PgDn         - Page Down"
    print "   Up Arrow - Move line Up      --  Down Arrow   - Move line Up"
    print "   Alt-f    - Find text         --  Alt-x        - Exit program"
    print "   Alt-r    - Read from Cursor to end of Doc or  - Read Selection"
    print "   Alt-t    - Stop reading" 
    print "   Alt-h    - Goto the beginning of document (Home)"
    print "   Esc      - Stop reading      --  Esc          - Unfullscreen"
    
    print
    sys.exit(0)
    
# ------------------------------------------------------------------------

version = "1.12"

def phelp():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options] epubfilename"
    print
    print "Options:    -p    - Print E-Book filename."
    print "            -x    - Extract E-Book to ~/.pyepub/"
    print "            -t    - Print E-Book Author and Title."
    print "            -l    - List E-Book content's files."
    print "            -e    - Show E-Book Header file(s) (ncx,opf)"
    print "            -r    - Show E-Book root file (xml)"
    print "            -s    - Show saved configuration."
    print "            -c    - Clear saved configuration."
    print "            -a    - Read E-Book via Text to Speech."
    print "            -f    - Start fullscreen."
    print "            -n    - Do not start GUI (for title listing)"
    print "            -k    - Keystrokes Help."
    print "            -V    - Print version."
    print "            -q    - Quiet. Less messages."
    print "            -v    - Verbose. More messages."
    print "            -h    - Help (This screen)"
    print "            -d N  - Debug level N (to see parser internals)"
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

conf = Config(optarr); 

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
    
    global gzf

    conf.data_dir = os.path.expanduser("~/.pyepub")
    try:   os.mkdir(conf.data_dir)
    except: pass
    conf.sql = publib.pubsql.pubsql(conf.data_dir + "/data.sql")
    args = conf.comline(sys.argv[1:])

    if conf.verbose:
        last = conf.sql.get_int("lastrun")
        print "pyepub.py has run %d times" % last 
   
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
        print "Usage: pyepub.py [options] ebookfile"
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
        print "Cannot open EPUB file, trying as HTM, file was", "'" + args[0] + "'"
        zf = None

    gzf = zf
    main(zf, args[0])












