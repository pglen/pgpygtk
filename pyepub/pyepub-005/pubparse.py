#!/usr/bin/env python

import re

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")
import gobject, pango, math, traceback, subprocess

from HTMLParser import HTMLParser
import pubdisp, pubutil

# Pre-create our regexes

isvalue = re.compile("([a-z]+)|([A-Z]+)|([0-9]+)")
ischapter = re.compile("chapter", re.IGNORECASE)

def get_attr(attrs, xname):
    for aa in attrs:
        if aa[0] == xname: 
            #print "get_attr", aa[1]
            return aa[1]
        
# ------------------------------------------------------------------------
# Parsers. These are simplified versions of the real thing. Parses links,
# paragraphs, lists, italic and bold. Outputs verbtim whatever else is 
# there. It produces remarkable results despite its simplicity. If in 
# doubt, the original HTML is displayed in the top pane. 
# (drag Pane Handle to view)

class MyHTMLParser(HTMLParser):

    def __init__(self, mw):
    
        self.mw = mw
        HTMLParser.__init__(self)
        self.mark = True
        self.txt = "";  self.ita = "";  self.bold = ""
        self.link = ""; self.ll = ""
        self.in_p = 0;  self.in_h = 0;  self.in_i = 0;  self.in_t = 0
        self.in_l = 0;  self.in_b = 0
        self.id_p = 0;  self.id_h = 0;  self.id_i = 0
        self.currattr = None; self.currtag = None
        
        self.outq = []
                    
    def handle_starttag(self, tag, attrs):

        self.currtag = tag; self.currattr = attrs
        
        print " -- Begin '%s' tag '%s'" % (tag, attrs)
        
        if tag == "p":
            if self.in_p != "":
                print "Warning: non closed '%s' tag", tag
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_p = tag
            self.id_p = get_attr(attrs,"id")
        
        elif tag == "h1" or tag == "h2" or tag == "h3" or \
                tag == "h4" or tag == "h5" :
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_h = tag
            self.id_h = get_attr(attrs, "id")
        
        elif tag == "a":
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_l = tag
            self.ll = get_attr(attrs, "href")
                    
        elif tag == "i":
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_i = tag
            
        elif tag == "b":
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_b = tag
            
        elif tag == "title":
            #print " -- Begin %s tag %s" % (tag, attrs)
            self.in_t = tag
        else:
            #print " -- Begin %s tag %s" % (tag, attrs)
            pass
            
    # --------------------------------------------------------------------
                        
    def handle_endtag(self, tag):
    
        global isvalue, ischapter
        print " -- End '%s' tag" % tag
        
        if tag == "html":
            print "flush"
            self.flush()
            print "text", self.txt
        
        if tag == "p":
            #print para; print
            #print "id_p", id_p
            # Anything of value?
            #if isvalue.search(para2):
            self.flush()
            self.in_p = 0; self.id_p = 0
            
        elif tag == "h1" or tag == "h2" or tag == "h3" or \
                tag == "h4" or tag == "h5" :
            nnn = None;
            if self.id_h: nnn = str(self.id_h)
            for aa in self.outq:
                nnn = None;
                if self.id_p: nnn = str(self.id_p)
                print "tagname:", nnn, "tag:", aa[1]
                print "head '" + aa[0] + "'"
                
                para2 = aa[0].replace("\n", " ")
                para2 = singlespace(para2)
                
                xtag = gtk.TextTag(nnn)
                xtag.set_property("weight", pango.WEIGHT_BOLD)
                self.mw.add_text_xtag(para2 + "\n\n", xtag, False)
                
            self.outq = []; 
            self.in_h = 0
            
        elif tag == "i":
            #print "ita" + "'" + self.ita + "'"; print
            self.outq.append((self.ita, self.in_i))
            self.ita = ""; self.in_i = 0
            #print "endtag %s" % tag
            
        elif tag == "b":
            #print "bold" + "'" + self.bold + "'"; print
            self.outq.append((self.bold, self.in_b))
            self.bol = ""; self.in_b = 0
            #print "endtag %s" % tag
            
        elif tag == "title":
            #print "title" + "'" + self.txt + "'"; print
            pass
        else:
            pass
            #print "endtag %s" % tag
            #print "text", self.txt; print
            #self.mw.add_text("text" + txt + "\n")
            #txt = ""
            
        if tag == "a":
            print "link:", "'" + self.link + "'"; print
            self.outq.append((self.link, self.in_l))
            self.in_l = 0; self.link = ""
            pass
            
    def handle_data(self, data):
        print " -- data '%s'" % data
        if self.in_p != 0:
            self.outq.append((data, self.in_p))
        elif self.in_h:
            self.outq.append((data, self.in_h))
        else:
            #self.outq.append((data, None))
            self.txt += data
            
        if self.in_i:
            self.ita +=   data
        if self.in_l:
            self.link +=  data
        if self.in_b:
            self.bold +=  data

    def flush(self):
        for aa in self.outq:
            nnn = None;
            if self.id_p: nnn = str(self.id_p)
            print "tagname:", nnn, "tag:", aa[1]
            print "para: '" + aa[0] + "'"
            
            para2 = aa[0].replace("\n", " ")
            para2 = singlespace(para2)
            
            #if ischapter.match(para2):
                #if self.mark:
                #    self.mw.update_tree(para2, para2)
                #if(nnn):
                #    self.mw.add_text_mark(nnn)
                
            xtag = gtk.TextTag(nnn)
            if aa[1] == "p":
                xtag.set_property("wrap_mode", gtk.WRAP_WORD)
                xtag.set_property("justification", gtk.JUSTIFY_FILL)
                pass    
            if aa[1] == "i":
                xtag.set_property("style", pango.STYLE_ITALIC)
                xtag.set_property("wrap_mode", gtk.WRAP_WORD)
                
            if aa[1] == "b":
                xtag.set_property("weight", pango.WEIGHT_BOLD)
                xtag.set_property("wrap_mode", gtk.WRAP_WORD)
                
            if aa[1] == "a":
                print "plink:", para2
                xtag.set_data("link", self.ll[1])
                #xtag.set_property("style", pango.STYLE_ITALIC)
                xtag.set_property("foreground", "darkblue")
        
            self.mw.add_text_xtag(para2, xtag, False)
                
        xtag2 = gtk.TextTag()
        self.mw.add_text_xtag("\n\n", xtag2, False)
        self.outq = []    
                    
                                    
