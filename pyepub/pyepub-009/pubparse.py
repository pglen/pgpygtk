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


# As simple as possible look at the last try before simplification ...
# GT char + one or more of (almost any char) + zero or more of (quoted string)
#       + LT char
#"\<[a-zA-Z0-9 \t_,:;+*%?!&$\(\)_\#=~@\{\}\-\^\n\.]+?(\".*?\")*\>", re.MULTILINE)

starttag = re.compile("\<[^>/]+(\".*?\")*\>", re.MULTILINE)

# GT char + one or more of (almost any char) + zero or more of (quoted string)
#       + LT char

endtag   = re.compile("\</[a-zA-Z0-9 \t+?\"\n]+\>", re.MULTILINE)

# GT char + one or more of (almost any char) + zero or more of (quoted string)
#       + Slash LT char

#endtag2  = re.compile("\<[a-zA-Z0-9 \t+?\"\n]+\/>", re.MULTILINE)
endtag2  = re.compile("\<[^>/]+(\".*?\")*\/\>", re.MULTILINE)

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
                    self._parse_tag2(self.buf[aa+ee2.start():aa+ee2.end()], self.got_endtag)
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

    def _parse_tag2(self, tag, callx):
        xtag = tag[1:-1]
        attrs = xtag.split()
        xtag2 = attrs[0]; attrs = attrs[1:]
        for aa in xrange(len(attrs)):
            try:
                aaa, bbb = attrs[aa].split("=")
                if bbb != "":
                    # Correct tag resudial
                    if bbb.endswith("/"):
                        bbb = bbb[:-1]        
                    attrs[aa] = (aaa.replace("\"", ""), \
                            bbb.replace("\"", ""))
            except:
                #pubutil.print_exception("parse tag")
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

    def __init__(self, content):
        HTMLParser.__init__(self)
        self.content = content
        self.currattr = None
        self.curtag = "";   self.firstlink = ""
        self.txt = "";      self.label = ""
        self.auth = "";     self.title = ""
            
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
        
        if self.currtag == "docauthor":
            #print "AUTHOR", "'" + para2 + "'"
            self.auth = para2
        
        if self.currtag == "navlabel":
            self.label = para2
            
        if self.currtag == "content":
            #print "Content", self.label, " -- ", self.currattr #[0][1] 
            if not self.firstlink:
               self.firstlink = self.currattr[0][1]
            self.content(self.label, self.currattr[0][1])
        
        if self.currtag == "text":
            erase = False
        
        if erase:
            self.txt = ""
        self.currtag = ""
            
    def handle_data(self, data):
        # Just remember stuff ....
        self.txt += data

# ------------------------------------------------------------------------

class ConHTMLParser(HTMLParser):

    def __init__(self, content2):
        HTMLParser.__init__(self)
        self.content = content2
        self.currattr = None
        self.curtag = "";   self.firstlink = ""
        self.txt = "";      self.label = ""
        self.auth = "";     self.title = ""
            
    def handle_starttag(self, tag, attrs):
        if tag != "text":
            #print " ++ Begin '%s' tag '%s'" % (tag, attrs)
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
            
        if self.currtag == "dc:title":
            #print "TITLE",  "'" + para2 + "'"
            self.title = para2
        
        if self.currtag == "dc:creator":
            #print "AUTHOR", "'" + para2 + "'"
            self.auth = para2
        
        if self.currtag == "navlabel":
            self.label = para2
            
        if self.currtag == "item":
            #print "Item", self.label, " -- ", self.currattr #[0][1] 
            self.id = ""; self.link = ""
            for aa in  self.currattr:
                if aa[0] == "id":
                    self.id = aa[1]
                if aa[0] == "href":
                    #print "href found", aa[0], aa[1]
                    if ".htm" in aa[1]:
                        self.link = aa[1]
            if self.link:            
                #print "got html file:", self.link
                if not self.firstlink:
                    self.firstlink = self.link
                self.content(self.id, self.link)
        
        if self.currtag == "text":
            erase = False
        
        if erase:
            self.txt = ""
        self.currtag = ""
            
    def handle_data(self, data):
        # Just remember stuff ....
        self.txt += data

# ------------------------------------------------------------------------

class RootHTMLParser(HTMLParser):

    def __init__(self, content):
        HTMLParser.__init__(self)
        self.content = content
        self.currattr = None
        self.curtag = "";   self.firstlink = ""
        self.txt = "";      self.label = ""
        self.auth = "";     self.title = ""
            
    def handle_starttag(self, tag, attrs):
        if tag != "text":
            #print " ++ Begin '%s' tag '%s'" % (tag, attrs)
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
            
        #print " ++ End '%s' tag " % (tag)
        
        if self.currtag == "rootfiles":
            #print "rootfile", self.label, " -- ", self.currattr #[0][1] 
            self.id = ""; self.link = ""
            for aa in  self.currattr:
                if aa[0] == "id":
                    self.id = aa[1]
                if aa[0] == "href":
                    #print "href found", aa[0], aa[1]
                    if ".htm" in aa[1]:
                        self.link = aa[1]
            if self.link:            
                #print "got html file:", self.link
                if not self.firstlink:
                    self.firstlink = self.link
                self.content(self.id, self.link)
        
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

def htmlentity(strx):
    prev = ""; res = ""
    for aa in range(len(strx)):
        strx2 = strx[aa:]
        mm = isEspace.match(strx2)
        if mm:
            res += " "
            aa += mm.end() 
        else:
            res += strx[aa]
        prev = bb
    return res        










