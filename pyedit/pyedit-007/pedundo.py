#!/usr/bin/env python

# Undo / redo handler

# To use the undo, we have four operations.
#
# 1.) Line modified - MODIFIED  (crude implementation, you may improve it)
# 2.) Line added    - ADDED
# 3.) Line deleted  - DELETED
# 4.) No change     - NOOP
#
# In order to group operations, (like multi line cut) set the 
# CONTFLAG by OR - ing it in. To signal the end of group do 
# a NOOP without the CONTFLAG. Redo is generated automatcally.
# Because of redo, provide the old buffer on delete as well. 
#
# A typical call to the undo looks like this:
# self2.undoarr.append((xidx, yidx, MODIFIED + CONTFLAG, self2.text[cnt]))            
#   Args: cursor x, cursor y, opcode, original content

# Op codes:
(NOOP, MODIFIED, ADDED, DELETED) = range(4)
#print "(NOOP, MODIFIED, ADDED, DELETED)", NOOP, MODIFIED, ADDED, DELETED

CONTFLAG = 0x80                         # Continuation flag
CONTMASK = CONTFLAG - 1                 # Cont flag mask
#print hex(CONTFLAG), hex(CONTMASK)

# The undo stack limit pops from the beginning, so the oldest transaction
# is discarded. The stack persists across sessions, so we limit it. 
# Note that the stack size is the number of undo transactions saved,
# including NOOP-s

# Development test (make it small, make it often)
#MAX_UNDO = 80                  # TEST               

# This is a generous limit, adjust to taste.
MAX_UNDO = 10000                # REAL - Sizeof undo stack 

# ------------------------------------------------------------------------
# Limit the size of undo    

def     limit_undo(self2):

    xlen = len(self2.undoarr)
    if xlen == 0: return
    if xlen  <  MAX_UNDO: return
    #print "limiting undo size from", len(self2.undoarr)        
    for aa in range(MAX_UNDO / 5):
        try:
            del (self2.undoarr[0])
        except:
            pass

    # Look to next boundary
    while True:
        xx, yy, mode, line = self2.undoarr[0]
        if not (mode & CONTMASK): break
        xlen = len(self2.undoarr)
        if  xlen == 0: break      
        #print "boundary del at", xlen
        del (self2.undoarr[0])
    
    #print "limited undo size to", len(self2.undoarr)
        
# ------------------------------------------------------------------------
# The undo information is maintenaned in the array of tuples 'undoarr'.
# We save current location (x and y), transaction type and the old line.
# The undo stack and redo stack are filled in a complimentarily fashion.
# (walk undo - fill redo -- walk redo - fill undo)
# Because the way they are designed, they can fill each other

def undo(self2):

    xlen = len(self2.undoarr)
    if xlen == 0:
        self2.mained.update_statusbar("Nothing to undo.")                     
        return

    while True:
        xlen = len(self2.undoarr)
        if xlen == 0: break

        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        xx, yy, mode, line = self2.undoarr[xlen-1]
        mode2 = mode & CONTMASK
        #print "undo", mode, xx, yy, "line '", line, "'"
        if mode2 == MODIFIED:                   # Line change
            self2.redoarr.append((xx, yy, mode, self2.text[yy]))
            self2.text[yy] = line
            self2.gotoxy(xx, yy)
        elif mode2 == ADDED:                    # Addition - delete
            self2.redoarr.append((xx, yy, mode, self2.text[yy]))
            del (self2.text[yy])
        elif mode2 == DELETED:                  # Deletion - recover
            self2.redoarr.append((xidx, yidx, mode, self2.text[yy]))
            text = self2.text[:yy]
            text.append(line)
            text += self2.text[yy:]
            self2.text = text                                        
        elif mode2 == NOOP:                     # Place Holder
            pass
        else:
            # Just to confirm 
            print "warninig: undo - invalid mode"
            pass

        del (self2.undoarr[xlen-1])
        # Continue if cont flag is on
        if mode & CONTFLAG:  pass
        else: break

    self2.invalidate()
    
    print self2.initial_undo_size, len(self2.undoarr)
        
    if self2.initial_undo_size == len(self2.undoarr):
        self2.set_changed(False)
    else:
        self2.set_changed(True)

    self2.invalidate()                                                
    self2.mained.update_statusbar("Undo %d done." % xlen)                     

# ------------------------------------------------------------------------

def redo(self2):    

    xlen = len(self2.redoarr)
    if xlen == 0:
        self2.mained.update_statusbar("Nothing to redo.")                     
        return

    # Reverese actions till first non contflag
    revredo = [];
    while True:
        xarridx = len(self2.redoarr) 
        if xarridx == 0 : break        
        xx, yy, mode, line = self2.redoarr[xarridx - 1]
        #print "redo", mode, "line '", line, "'"
        revredo.append((xx, yy, mode, line))
        del (self2.redoarr[xarridx - 1]) 

        mode2 = 0
        if len(self2.redoarr):
            xx2, yy2, mode2, line2 = self2.redoarr[len(self2.redoarr)-1]
        if mode2 & CONTFLAG:    pass                
        else:                   break    

    # Just for show
    #for xx, yy, mode, line in revredo:
    #    print "rev", mode, xx, yy, "line '", line, "'"
  
    while True:
        xlen = len(revredo)
        if xlen == 0: break
        xidx = self2.caret[0] + self2.xpos; 
        yidx = self2.caret[1] + self2.ypos 
        xx, yy, mode, line = revredo[xlen-1]
        mode2 = mode & CONTMASK
        #print "redo", mode2, xx, yy, "line '", line, "'"
        if mode2 == MODIFIED:                   # Line change
            self2.undoarr.append((xx, yy, mode, self2.text[yy]))
            self2.text[yy] = line
            self2.gotoxy(xx, yy)
        elif mode2 == ADDED:                 # Redo Addition
            self2.undoarr.append((xx, yy, mode, self2.text[yy]))
            text = self2.text[:yy]
            text.append(line)
            text += self2.text[yy:]
            self2.text = text
            self2.gotoxy(xx, yy)         
        elif mode2 == DELETED:                 # Redo Deletion
            self2.undoarr.append((xx, yy, mode, self2.text[yy]))
            del (self2.text[yy])
        elif mode2 == NOOP:                     # Place Holder
            pass
        else:
            # Just to confirm 
            print "warninig: redo - invalid mode"
            pass 

        del (revredo[xlen-1])

        # Continue if cont flag is on
        if mode & CONTFLAG:  pass
        else: break

    # Not true, needs to account for old changes ... removed
    #if self2.initial_redo_size == len(self2.redoarr):
    #    self2.set_changed(False)
    #else:

    self2.invalidate()
    self2.set_changed(True)
    self2.mained.update_statusbar("Redo %d done." % xlen)                     
  
# EOF
