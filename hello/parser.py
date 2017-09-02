#!/usr/bin/env python

import sys, os, pygtk, gobject, pango, gtk
import re

# ------------------------------------------------------------------------
# 

class ParseEvent():
    
    def run(self, typex, mmm):
        #print typex, mmm.start(), mmm.end(), mmm.string
        print typex, mmm.string[:mmm.start()]

# ------------------------------------------------------------------------
# 
  #[100 ,  "str2", re.compile("\".*\"")      ], \
          
enum = 100
tokens =    [10,  "span", re.compile("<span ")     ], \
            [20,  "endspan", re.compile("</span>")     ], \
            [40,   "it", re.compile("<i>")         ], \
            [50,   "eit", re.compile("</i>")        ], \
            [60,   "bold", re.compile("<b>")         ], \
            [70,   "ebold", re.compile("</b>")        ], \
            [90 ,  "escquo", re.compile(r"\\\"")  ], \
            [90 ,  "dblbs", re.compile(r"\\\\")  ], \
            [90 ,  "iden", re.compile("[A-Za-z0-0_]+")  ], \
            [80 ,  "str", re.compile("\".*?\"")     ], \
            [80 ,  "str2", re.compile("\'.*?\'")     ], \
            [110 ,  "eq", re.compile("=")           ], \
            [120 ,  "lt", re.compile("<")           ], \
            [130 ,  "gt", re.compile(">")           ], \
            [140 ,  "sp", re.compile(" ")           ], \
            [150 ,  "tab", re.compile("\t")          ], \
            [160 ,  "nl", re.compile("\n")          ], \
            [170 ,  "any", re.compile(".")           ], \

class ParseItem():

    def __init__(self):
        cnt = 0; 

        #for tt in tokens:
        #    print tt
        #    self.comptok[cnt] = re

    def Iter(self, pos, strx):
        #print strx[pos:]
        for aa, bb, cc in tokens:
            mmm = cc.match(strx, pos)
            if mmm:
                #print mmm.end() - mmm.start(), strx[mmm.start():mmm.end()]
                tt = aa, bb, mmm
                return tt
        
        return None;

class Parse():

    def __init__(self, data, item, callback):
        stack = Stack()
   
        print data  
        lastpos = 0;  pos = 0; lenx = len(data)
        while True:
            if pos >= lenx:
                break; 
            tt = item.Iter(pos, data)
            mmm = tt[2]
            if mmm: 
                # skip token                
                pos = mmm.end()
                #print  "'" + mmm.re.pattern + "'\t", mmm.start(), mmm.end(),"\t", data[mmm.start():mmm.end()]
                print  tt[1], "'" + data[mmm.start():mmm.end()] + "' - ",
                stack.push(tt)
            else:
                pos += 1  # step to next
                
        print "\nShowing stack:"
        while True:
            tt = stack.pop()
            if not tt: 
                break
            print tt[1], "'" + data[tt[2].start():tt[2].end()] + "' - ",

        stack.reset()
        print "\nShowing list:"
        while True:
            tt = stack.get()
            if not tt: 
                break
            print tt[1], "'" + data[tt[2].start():tt[2].end()] + "' - ",


class Stack():

    def __init__(self):
        self.store = []
        self.reset()

    def push(self, item):
        try:
            self.store.append(item)
        except Exception as xxx:
            print xxx

        self.cnt = self.cnt+1

    def pop(self):
        if len(self.store) == 0: return None
        item = self.store.pop(len(self.store) - 1) 
        return item

    def get(self):
        if len(self.store) == 0: return None
        item = self.store.pop(0)
        return item
    
    # non destructive pop
    def pop2(self):
        if self.cnt <= 0: return None
        self.cnt = self.cnt - 1
        item = self.store[self.cnt] 
        return item

    # non destructive get
    def get2(self):
        if self.gcnt >= len(self.store): return None
        item = self.store[self.gcnt] 
        self.gcnt = self.gcnt + 1
        return item
   
    # Start counters fresh 
    def reset(self):
        self.cnt = 0
        self.gcnt = 0

    def len():
        return len(store)
        
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    strx = sys.argv[1]    
    f = open(strx)
    buf = f.read()
    f.close()
       
    Parse(buf, ParseItem(), ParseEvent())
    
    #main()

