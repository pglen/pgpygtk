#!/usr/bin/env python

import re

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")
import gobject, pango, math, traceback, subprocess

from HTMLParser import HTMLParser
import pubdisp, pubutil

# ------------------------------------------------------------------------
# Parsers. These are simplified versions of the real thing. Parses links,
# paragraphs, lists, italic and bold. Outputs verbtim whatever else is 
# there. It produces remarkable results despite its simplicity. If in 
# doubt, the original HTML is displayed in the top pane. 
# (drag Pane Handle to view)
                    
# Pre-create our regexes
# Some of the tags can span multi line ... bad specs

starttag = re.compile("\<[a-zA-Z0-9 \t_,:;+*%?!&$\(\)_\#=~@\-\^\"\n\.]+\>", re.MULTILINE)
endtag   = re.compile("\</[a-zA-Z0-9 \t+\"\n]+\>", re.MULTILINE)
endtag2  = re.compile("\<[a-zA-Z0-9 \t+\"\n]+\/>", re.MULTILINE)
iscomm   = re.compile("<!--[a-zA-Z0-9_ \t/,\:;\+\*%?!&$\(\)_#=~@\n\.-]+-->", re.MULTILINE)

# ------------------------------------------------------------------------

class   HTML_Recurse():

    def __init__(self):
        self.buf = ""
        self.feedret = False
        
    def feed(self, xstr):
        self.feedret = False
        self.buf += xstr
        cc = tt = ee = ee2 = None
        while 1:
            for aa in range(len(self.buf)):
                cc = iscomm.match(self.buf[aa:])
                if cc:
                    self.got_comment(self.buf[aa+cc.start():aa+cc.end()])
                    self.buf = self.buf[aa+cc.end():]
                    break
                tt = starttag.match(self.buf[aa:])
                if tt:
                    self.got_data(self.buf[:aa])
                    self._parse_tag(self.buf[aa+tt.start():aa+tt.end()], self.got_tag)
                    self.buf = self.buf[aa+tt.end():]
                    break
                ee = endtag.match(self.buf[aa:])
                if ee:
                    self.got_data(self.buf[:aa])
                    self._parse_tag(self.buf[aa+ee.start():aa+ee.end()], self.got_endtag)
                    self.buf = self.buf[aa+ee.end():]
                    break

                ee2 = endtag2.match(self.buf[aa:])
                if ee2:
                    self.got_data(self.buf[:aa])
                    self._parse_tag(self.buf[aa+ee2.start():aa+ee2.end()], self.got_endtag)
                    self.buf = self.buf[aa+ee2.end():]
                    break

            # No match, wait for more
            if not (cc or tt or ee or ee2):
                break
            if len(self.buf) < 1:
                break
        return self.feedret

    # Internal: Get tag, get attributes, remove quotes, call callback
    def _parse_tag(self, tag, callx):
        #print "parse_tag", tag
        xtag = tag[1:-1]
        attrs = xtag.split()
        xtag2 = attrs[0]; attrs = attrs[1:]
        for aa in xrange(len(attrs)):
            try:
                aaa, bbb = attrs[aa].split("=")
                attrs[aa] = (aaa.replace("\"", ""), \
                        bbb.replace("\"", ""))
            except:
                #print_exception("parse tag")
                pass
        callx(xtag2, attrs)

    # Overrides
    def got_tag(self, tag, attrs):
        pass
    def got_endtag(self, tag, attrs):
        pass
    def got_data(self, data):
        pass
    def got_comment(self, data):
        pass

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








