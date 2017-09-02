#!/usr/bin/env python

import signal, os, time, string, pickle, gconf
from threading import Timer
import gobject, gtk, pango

from pedutil import *

index2 = []; index3 = []

# Punctuation characters (most all non asci chars)
# Note the space at the beginning
punctuation = " ,./<>?;\':[]\{}|=-`!@#$%^&*()_+\""

# Benchmark time ma
#got_clock = 0

# ------------------------------------------------------------------------
# Spell buffer. We read the spell.txt file into a pyn array. 
# Lower case it, and we create an index to the letters a-z.
# On search, we look at the first 2 letters and search the index for offset 
# in the array. This loads on 300 msec on an average system, and spell 
# checks the current context (of an average python file) in 5-15 msec. 
# Not bad for a 200+ thousand word dictionary. Without the index the 
# check took 3.00 full seconds. The spell operates on the idle timer,
# within the next 2 ticks.

# We spell check the strings and comments only. The algorithm used to 
# select the checkable portion of the file is similar to the algorithm 
# used in coloring. Speed versus intelligence, so 'backslash quote' will
# fool the speller into thinking it is code.
# As the speller's presence is advisory, no harm is done. You can 
# cooperate in your strings with the speller by using single quote in 
# double quote strings and vice-versa. One useful trick is to place
# the offending quote to the of of strings. (see 'punctuation' above)

def spell(self2):

    #global got_clock
    global document
    document = self2

    # Profile line, use it on bottlenecks
    #ck = time.clock()   
    
    if not self2.spell:        
        if len(self2.ularr):
            self2.ularr = []
            self2.invalidate()
        return
    
    #print "spell"
    
    self2.ularr = []
    try:    
        errcnt = 0
        xlen = len(self2.text); cnt = self2.ypos
        yyy = self2.ypos + self2.get_height() / self2.cyy 

        # Contain checking in visible range
        while True:
            if cnt >= xlen: break
            if cnt >= yyy: break

            line = self2.text[cnt]
            
            # Comments      
            ccc = line.find("#"); cccc = line.find('"')

            # See if hash preceeds quote (if any)
            if ccc >= 0 and (cccc > ccc or cccc == -1):
                ccc2 = calc_tabs(line, ccc)                    
                err = spell_line(line, ccc, len(line))
                for ss, ee in err:
                    self2.ularr.append((ss, cnt, ee))
                    #print  ss, ee, cnt, "'" + line[ss:ee] + "'"
                    errcnt += 1
            else:   
                # Locate strings
                qqq = 0                                 
                while True:
                    quote = '"'
                    sss = qqq
                    qqq = line.find(quote, qqq); 
                    if qqq < 0:
                        # See if single quote is foound
                        qqq = line.find("'", sss); 
                        if qqq >= 0:
                            quote = "'"                    
                    if qqq >= 0:
                        qqq += 1
                        qqqq = line.find(quote, qqq)
                        if qqqq >= 0:
                            qqq -= self2.xpos           
                            qqq2 = calc_tabs(line, qqq)                    
                            err = spell_line(line, qqq, qqqq)
                            for ss, ee in err:
                                self2.ularr.append((ss, cnt, ee))
                                #print  ss, ee, cnt, "'" + line[ss:ee] + "'"
                                errcnt += 1
                            qqq = qqqq + 1
                        else:
                            break
                    else:
                        break
            cnt += 1
        self2.invalidate()
        #self2.mained.update_statusbar("%d spelling mistakes." % errcnt)                     

    except:
        print "Exception on spell check", sys.exc_info()
        
    #print  "all", time.clock() - got_clock        

# Ret an array of error misspelled x,y coord for this line
def spell_line(line, beg, end):

    #print "spell_line", line[beg:end]
    err = [];  idx = beg
    while True:
        if idx >= end: break
        idx = xnextchar2(line, punctuation, idx)
        #ss, ee = selword(line, idx)
        ss, ee = selasci(line, idx)
        found = spell_word(line[ss:ee])
        # Communcate it to upper layers
        if not found:
            err.append((ss, ee))
        idx = ee + 1
    return err
    
# Return True if word found

def spell_word(word):

    #print "word", "'" + word + "'"
    
    if len(word) <= 1:          # Do not spell short words
        return  True
        
    if word[0] == "#":          # Hex Numbers, hashes
        return True   
    
    lw = word.lower()
    global index2, index3
    # Pre read index
    if len(index2) == 0:
        build_index()
        
    found = False
    # Locate start and end
    cnt = 0; sss = 0; eee = 0
    for bb, bbb in index3:
        if lw[0:2] == bb:
            sss = bbb
            eee = index3[cnt+1][1]
            break
        cnt += 1
    #print "start, end", sss, eee
    # Finally, search within limits
    while True:
        if sss >= eee: break        
        if  index2[sss] == lw:
            #print "found", lw, word
            found = True
            break
        sss += 1
            
    return found

# ------------------------------------------------------------------------

def build_index():

    global index2, index3

    global document

    #document.mained.update_statusbar("Loading dictionary")                     
    
    # It is an msdos file (don't ask)
    index = readfile(get_exec_path("spell.txt"), "\r\n")

    #print index[0:10]
    for ww in index:
        index2.append(ww.lower())               
        
    #print index2[0:10]        
    prev = ""; cnt = 0
    for ii in index2:
        if len(ii) >= 2:
            # The dictionary contained some garbage
            if ii[0].isalnum() and ii[1].isalnum():        
                ss = ii[0:2]
                if ss != prev:                                      
                    index3.append((ss, cnt))    
                    prev = ss                    
        cnt += 1     
        
    # End Marker              
    index3.append((" ", cnt))            
    #print index3
    
    #global got_clock
    #print  "building idx", time.clock() - got_clock        
    
    #document.mained.update_statusbar(" ")                     
        
# EOF



