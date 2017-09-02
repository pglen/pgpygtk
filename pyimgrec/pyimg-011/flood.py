#!/usr/bin/env python

import  os, sys, getopt, signal, array
import  gobject, gtk, pango, time
from    random import *
import  stack

import pyimgrec.imgrec as imgrec

# Placeholder for lots of params for the floodfill function
# Passing a data class will make it private / reentrant data

reenter = 0

class floodParm():

    def __init__(self, divider, darr):
    
        self.cnt = 0;       self.depth = 0
        self.mark = 0;      self.ddd = divider
        self.hstep = 0;     self.vstep = 0
        self.colx = 0x808080
        self.tresh = 50;    self.breath = divider
        self.darr = darr;     self.spaces = {}
        self.stack = stack.Stack()
        
        self.inval = None   # Callback
        
        #for aa in range(divider):
        #    self.spaces[aa] = {}
      
# ------------------------------------------------------------------------
# Flood fill. Fill in star formation, clockwise. Re-written from recursive 
# to stack based. FYI: python (2.6) only does 1000 deep recursion.
# If two functions are recursed, that goes to 500 ... 
# Example: func1() calls func2() recurses to func1() -- 500 of these
#
# Synonyms for directions:
#            L-left R-right A-above B-below
#
# Scanning order:
#           A, AR, R, BR, B, BL, L, AL
#
# Most of the parameters are passed tru a class. Relies on stack.py

def flood(xxx, yyy, param):
    
    global reenter    
    # Safety net
    if reenter:
        print "Flood re-entry", xxx, yyy;  return
    reenter +=1
    
    # Mark initial position
    try:
        param.mark = param.darr[xxx][yyy]
    except KeyError:
        print "Exceeded allocated array %d / %d (%d)" %( xxx, yyy, param.ddd)
        reenter -= 1
        return
    
    param.stack.push((xxx, yyy))
    mark_done(xxx, yyy, 1, param)
    
    # Loop until done
    while True :        
    
        param.cnt += 1; 
            
        # To observe in action, if requested
        if param.inval:
            if param.cnt % param.breath == 0:
                param.inval(param);
      
        #print "Scannning", xxx, yyy
        
        # ----------------------------------------------------------------
        # Walk the patches (see order in header)
        
        xxx2 = xxx; yyy2 = yyy-1  
        ret = scan_one(xxx2, yyy2, param)
        if  ret[0] == -1: break;
        if  ret[0] ==  1: xxx = ret[1]; yyy = ret[2]
        #print "A", diff
        
        xxx2 = xxx+1; yyy2 = yyy-1  
        ret = scan_one(xxx2, yyy2, param)
        if  ret[0] == -1: break;
        if  ret[0] ==  1: xxx = ret[1]; yyy = ret[2]
        #print "AR", diff
            
        xxx2 = xxx+1; yyy2 = yyy  
        ret = scan_one(xxx2, yyy2, param)
        if  ret[0] == -1: break;
        if  ret[0] ==  1: xxx = ret[1]; yyy = ret[2]
        #print "R", diff
        
        xxx2 = xxx+1; yyy2 = yyy+1  
        ret = scan_one(xxx2, yyy2, param)
        if  ret[0] == -1: break;
        if  ret[0] ==  1: xxx = ret[1]; yyy = ret[2]
        #print "BR", diff
          
        xxx2 = xxx; yyy2 = yyy+1  
        ret = scan_one(xxx2, yyy2, param)
        if  ret[0] == -1: break;
        if  ret[0] ==  1: xxx = ret[1]; yyy = ret[2]
        #print "B", diff
        
        xxx2 = xxx-1; yyy2 = yyy+1  
        ret = scan_one(xxx2, yyy2, param)
        if  ret[0] == -1: break;
        if  ret[0] ==  1: xxx = ret[1]; yyy = ret[2]
        #print "BL", diff
        
        xxx2 = xxx-1; yyy2 = yyy  
        ret = scan_one(xxx2, yyy2, param)
        if  ret[0] == -1: break;
        if  ret[0] ==  1: xxx = ret[1]; yyy = ret[2]
        #print "L", diff
    
        xxx2 = xxx-1; yyy2 = yyy-1  
        ret = scan_one(xxx2, yyy2, param)
        if  ret[0] == -1: break;
        if  ret[0] ==  1: xxx = ret[1]; yyy = ret[2]
        #print "AL", diff
        
        # ----------------------------------------------------------------
        
        if param.stack.stacklen() == 0:
            print "while break end"
            break
  
    reenter -=1
    
    print "done"
    return
        
