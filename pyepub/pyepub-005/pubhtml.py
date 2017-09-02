#!/usr/bin/env python

import re

import warnings; warnings.simplefilter("ignore"); 
import gtk; warnings.simplefilter("default")
import gobject, pango, math, traceback, subprocess

from HTMLParser import HTMLParser
import pubdisp, pubutil
import htmlentitydefs

from    pubutil import Config, print_exception, usleep

# ------------------------------------------------------------------------
# HTML Parser. This is a simplified version of a real HTML parser. 
# Parses links, paragraphs, lists, italic and bold. Outputs verbtim 
# whatever else is there. It allows tag recursion like: 
#           <p> para text <b> bold text </b> more para text</p>
#
# The simple parser produces remarkable results despite its simplicity. 
# If in doubt, the original HTML is displayed in the top pane. (Drag 
# Pane Handle to view text)

# Pre-create our regexes

#isvalue = re.compile("([a-z]+)|([A-Z]+)|([0-9]+)")
#ischapter = re.compile("chapter", re.IGNORECASE)
#ischapter = re.compile("chapter", re.IGNORECASE)
#justtag = re.compile("[a-zA-Z0-9]+")

# Some of the tags can span multi line ... bad specs
starttag = re.compile("\<[a-zA-Z0-9 \t_,:;+*%?!&$\(\)_\#=~@\-\^\"\n\.]+\>", re.MULTILINE)
endtag   = re.compile("\</[a-zA-Z0-9 \t+\"\n]+\>", re.MULTILINE)
endtag2  = re.compile("\<[a-zA-Z0-9 \t+\"\n]+\/>", re.MULTILINE)
iscomm   = re.compile("<!--[a-zA-Z0-9_ \t/,\:;\+\*%?!&$\(\)_#=~@\n\.-]+-->", re.MULTILINE)

# ------------------------------------------------------------------------

class   HTML_Recurse():

    def __init__(self):
        self.buf = ""

    def feed(self, xstr):
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
# Derived class

class HTML_Parser(HTML_Recurse):

    def __init__(self):
        HTML_Recurse.__init__(self)
        self.last_tag = None
        self.bold = 0
        self.outq = []
        self.href = ""
    
    def got_tag(self, tag, attrs):
        print "start tag",  "'" + tag + "'", "attrs", attrs 
        for aa in attrs:
            if aa[0] == "href":
                self.href = aa[1]
        self.last_tag = tag
        pass
    
    def got_endtag(self, tag, attrs):
        print "end etag", "'" + tag + "'", "attrs", attrs
        self.last_tag = tag
        self.outq.append((tag, ""))
        
        for aa  in self.outq:
            #print "output", aa
            
            #// -----------------------------------------------------------                            
            if aa[0] == 'p':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
                
            if aa[0] == '/p':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "\n")
                            
            #// -----------------------------------------------------------                            
            if aa[0] == 'span':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
                
            if aa[0] == '/span':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
            #// -----------------------------------------------------------                            
            if aa[0] == 'h1':
                self.put_tag(aa, (\
                            ("size_points",     25),               \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
                            
            if aa[0] == '/h1':
                self.put_tag(aa, (\
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "\n")
            #// -----------------------------------------------------------                            
            if aa[0] == 'h2':
                self.put_tag(aa, (\
                            ("size_points",     20),               \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
                            
            if aa[0] == '/h2':
                self.put_tag(aa, (\
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "\n")
            #// -----------------------------------------------------------                            
            if aa[0] == 'b':
                self.put_tag(aa, (\
                            ("weight", pango.WEIGHT_BOLD),)  \
                            )
                
            if aa[0] == '/b':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
                
            #// -----------------------------------------------------------                            
            
            if aa[0] == 'a':
                self.put_tag(aa, (\
                            ("foreground", "darkblue"), )\
                            , "", self.href)
                
            if aa[0] == '/a':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
                
            #// -----------------------------------------------------------                            
            if aa[0] == 'i':
                self.put_tag(aa, (\
                            ("style", pango.STYLE_ITALIC),) \
                            )
                
            if aa[0] == '/i':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
            #// -----------------------------------------------------------                            
            
        pass
        self.outq = []

    def got_data(self, data):
        #print "data", "'" + data + "'"
        self.outq.append((self.last_tag, data))
        pass

    def got_comment(self, data):
        print "comment", data
        pass
        
    def put_tag(self, aa, props, post = "", link = ""):
        para2 = aa[1].replace("\n", " ")
        para2 = singlespace(para2)
        xtag = gtk.TextTag()
        for aa, bb in props:
            xtag.set_property(aa, bb)
        if link:
            xtag.set_data("link", link)
        self.mw.add_text_xtag(para2 + post, xtag, False)

    # option, var_name, initial_val, function
optarr = \
    ["d:",  "debug",        0,      None],      \
    ["v",   "verbose",      0,      None],      \
    ["q",   "quiet",        0,      None],      \
    ["x",   "extract",      0,      None],      \
    ["f",   "fullscreen",   0,      None],      \

conf = Config(optarr)

def reader_tick():
    
    global mw, par
    
    fh = open(args[0])
    while 1:
        sss = fh.readline()
        if sss == "":
            break
        #print "got", sss
        mw.add_text(sss, True)
        par.feed(sss)
        
    fh.close()    
    
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

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    import sys    
    
    global mw, par
    
    args = conf.comline(sys.argv[1:])

    if len(args) < 1:
        print "Usage: pubhtml.py htmlfile"
        sys.exit(1)
        
    mw = pubdisp.PubView(conf)
    mw.fname = ""; #mw.loader = openHTML2

    par =  HTML_Parser()
    par.mw = mw
    gobject.timeout_add(100, reader_tick)
    gtk.main()