# ------------------------------------------------------------------------

class TocHTMLParser(HTMLParser):

    def __init__(self, mw):
        self.mw = mw
        HTMLParser.__init__(self)
        self.currattr = None
        self.curtag = ""
        self.txt = "";      self.label = ""
        self.auth = "";     self.title = ""
        self.firstlink = ""
            
    def handle_starttag(self, tag, attrs):
        if tag != "text":
            #print " -- Begin '%s' tag '%s'" % (tag, attrs)
            self.currtag = tag.lower()
            self.currattr = attrs
                        
    def handle_endtag(self, tag):
        
        erase = True
        para2 = self.txt.replace("\n", " ")
        para2 = singlespace(para2)
        para2 = para2.strip()
        
        if tag != "text":
            pass
            #print " -- End '%s' tag - text '%s'" % (tag, para2)
            
        if self.currtag == "doctitle":
            #print "TITLE",  "'" + para2 + "'"
            self.title = para2
            old = self.mw.get_title()
            self.mw.set_title(old + " '" + self.title + "' ")
        
        if self.currtag == "docauthor":
            #print "AUTHOR", "'" + para2 + "'"
            self.auth = para2
            old = self.mw.get_title()
            self.mw.set_title(old + " '" + self.auth + "' ")
        
        if self.currtag == "navlabel":
            self.label = para2
            
        if self.currtag == "content":
            #print "Found", self.label, " -- ", self.currattr[0][1] 
            if not self.firstlink:
               self.firstlink = self.currattr[0][1]
            self.mw.update_tree(self.label, self.currattr[0][1])
        
        if self.currtag == "text":
            erase = False
        
        if erase:
            self.txt = ""
        self.currtag = ""
            
    def handle_data(self, data):
        # Just remember stuff ....
        self.txt += data

# ------------------------------------------------------------------------
# Change spaces to single space

def singlespace(strx):
    prev = ""; res = ""
    for aa in range(len(strx)):
        bb = strx[aa]
        if prev == " " and bb == " ":
            pass
        else:
            res += bb
        prev = bb
    return res        







