#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, pango, math, traceback, subprocess
import gzip, zlib, zipfile, re

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")

from HTMLParser import HTMLParser
import pubdisp

# Just line the system would print

isvalue = re.compile("([a-z]+)|([A-Z]+)|([0-9]+)")
ischapter = re.compile("chapter", re.IGNORECASE)

def put_exception(xstr):

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


class MyHTMLParser(HTMLParser):

    def __init__(self):
    
        HTMLParser.__init__(self)
        self.mark = True
        self.para = "";  self.txt = "";    self.head = ""; self.ita = ""
        self.in_p = 0;   self.in_h = 0;    self.in_i = 0
        self.id_p = 0;   self.id_h = 0;    self.id_i = 0
                    
    def handle_starttag(self, tag, attrs):

        #print " -- Begin '%s' tag '%s'" % (tag, attrs)
        
        if tag == "p":
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_p = 1
            for aa in attrs:
                if aa[0] == "id": 
                    self.id_p = aa[1]
        
        elif tag[0] == "h":
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_h = tag
            for aa in attrs:
                if aa[0] == "id": 
                    self.id_h = aa[1]
        
        elif tag[0] == "i":
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_i = tag
        else:
            #print " -- Begin %s tag %s" % (tag, attrs)
            pass
                        
    def handle_endtag(self, tag):
        global isvalue, ischapter
        
        #print " -- End '%s' tag" % tag
        
        if tag == "p":
            self.in_p = 0
            #print para; print
            #print "id_p", id_p
            para2 = self.para.replace("\n", " ")
            if isvalue.search(para2):
                nnn = None;
                if self.id_p: nnn = str(self.id_p)
                #print "tagname:", nnn
                
                xtag = gtk.TextTag(nnn)
                xtag.set_property("wrap_mode", gtk.WRAP_WORD)
                xtag.set_property("justification", gtk.JUSTIFY_FILL)
                
                #if para2.find("Chapter ") != -1:
                if ischapter.match(para2):
                    #print para2
                    if self.mark:
                        mw.update_tree(para2, para2)
                #if(nnn):
                #    mw.add_text_mark(nnn)
                    
                mw.add_text_xtag(para2 + "\n\n", xtag, False)
            self.para = ""
            self.id_p = 0
            #print "endtag %s" % tag
        elif tag[0] == "h":
            self.in_h = 0
            #print "head" + "'" + head + "'"; print
            nnn = None;
            if self.id_h: nnn = str(self.id_h)
            #print "head tagname:", nnn
            para2 = self.head.replace("\n", " ")
            if isvalue.search(para2):
                if nnn:
                    if self.mark:
                        mw.update_tree(para2, nnn)
                    mw.add_text_mark(nnn)
                    
                #elif ischapter.search(para2):   
                #    mw.update_tree(para2, para2)
                #    mw.add_text_mark(para2)
                    
                xtag = gtk.TextTag(nnn)
                xtag.set_property("weight", pango.WEIGHT_BOLD)
                mw.add_text_xtag(para2 + "\n\n", xtag, False)
                
            self.head = ""
            #print "endtag %s" % tag
        elif tag[0] == "i":
            self.in_i = 0
            #print "ita" + "'" + ita + "'"; print
            para2 = self.ita.replace("\n", " ")
            if para2 != "":
                xtag = gtk.TextTag()
                xtag.set_property("style", pango.STYLE_ITALIC)
                #xtag.set_property("wrap_mode", gtk.WRAP_WORD)
                #xtag.set_property("justification", gtk.JUSTIFY_FILL)
                mw.add_text_xtag(para2, xtag, False)
            self.ita = ""
            #print "endtag %s" % tag
        else:
            pass
            #print "endtag %s" % tag
            #print txt; print
            #mw.add_text("text" + txt + "\n")
            #txt = ""
            
    def handle_data(self, data):
        #print " -- data '%s'" % data
        if self.in_p:
            self.para +=  data
        elif self.in_h:
            self.head +=  data
        elif self.in_i:
            self.ita +=  data
        else:
            #print " -- data", data
            self.txt += data

# ------------------------------------------------------------------------

class TocHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.txt = ""
        self.curtag = ""
        self.label = ""
        self.currattr = None
        self.auth = ""
        self.title = ""
            
    def handle_starttag(self, tag, attrs):
        if tag != "text":
            #print " -- Begin '%s' tag '%s'" % (tag, attrs)
            self.currtag = tag.lower()
            self.currattr = attrs
                        
    def handle_endtag(self, tag):
        
        erase = True
        para2 = self.txt.replace("\n", " ")
        para2 = para2.strip()
        
        if tag != "text":
            pass
            #print " -- End '%s' tag - text '%s'" % (tag, para2)
            
        if self.currtag == "doctitle":
            #print "TITLE",  "'" + para2 + "'"
            self.title = para2
            old = mw.get_title()
            mw.set_title(old + " '" + self.title + "' ")
        
        if self.currtag == "docauthor":
            #print "AUTHOR", "'" + para2 + "'"
            self.auth = para2
            old = mw.get_title()
            mw.set_title(old + " '" + self.auth + "' ")
        
        if self.currtag == "navlabel":
            self.label = para2
            
        if self.currtag == "content":
            #print "Found", self.label, " -- ", self.currattr[0][1] 
            mw.update_tree(self.label, self.currattr[0][1])
        
        if self.currtag == "text":
            erase = False
            
        self.currtag = ""
        if erase:
            self.txt = ""
            
    def handle_data(self, data):
        self.txt += data

class PlotConfig():
    full_screen = False
    pass

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
# Read epub, save files in data dir

def readepub(zf):
    global mw, basefile
    
    names = [];  allnames = []
    
    for aa in zf.infolist():
        #print aa.filename, aa.file_size 
        # Extract    
        try:
            dd = "data/" + basefile + "/" + os.path.split(aa.filename)[0]
            if not os.path.isdir(dd):
                os.makedirs(dd)
            fh  = zf.open(aa.filename)
            fff = dd + "/" + os.path.basename(aa.filename)
            fh2 = open(fff, "w+")
            while 1:
                sss = fh.readline() 
                if sss == "": break
                fh2.write(sss)
            fh2.close()
        except:
            put_exception("Cannot extract")
            #print "Cannot extract", aa.filename, sys.exc_info()
        
        if os.path.splitext(aa.filename)[1].find("htm") >= 0:
            names.append(aa.filename)
            
        allnames.append(aa.filename)
            
    names.sort(cmp)
    #print names  
    
    found = False
    for aa in allnames:
        if "toc" in aa:
            #print "Found toc", aa
            found = True
            fh = zf.open(aa)
            ht = TocHTMLParser()
            while 1:
                sss = fh.readline()
                if sss == "": break
                ht.feed(sss)
                mw.add_text(sss, True)
        
    # No TOC Open and parse all the files
    if not found:        
        #nnn = "000";  mw.update_tree("Start", nnn); mw.add_text_mark(nnn)
        for bbb in names:    
            openHTML(zf, bbb)
        #nnn = "999";  mw.update_tree("End", nnn);   mw.add_text_mark(nnn)

# ------------------------------------------------------------------------
def  openHTML2(fname):
    global gzf
    openHTML(gzf, fname, False)

# ------------------------------------------------------------------------
def  openHTML(zf, fname, mark = True):

    # Is it a tagged link?
    ppp = fname.find("#")
    spl = []
    if spl >= 0:
        spl = fname.split("#")
        print "tagged", spl
        fname = spl[0]
        
    if mw.fname == fname:
        print "Loaded already"
    else:
        mw.clear(); mw.clear(True)
        try:           
            fh = zf.open(fname)
        except:
            #print "searching for", fname
            # Search for it ...
            for aa in zf.infolist():
                if os.path.basename(aa.filename) == fname:
                    try:
                        fh = zf.open(aa.filename)
                    except:
                        put_exception("No Zip File")
                        return
            
        ht = MyHTMLParser()
        ht.mark = mark
        mw.waitcursor(True)
        while 1:
            sss = fh.readline()
            if sss == "": break
            ht.feed(sss)
            mw.add_text(sss, True)
        mw.fname = fname
        mw.waitcursor(False)
    
    # Jump to tag, if any
    if len(spl) > 1:
        #print "Jumping to", "'" + spl[1] + "'"
        mm = mw.buffer_1.get_mark(spl[1])
        if mm:
            mw.view.scroll_to_mark(mm, 0.0, True, 0, 0)
    
# ------------------------------------------------------------------------
# Main          

def main(zf):
    global mw
    mw = pubdisp.PubView(PlotConfig)
    mw.fname = ""; mw.loader = openHTML2
    
    readepub(zf)
    
    #mw.gohome()
    gtk.main()

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
    
    global basefile, data_dir, gzf
    
    if len(sys.argv) < 2:
        print "Usage: pyepub.py ebookfile"
        sys.exit(1)
        
    basefile = os.path.basename(sys.argv[1])
    basefile = os.path.splitext(basefile)[0]
    basefile = basefile.translate(string.maketrans(" {}()", "_____"))
    
    #print basefile
    #sys.exit(0)
    data_dir = os.path.expanduser("~/.pyepub")
    #print "data_dir", data_dir
    
    try:   os.mkdir("data")
    except: pass
        
    try:   os.mkdir(data_dir)
    except: pass
    
    try:
        zf = zipfile.ZipFile(sys.argv[1])
    except:
        #print sys.exc_info()
        put_exception("Cannot open zipfile")

    gzf = zf
    main(zf)


