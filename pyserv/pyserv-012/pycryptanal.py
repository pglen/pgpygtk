#!/usr/bin/env python

import os, getpass, sys, base64, getpass #, crypt, pwd, spwd, 
import  pyserv.pycrypt, pyserv.pyclisup

# ------------------------------------------------------------------------
# Functions from command line

def phelp():

    bn = os.path.basename(sys.argv[0])
    print 
    print "Usage: " + bn + " [options] filename"
    print 
    print "Options:    -v        - Verbose"
    print "            -V        - Print version"
    print "            -q        - Quiet"
    print "            -h        - Help"
    print  
    sys.exit(0)

def pversion():
    print os.path.basename(sys.argv[0]), "Version", version
    sys.exit(0)
 
    # option, var_name, initial_val, function
optarr = \
    ["p:",  "passwd",     "",   None],      \
    ["v",   "verbose",  0,      None],      \
    ["d",   "dump",     0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["f",   "force",    0,      None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \
    
conf = pyserv.pyclisup.Config(optarr)

def _cmp(a1, a2):
    #print "vals", a1, a2
    return cmp(a1[1], a2[1])
    
# ------------------------------------------------------------------------
if __name__ == '__main__':

    args = conf.comline(sys.argv[1:])
    if len(args) < 1:
        phelp()
        
    if not os.path.isfile(args[0]):
        print "No such file", "'" + args[0] + "'"
        sys.exit(2)
    
    if conf.verbose:
        print "Analizing file:", "'" + args[0] + "'"
        
    try:
        fh1 = open(args[0], "r")
    except:
        print "Cannot open file:", sys.exc_info()[1]
        sys.exit(3)
    
    bytes = 0; ddd = {}
    while 1:
        buff = fh1.read(1024)
        if len(buff) == 0:
            break
        for aa in buff:
            #print ord(aa),
            try:
                ddd[ord(aa)] += 1
            except:
                ddd[ord(aa)] = 1
        bytes += len(buff)
    fh1.close();
    
    iii = ddd.items(); iiii = [] 
    #iii.sort(_cmp, None, True)          
    # Reverse order
    for aa in iii:
        iiii.append((aa[1], aa[0]))
    iiii.sort(None, None, True)    
    #print iiii
    
    if conf.dump:
        cnt = 0
        for aa in iiii:
            chh = aa[1]
            if chh == ord("\r") or chh == ord("\n") or \
                    chh >= 0x80 or chh <= 0xf:
                chh = " "
            print "0x%-3x '%c' %5d " % (aa[1], chh, aa[0]),
            cnt += 1
            if cnt and cnt % 4 == 0:
                print 
        print 
        
    median = 0
    for aa in iiii:
        median += aa[0]
    median /= len(iiii)
    xxx = max(iiii); mmm = min(iiii)           
    print "Median:", median, "Max",  xxx, "Min", mmm           
    deviate = 0L
    for aa in iiii:
        deviate += float(aa[0]- median)
    deviate /= len(iiii)
    deviate = int(deviate * 100)
    print "Standard deviation:", str(deviate) + "%"
    
    rrr =  float(xxx[0]) / float(mmm[0])
    print "MaxMin ratio: %.0f%%" % rrr
    
    deviate = 0L
    try:
        for aa in iiii:
            deviate += abs(float(aa[0]) / float(median))
    except:
        pass
                
    print "Compound deviation: %.0f%%" % deviate
    
    if conf.verbose:
        print "%d bytes processed." % bytes   