# ------------------------------------------------------------------------    
# Scan new patch in direction specified by the caller

def scan_one(xxx2, yyy2, param):

    done = is_done(xxx2, yyy2, param)
    if done != -1: 
        #print "Shcut", done, xxx2, yyy2
        try: 
            xxx, yyy = param.stack.pop()    
            param.depth -= 1
            return 1, xxx, yyy
        except:
            #print "scan_one is_done"
            return -1, 0, 0
    try:
        diff = imgrec.diffcol(param.mark, param.darr[xxx2][yyy2]) 
    except:
        #print "out of range for ", xxx2, yyy2
        try: 
            xxx, yyy = param.stack.pop()    
            param.depth -= 1
            return 1, xxx, yyy
        except:
            mark_done(xxx2, yyy2, 0, param)
            #print "scan_one done"
            return -1, 0, 0
        
    if diff[1] < param.tresh:
        #print "OK", xxx2, yyy2, diff[1]
        mark_done(xxx2, yyy2, 1, param)
        param.stack.push((xxx2, yyy2))
        param.depth += 1
        return 1, xxx2, yyy2
    else:
        #print "NOK", xxx2, yyy2, diff[1]
        mark_done(xxx2, yyy2, 0, param)
        try: 
            xxx, yyy = param.stack.pop()    
            param.depth -= 1
            return 1, xxx, yyy
        except:
            #print "scan_one 2 done"
            return -1, 0, 0
            
    return 0, 0, 0
            
# ------------------------------------------------------------------------    
# Return flag if visited before

def is_done(xxx, yyy, param):
    aa = -1
    try:
        aa = param.spaces[xxx, yyy]
    except:
        pass
    return aa 
        
# ------------------------------------------------------------------------    
# Mark a cell done

def mark_done(xxx, yyy, flag, param):

        param.spaces[xxx, yyy] = flag

# ------------------------------------------------------------------------    
# Flood fill. Initial attempt.

def flood2(darr, xxx, yyy, hstep, vstep, ddd, tresh):

    www = ddd;  hhh = ddd;
    
    mark = darr[xxx][yyy]
    # Walk right
    for aa in range(xxx+1, www):
        diff = imgrec.diffcol(mark, darr[aa][yyy])
        if diff[1] > tresh:
            break;
        imgrec.frame(aa * hstep, yyy * vstep, 
                    (aa + 1) * hstep, (yyy + 1) * vstep, 0xff000000)
        #print "right", hex(mark), hex(darr[aa][yyy]), hex(diff[0]), diff[1]
    
    # Walk left
    for aa in range(xxx-1, 0, -1):
        diff = imgrec.diffcol(mark, darr[aa][yyy]) 
        if diff[1] > tresh:
            break;
        #print "left", hex(mark), hex(darr[aa][yyy]), hex(diff[0]), diff[1]
        imgrec.frame(aa * hstep, yyy * vstep, 
                    (aa + 1) * hstep, (yyy + 1) * vstep, 0xff008800)
    
    # Walk up
    for aa in range(yyy-1, 0, -1):
        diff = imgrec.diffcol(mark, darr[xxx][aa])
        if diff[1] > tresh:
            break;
        imgrec.frame(xxx * hstep, aa * vstep, 
                    (xxx + 1) * hstep, (aa + 1) * vstep, 0xff800000)
        #print "up", hex(mark), hex(darr[xxx][aa]), hex(diff[0]), diff[1]
  
    # Walk down
    for aa in range(yyy+1, hhh):
        diff = imgrec.diffcol(mark, darr[xxx][aa])
        if diff[1] > tresh:
            break;
        imgrec.frame(xxx * hstep, aa * vstep, 
                    (xxx + 1) * hstep, (aa + 1) * vstep, 0xff000080)
        #print "down", hex(mark), hex(darr[xxx][aa]), hex(diff[0]), diff[1]
    
    # Mark origin
    fframe(xxx, yyy, hstep, vstep, 0xff00ffff)
        
def fframe(xx, yy, hstep, vstep, col = 0xff000000):
    imgrec.frame(xx * hstep, yy * vstep, 
                    (xx + 1) * hstep, (yy + 1) * vstep, col)
        
# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    got_clock = time.clock() + float(msec) / 1000
    #print got_clock
    while True:
        if time.clock() > got_clock:
            break
        gtk.main_iteration_do(False)        
      










