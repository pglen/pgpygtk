#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, pango, math, traceback, subprocess
import gzip, zlib, zipfile, re

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")

import  pubdisp, pubhtml

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
    print "Image callback", "'" + fname + "'"
    
    fh = None
    try:
        fh = gzf.open(fname)
    except:
        #sys.exc_info()
        #print "searching for", "'" + fname + "'"
        # Search for it ...
        for aa in zf.infolist():
            #print "search", aa.filename, fname
            if os.path.basename(aa.filename) == fname:
                #print "found:", "'" + aa.filename + "'"
                try:
                    fh = gzf.open(aa.filename)
                except:
                    print_exception("No image File")
                    return
                break
                
    # Extract image file
    fname2 = conf.data_dir + "/" + fname
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

    global mw, basefile, ht, conf
    
    names = [];  allnames = []
    
    if not conf.nogui:
        mw.waitcursor(True)
    
    if conf.extract:
        print "Extracting epub to:", conf.data_dir + "/" + basefile + "/"
                
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
                dd = conf.data_dir + "/" + basefile + "/" + os.path.split(aa.filename)[0]
                if not os.path.isdir(dd):
                    os.makedirs(dd)
                fh  = zf.open(aa.filename)
                fff = dd + "/" + os.path.basename(aa.filename)
                
                # Only extract once:
                if not os.path.isfile(fff):
                    if not conf.nogui:
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
        
    found = False
    ht = None;   ht2 = None
    for aa in allnames:
        if "toc.ncx" in aa:
            #print "Found toc", aa
            found = True
            fh = zf.open(aa)
            ht = TocHTMLParser(contentcb)
            while 1:
                sss = fh.readline()
                if sss == "": break
                ht.feed(sss)
                if conf.header:
                    print sss,
                if not conf.nogui:
                    mw.add_text(sss, True)
            break
        
    if 1: #not found:        
        for aa in allnames:
            if "content.opf" in aa:
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

    global conf
    # Is it a tagged link?
    ppp = fname.find("#")
    spl = []
    if spl >= 0:
        spl = fname.split("#")
        fname = spl[0]
        
    # Not loaded, load
    if mw.fname != fname:
        #print "loading", fname
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
            mw.fname = fname
            mw.waitcursor(False)
        except:
            print_exception("Parsing HTML")
        mw.prog.set_text("Done Reading.")
        usleep(10)
          
    # Jump to tag, if any
    if len(spl) > 1:
        #print "Jumping to", "'" + spl[1] + "'"
        mm = mw.buffer_1.get_mark(spl[1])
        ii = mw.buffer_1.get_iter_at_mark(mm)
        if mm:
            mw.view.scroll_to_mark(mm, 0.0, True, 0, 0)
    else:
        mw.gohome()
    return True  
  
# ------------------------------------------------------------------------

def reader_tick():
    global conf
    readepub(zf)
    if not conf.nogui:
        openHTML2(ht.firstlink)
    
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
        mw.fname = ""; mw.loader = openHTML2;
        mw.callback =  openHTML2
        
    if  conf.nogui:
        reader_tick()
        
    else:
        gobject.timeout_add(100, reader_tick)
    
    if not conf.nogui:
        gtk.main()

version = 1.0

# ------------------------------------------------------------------------

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
    print "            -e        - Show Ebook Header file (ncx,opf)"
    print "            -r        - Show Ebook root file (xml)"
    print "            -n        - Nogui, Do not start GUI"
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
    
    if conf.prname:
        print args[0]
    try:
        conf.fname = args[0]
        zf = zipfile.ZipFile(args[0])
    except:
        zf = None
        print_exception("Cannot open zipfile")
        #return

    gzf = zf
    main(zf)

