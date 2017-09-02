#!/usr/bin/env python

import  os, sys, getopt, signal, array
import  gobject, gtk, pango, time
#from    timeit import Timer
from    random import *

import pyimgrec.imgrec as imgrec

# Placeholder for lots of params

class floodParm():

    def __init__(self, divider):
        self.cnt = 0
        self.depth = 0
        self.darr = {}
        self.mark = 0
        self.hstep = 0
        self.vstep = 0
        self.ddd = 0
        self.colx = 0x808080
        self.tresh = 50
        self.breath = 50
        self.inval = None
        self.spaces = {}
        
        for aa in range(divider):
            self.spaces[aa] = {}
      
# ------------------------------------------------------------------------
# Flood fill. Star formation, clockwise. 
# Synonyms -> L-left R-right A-above B-below
#
# Scanning order:
#
#  A, AR, R, BR, B, BL, L, AL

def flood(xxx, yyy, param):
        
    # Terminate this branch
    if xxx <= 0 or yyy <= 0 or xxx >= param.ddd-1 or yyy >= param.ddd-1:
        return
     
    # Stop overly zealous recursion   
    param.cnt += 1; param.depth += 1
    if  param.depth > 900:
        print "Warn: Backed out of extensive recursion. Depth", param.depth, "Count", param.cnt
        return
        
    # To observe in action:
    if param.inval:
        if param.cnt % param.breath == 0:
            param.inval(param); usleep(.01)
    
    diff = imgrec.diffcol(param.mark, param.darr[xxx][yyy-1]) 
    #fframe(xxx, yyy-1, param.hstep, param.vstep, 0xffff0000)
    #print "A", diff
    if diff[1] < param.tresh:
        if not is_done(xxx, yyy-1, param):
            flood(xxx, yyy-1, param)

    diff = imgrec.diffcol(param.mark, param.darr[xxx+1][yyy-1]) 
    #fframe(xxx+1, yyy-1, param.hstep, param.vstep, 0xffff8000)
    #print "AR", diff
    if diff[1] < param.tresh:
        if not is_done(xxx+1, yyy-1, param):
            flood(xxx+1, yyy-1, param) 
        
    diff = imgrec.diffcol(param.mark, param.darr[xxx+1][yyy]) 
    #fframe(xxx+1, yyy, param.hstep, param.vstep, 0xffff8080)
    #print "R", diff
    if diff[1] < param.tresh:
        if not is_done(xxx+1, yyy, param):
            flood(xxx+1, yyy, param)
      
    diff = imgrec.diffcol(param.mark, param.darr[xxx][yyy+1]) 
    #fframe(xxx, yyy+1, param.hstep, param.vstep, 0xffffffFF)
    #print "B", diff
    if diff[1] < param.tresh:
        if not is_done(xxx, yyy+1, param):
            flood(xxx, yyy+1, param)
    
    diff = imgrec.diffcol(param.mark, param.darr[xxx-1][yyy]) 
    #fframe(xxx-1, yyy, param.hstep, param.vstep, 0xffff8080)
    #print "L", diff
    if diff[1] < param.tresh:
        if not is_done(xxx-1, yyy, param):
            flood(xxx-1, yyy, param)

    param.depth -= 1
   
# Mark a cell done, return True if visited before

def is_done(xxx, yyy, param):

    aa = 0
    try:
        aa = param.spaces[xxx, yyy]
    except:
        #fframe(xxx, yyy, param.hstep, param.vstep, 0xffff8000)
        param.spaces[xxx, yyy] = 1
        return False 
        
    if aa == 1:
        return True 
    else: 
        try:
            #fframe(xxx, yyy, param.hstep, param.vstep, 0xffff8000)
            param.spaces[xxx, yyy] = 1
        except:
            pass
        return False     
        

# Flood fill. Inital attempt.

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
        print "right", hex(mark), hex(darr[aa][yyy]), hex(diff[0]), diff[1]
    
    # Walk left
    for aa in range(xxx-1, 0, -1):
        diff = imgrec.diffcol(mark, darr[aa][yyy]) 
        if diff[1] > tresh:
            break;
        print "left", hex(mark), hex(darr[aa][yyy]), hex(diff[0]), diff[1]
        imgrec.frame(aa * hstep, yyy * vstep, 
                    (aa + 1) * hstep, (yyy + 1) * vstep, 0xff008800)
    
    # Walk up
    for aa in range(yyy-1, 0, -1):
        diff = imgrec.diffcol(mark, darr[xxx][aa])
        if diff[1] > tresh:
            break;
        imgrec.frame(xxx * hstep, aa * vstep, 
                    (xxx + 1) * hstep, (aa + 1) * vstep, 0xff800000)
        print "up", hex(mark), hex(darr[xxx][aa]), hex(diff[0]), diff[1]
  
    # Walk down
    for aa in range(yyy+1, hhh):
        diff = imgrec.diffcol(mark, darr[xxx][aa])
        if diff[1] > tresh:
            break;
        imgrec.frame(xxx * hstep, aa * vstep, 
                    (xxx + 1) * hstep, (aa + 1) * vstep, 0xff000080)
        print "down", hex(mark), hex(darr[xxx][aa]), hex(diff[0]), diff[1]
    
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
      






