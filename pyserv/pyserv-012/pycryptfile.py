#!/usr/bin/env python

import os, getpass, sys, base64 #, crypt, pwd, spwd, 

import bluepy.bluepy
import  pyserv.pycrypt, pyserv.pyclisup

# ------------------------------------------------------------------------
# Functions from command line

def phelp():

    bn = os.path.basename(sys.argv[0])
    print 
    print "Usage: " + bn + " [-e] [-d] [options] fromfile tofile"
    print "Specify -e for encrypt -d decrypt"
    print "Options:    -p pass   - pass to use"
    print "            -v        - Verbose"
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
    ["e",   "encrypt",  0,      None],      \
    ["d",   "decrypt",  0,      None],      \
    ["q",   "quiet",    0,      None],      \
    ["t",   "test",     "x",    None],      \
    ["f",   "force",    0,      None],      \
    ["V",   None,       None,   pversion],  \
    ["h",   None,       None,   phelp]      \
    
conf = pyserv.pyclisup.Config(optarr)

# ------------------------------------------------------------------------
if __name__ == '__main__':

    args = conf.comline(sys.argv[1:])
    if len(args) < 2:
        phelp()
    
    if conf.encrypt == 0 and conf.decrypt == 0:
        print "Must specify one of -e or -d (encrypt / decrypt) options"
        sys.exit(1)

    if conf.encrypt == 1 and conf.decrypt == 1:
        print "Must specify ONE of -e -d  (encrypt / decrypt) options"
        sys.exit(1)
        
    if args[0] == args[1]:
        print "Must use different output file name: '" + args[1] + "'"
        sys.exit(1)
    
    if not os.path.isfile(args[0]):
        print "No such file", "'" + args[0] + "'"
        sys.exit(2)

    if os.path.isfile(args[1]):
        if not conf.force:
            print "Output exists, use -f to overwrite ", "'" + args[1] + "'"
            sys.exit(2)
    
    if conf.passwd == "":
        if conf.verbose:
            print \
        "Prompting for pass. Make sure you make a note of the pass, as the data\n"\
        "is not recoverable without it."
        conf.passwd = getpass.getpass("Enter password for file: ")
        #print  conf.passwd

    if conf.verbose:
        if conf.encrypt:
            print "Encrypting file:", "'" + args[0] + "'",\
                 "into:", "'" + args[1] + "'", " ... ",
        if conf.decrypt:
            print "Decrypting file:", "'" + args[0] + "'",\
                "into:", "'" + args[1] + "'", " ... ",
        sys.stdout.flush()
        
    try:
        fh1 = open(args[0], "r")
    except:
        print "Cannot open file:", sys.exc_info()[1]
        sys.exit(3)
    
    try:
        fh2 = open(args[1], "w")
    except:
        print "Cannot create file:", sys.exc_info()[1]
        sys.exit(4)

    bytes = 0
    while 1:
        buff = fh1.read(1024)
        if len(buff) == 0:
            break
        bytes += len(buff)
        if conf.encrypt:
            buff2 = pyserv.pycrypt.xencrypt(buff, conf.passwd)
        if conf.decrypt:
            buff2 = pyserv.pycrypt.xdecrypt(buff, conf.passwd)
            
        try:
            fh2.write(buff2)
        except:
            print "Cannot write", sys.exc_info()[1]
            break
             
    fh1.close(); fh2.close()
              
    if conf.verbose:
        print "%d bytes processed." % bytes   




