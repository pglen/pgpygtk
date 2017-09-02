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

isvalue   = re.compile("[a-zA-Z0-9]+", re.MULTILINE)
isEspace  = re.compile("&nbsp;", re.MULTILINE)

# ------------------------------------------------------------------------
# Derived class from  HTML_Recurse ... 

class HTML_Parser(HTML_Recurse):

    def __init__(self, conf):
        HTML_Recurse.__init__(self)
        self.last_tag = None
        self.bold = 0
        self.conf = conf
        self.getimagecb = None
        self.outq = []; self.attrs = []
        self.href = ""; self.data = ""; 
        self.old_para = ""

    def got_tag(self, tag, attrs):
        if self.conf.verbose:
            print "** start tag",  "'" + tag + "'", "attrs", attrs
        for aa in attrs:
            if aa[0] == "href":
                self.href = aa[1]
            if aa[0] == "id":
                #print "mark", tag, "'" + aa[1] + "'"
                self.mw.add_text_mark(aa[1])
        self.last_tag = tag
        self.attrs = attrs
        self.outq.append((tag, self.data))
        self.data = ""

    def got_endtag(self, tag, attrs):
        if self.conf.verbose:
            print "** end tag", "'" + tag + "'", "attrs", attrs
        for aa in attrs:
            if aa[0] == "href":
                self.href = aa[1]
            if aa[0] == "id":
                #print "mark", tag, "'" + aa[1] + "'"
                self.mw.add_text_mark(aa[1])
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
                            , " ")

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
                            ," ", " ")
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
                            ("size_points",     25),               \
                            ("header",          25),               \
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
            if aa[0] == '/h1':
                self.put_tag(aa, (\
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("size_points",     25),                \
                            ("header",          25),               \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'h2':
                self.put_tag(aa, (\
                            ("size_points",     20),                \
                            ("header",          "20"),              \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/h2':
                self.put_tag(aa, (\
                            ("size_points",     20),                \
                            ("header",          "20"),              \
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            ,"", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'h3':
                self.put_tag(aa, (\
                            ("size_points",     18),                \
                            ("header",          "18"),              \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/h3':
                self.put_tag(aa, (\
                            ("size_points",     18),                \
                            ("header",          "18"),              \
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'h4':
                self.put_tag(aa, (\
                            ("size_points",     16),                \
                            ("header",          "16"),              \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/h4':
                self.put_tag(aa, (\
                            ("size_points",     16),                \
                            ("header",          "16"),              \
                            ("weight", pango.WEIGHT_BOLD),          \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'h5':
                self.put_tag(aa, (\
                            ("size_points",     12),                \
                            ("header",          "16"),              \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )

            if aa[0] == '/h5':
                self.put_tag(aa, (\
                                ("weight", pango.WEIGHT_BOLD),          \
                            ("size_points",     12),                \
                            ("header",          "16"),              \
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            , "", "\n\n")
            #// -----------------------------------------------------------
            if aa[0] == 'b':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL),  \
                            ("weight", pango.WEIGHT_BOLD),)  \
                            )

            if aa[0] == '/b':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
            #// -----------------------------------------------------------
            if aa[0] == 'a':
                #print "link", aa, self.attrs, self.data
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL),  \
                            ("foreground",      "darkblue"), \
                            ("link",            self.href)) \
                            )

            if aa[0] == '/a':
                #print "link end", aa, self.attrs, self.data
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL),  \
                            ("foreground",      "darkblue"), \
                            ("link",            self.href)) \
                            )
            #// -----------------------------------------------------------
            if aa[0] == 'i':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL),  \
                            ("style", pango.STYLE_ITALIC),) \
                            )

            if aa[0] == '/i':
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
            #// -----------------------------------------------------------
            if aa[0] == 'img':
                #print aa, attrs, self.data
                for bb in attrs:
                    if bb[0] == "src":
                        if self.getimagecb:
                            pixbuf = self.getimagecb(bb[1])
                            if pixbuf:
                                self.mw.add_pixbuf(pixbuf)
                pass
            if aa[0] == '/img':
                #print aa, self.last_tag, self.data
                for bb in self.last_tag:
                    if bb[0] == "src":
                        print "image", bb[1]
                        
                self.put_tag(aa, (\
                            ("wrap_mode",       gtk.WRAP_WORD),     \
                            ("justification",   gtk.JUSTIFY_FILL))  \
                            )
                self.data = ""
            #// -----------------------------------------------------------
            
        self.outq = []

    def got_data(self, data):
        if self.conf.verbose:
            print "data", self.last_tag, "'" + data + "'"
        self.data += data
        pass

    def got_comment(self, data):
        #print "comment", data
        pass

    def put_tag(self, aa, props, pre = "", post = ""):
    
        para2 = aa[1].replace("\n", " ")
        para2 = self.singlespace(para2); para2 = self.htmlentity(para2)
        
        para2 = pre + para2 + post
        
        # Too much space looks bad
        if not isvalue.search(para2) and \
            not isvalue.search(self.old_para):
            #print "Duplicate empty tag", para2
            return
            
        self.old_para = para2
        
        xtag = gtk.TextTag()
        for aa in props:
            #print "setting prop", aa[0], aa[1]
            try:
                xtag.set_property(aa[0], aa[1])
            except:
                # If cannot set, assume new data (like link)
                #print "set data", aa[0], aa[1]
                xtag.set_data(aa[0], aa[1])
                
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
    
    # Change html entityies to their strings    
    def htmlentity(self, strx):
        prev = ""; res = ""; skip = 0
        for aa in range(len(strx)):
            if skip:
                skip -= 1; continue
            strx2 = strx[aa:]
            mm = isEspace.match(strx2)
            if mm:
                res += " "
                skip = mm.end() 
            else:
                res += strx[aa]
        return res        
    
# ------------------------------------------------------------------------
# Start of program: (mostly tests)

if __name__ == '__main__':

    import os, sys
    
    global mw
    
    # option, var_name, initial_val, function
    optarr = \
        ["d:",  "debug",        0,      None],      \
        ["v",   "verbose",      0,      None],      \
        ["q",   "quiet",        0,      None],      \
        ["x",   "extract",      0,      None],      \
        ["f",   "fullscreen",   0,      None],      \
    
    conf = Config(optarr)
    
    conf.data_dir = os.path.expanduser("~/.pyepub")
    try:   os.mkdir(conf.data_dir)
    except: pass
    
    def reader_tick():
        global mw
        fh = open(args[0])
        while 1:
            sss = fh.readline()
            if sss == "":
                break
            #print "got", sss
            mw.add_text(sss, True)
            mw.prog.set_text("Reading %d" % fh.tell())
            usleep(1)
            mw.par.feed(sss)
        fh.close()
    
    def callback(fname):
        print "callback", fname
    
    args = conf.comline(sys.argv[1:])

    if len(args) < 1:
        print "Usage: pubhtml.py htmlfile"
        sys.exit(1)

    mw = pubdisp.PubView(conf)
    par =  HTML_Parser(conf)
    mw.par = par
    mw.fname = ""; 
    mw.callback = callback
    par.mw = mw

    gobject.timeout_add(100, reader_tick)
    gtk.main()



