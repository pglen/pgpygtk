#!/usr/bin/env python

import re

import warnings; warnings.simplefilter("ignore");
import gtk; warnings.simplefilter("default")
import gobject, pango, math, traceback, subprocess

from HTMLParser import HTMLParser
import pubdisp, pubutil
import htmlentitydefs

from    pubutil import Config, print_exception, usleep
from    pubparse import HTML_Recurse

# Pre-create our regexes

isvalue = re.compile("([a-z]+)|([A-Z]+)|([0-9]+)|(\n)+")

# ------------------------------------------------------------------------
# Derived class

class HTML_Parser(HTML_Recurse):

    def __init__(self):
        HTML_Recurse.__init__(self)
        self.last_tag = None
        self.bold = 0
        self.outq = []
        self.href = ""
        self.data = ""

    def got_tag(self, tag, attrs):
        #print "start tag",  "'" + tag + "'", "attrs", attrs
        for aa in attrs:
            if aa[0] == "href":
                self.href = aa[1]
        self.last_tag = tag
        self.outq.append((tag, self.data))
        self.data = ""

    def got_endtag(self, tag, attrs):
        #print "end etag", "'" + tag + "'", "attrs", attrs
        self.last_tag = tag
        self.outq.append((tag, self.data))
        self.data = ""

        for aa  in self.outq:
            #print "output", aa
            #// -----------------------------------------------------------
            if aa[0] == 'p':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            ,"  ", "")

            if aa[0] == '/p':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            ,"", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'br':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            ,"", "\n")
            if aa[0] == 'br/':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            ,"", "\n")
            #// -----------------------------------------------------------
            '''if aa[0] == 'ul':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/ul':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )'''

            if aa[0] == 'li':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , " o ")

            if aa[0] == '/li':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n")
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
            if aa[0] == 'code':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/code':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
            #// -----------------------------------------------------------
            if aa[0] == 'div':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/div':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
            #// -----------------------------------------------------------
            if aa[0] == 'pre':
                xtag = gtk.TextTag()
                self.mw.add_text_xtag(aa[1], xtag, False)

            if aa[0] == '/pre':
                xtag = gtk.TextTag()
                self.mw.add_text_xtag(aa[1], xtag, False)
            #// -----------------------------------------------------------
            if aa[0] == 'h1':
                self.put_tag(aa, (\
                            ("size_points",     25),                \
                            ("header",          "+12"),             \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/h1':
                self.put_tag(aa, (\
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n\n")
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
                            ,"", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'h3':
                self.put_tag(aa, (\
                            ("size_points",     18),               \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/h3':
                self.put_tag(aa, (\
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'h4':
                self.put_tag(aa, (\
                            ("size_points",     16),               \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/h4':
                self.put_tag(aa, (\
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'h5':
                self.put_tag(aa, (\
                            ("size_points",     12),               \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/h5':
                self.put_tag(aa, (\
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n\n")
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
                            ("foreground",      "darkblue"), \
                            ("link",            self.href)) \
                            )

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
        self.outq = []

    def got_data(self, data):
        #print "data", self.last_tag, "'" + data + "'"
        #self.outq.append((self.last_tag, data))
        self.data += data
        pass

    def got_comment(self, data):
        #print "comment", data
        pass

    def put_tag(self, aa, props, pre = "", post = ""):
        para2 = aa[1].replace("\n", " ")
        para2 = self.singlespace(para2)
        para2 = pre + para2 + post
        
        if not isvalue.search(para2):
            #print "Empty tag", post
            return

        xtag = gtk.TextTag()
        for aa, bb in props:
            try:
                xtag.set_property(aa, bb)
            except:
                # If cannot set, assume new data (like link)
                xtag.set_data(aa, bb)
        self.mw.add_text_xtag(para2, xtag, False)

    # Change spaces to single space
    def singlespace(self, strx):
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
# Start of program: (mostly tests)

if __name__ == '__main__':

    import sys
    global mw, par
    
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
            mw.prog.set_text("Reading %d" % fh.tell())
            usleep(1)
            par.feed(sss)
    
        fh.close()
    
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








