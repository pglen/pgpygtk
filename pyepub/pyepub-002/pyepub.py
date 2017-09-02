#!/usr/bin/env python

import os, sys, glob, getopt, time, string, signal, stat, shutil
import gobject, pango, math, traceback, subprocess
import gzip, zlib, zipfile

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")

from HTMLParser import HTMLParser

import pubdisp

para = "";  txt = "";    head = ""; ita = ""
in_p = 0;   in_h = 0;    in_i = 0
id_p = 0;   id_h = 0;    id_i = 0

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
            
    def handle_starttag(self, tag, attrs):
        global in_p, in_h, in_i
        global id_p, id_h, id_i
        
        if tag == "p":
            #print " -- Begin %s tag %s" % (tag, attrs)
            in_p = 1
            for aa in attrs:
                if aa[0] == "id": 
                    id_p = aa[1]
        
        elif tag[0] == "h":
            #print " -- Begin %s tag %s" % (tag, attrs)
            in_h = tag
            for aa in attrs:
                if aa[0] == "id": 
                    id_h = aa[1]
        
        elif tag[0] == "i":
            #print " -- Begin %s tag %s" % (tag, attrs)
            in_i = tag
        else:
            #print " -- Begin %s tag %s" % (tag, attrs)
            pass
                        
    def handle_endtag(self, tag):
        global in_p, id_p, para, txt, mw, in_h, id_h, head, in_i, ita
        #print " -- End %s tag" % tag
        if tag == "p":
            in_p = 0
            #print para; print
            #print "id_p", id_p
            para2 = para.replace("\n", " ")
            nnn = None;
            #if id_p: nnn = str(id_p)
            #print "tagname:", nnn
            xtag = gtk.TextTag(nnn)
            xtag.set_property("wrap_mode", gtk.WRAP_WORD)
            xtag.set_property("justification", gtk.JUSTIFY_FILL)
            mw.add_text_xtag(para2 + "\n\n", xtag, False)
            para = ""
            #print "endtag %s" % tag
        elif tag[0] == "h":
            in_h = 0
            #print "head" + "'" + head + "'"; print
            #print "id_h", id_h
            nnn = None;
            if id_h: nnn = "head_" + str(id_h)
            #print "head tagname:", nnn
            para2 = head.replace("\n", " ")
            if para2 != "":
                if nnn:
                    mw.update_tree(para2, nnn)
                xtag = gtk.TextTag(nnn)
                xtag.set_property("weight", pango.WEIGHT_BOLD)
                if nnn:
                    mw.add_text_mark(nnn)
                mw.add_text_xtag(para2 + "\n\n", xtag, False)
                
            head = ""
            #print "endtag %s" % tag
        elif tag[0] == "i":
            in_i = 0
            #print "ita" + "'" + ita + "'"; print
            para2 = ita.replace("\n", " ")
            if para2 != "":
                xtag = gtk.TextTag()
                xtag.set_property("style", pango.STYLE_ITALIC)
                #xtag.set_property("wrap_mode", gtk.WRAP_WORD)
                #xtag.set_property("justification", gtk.JUSTIFY_FILL)
                mw.add_text_xtag(para2, xtag, False)
            ita = ""
            #print "endtag %s" % tag
        else:
            pass
            #print "endtag %s" % tag
            #print txt; print
            #mw.add_text("text" + txt + "\n")
            #txt = ""
            
    def handle_data(self, data):
        global in_p, para, txt, in_h, head, in_i, ita
        #print " -- data '%s'" % data
        if in_p:
            para +=  data
        elif in_h:
            head +=  data
        elif in_i:
            ita +=  data
        else:
            #print " -- data", data
            txt += data

    def handle_comment(self, data):
        pass
        #print "Comment '%s'" % data

    def handle_decl(self, data):
        pass
        #print "Decl '%s'" % data

    def handle_charref(name):
        pass
        #print "Encountered charref '%s'" % name

    def handle_entityref(name):
        pass
        #print "Encountered entityref '%s'" % name

    def unknown_decl(data):
        pass
        print "Encountered unkown decl '%s'" % data

    def handle_pi(self, data):
        pass
        #print "Encountered pi '%s'" % data

class PlotConfig():
    full_screen = False
    pass

def readepub(zf):
    global mw
    for aa in zf.infolist():
        #print aa.filename, aa.file_size 
        if os.path.splitext(aa.filename)[1] == ".html":
            #print "html file:", aa.filename
            fh = zf.open(aa.filename)
            ht = MyHTMLParser()
            while 1:
                sss = fh.readline()
                if sss == "": break
                ht.feed(sss)
                mw.add_text(sss, True)
            
# ------------------------------------------------------------------------
# Main          

def main(zf):
    global mw
    mw = pubdisp.PubView(PlotConfig)
    #mw.clear_tree()
    
    nnn = "000";  mw.update_tree("Start", nnn); mw.add_text_mark(nnn)
    readepub(zf)
    nnn = "999";  mw.update_tree("End", nnn);   mw.add_text_mark(nnn)
    
    mw.gohome()
    gtk.main()

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print "Usage: pyepub.py ebookfile"
        sys.exit(1)
        
    zf = zipfile.ZipFile(sys.argv[1])
    
    #print zf.infolist()  #print zf.namelist()
    #for aa in zf.infolist():
    #    print "File name:", "'" + aa.filename + "'", "File size:", aa.file_size 
    
    main(zf)




