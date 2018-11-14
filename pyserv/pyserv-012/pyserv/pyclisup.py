#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random

import pydata, pyserv, pycrypt
#import bluepy import bluepy
                            
# -----------------------------------------------------------------------
# Globals 

myhandler = None; mydathand = None
verbose = False
debug = False

random.seed()

# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the class      

class Config:

    def __init__(self, optarr):
        self.optarr = optarr

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            optletters += aa[0]
        #print optletters    
        # Create defaults:
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        except getopt.GetoptError, err:
            print "Invalid option(s) on command line:", err
            return ()
            
        #print "opts", opts, "args", args
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print "match", aa, self.optarr[bb]
                    if len(self.optarr[bb][0]) > 1:
                        #print "arg", self.optarr[bb][1], aa[1]
                        if self.optarr[bb][2] != None: 
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print "set", self.optarr[bb][1], self.optarr[bb][2]
                        if self.optarr[bb][2] != None: 
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print "call", self.optarr[bb][3]
                        if self.optarr[bb][3] != None: 
                            self.optarr[bb][3]()
        return args
    
# ------------------------------------------------------------------------
# Send out our special buffer (short)len + (str)message

def sendx(sock, message):
    strx = struct.pack("!h", len(message)) + message
    sock.send(strx)

# ------------------------------------------------------------------------
# Set encryption key. New key returned. Raises ValuError.

def set_key(s1, newkey, oldkey):
    resp = client(s1, "ekey " + newkey, oldkey)
    tmp = resp.split()
    if len(tmp) < 2 or tmp[0] != "OK":
        #print "Cannot set new key", resp
        raise(ValueError, "Cannot set new key. ")
    return newkey

# ------------------------------------------------------------------------
# Set encryption key from named key. Raises ValuError.
# Make sure you fill in key_val from local key cache.

def set_xkey(s1, newkey, oldkey):
    resp = client(s1, "xkey " + newkey, oldkey)
    tmp = resp.split()
    if len(tmp) < 2 or tmp[0] != "OK":
        #print "Cannot set new key", resp
        raise(ValueError, "Cannot set new named key.")

# ------------------------------------------------------------------------
# Send file. Return True for success.

def sendfile(s1, fname, toname,  key = ""):

    if verbose:
        print "Sending ", fname, "to", toname
    response = ""
    try:    
        flen = os.stat(fname)[stat.ST_SIZE]
        fh = open(fname)
    except:
        print "Cannot open file", sys.exc_info()[1]
        return
    resp = client(s1, "file " + toname, key)
    tmp = resp.split()
    if len(tmp) < 2 or tmp[0] != "OK":
        print "Cannot send file command", resp
        return 
    resp = client(s1, "data " + str(flen), key)
    tmp = resp.split()
    if len(tmp) < 2 or tmp[0] != "OK":
        print "Cannot send data command", resp
        return 
    while 1:
        buff = fh.read(pyserv.pyservsup.buffsize)
        if len(buff) == 0:
            break
        if key != "":
            buff = bluepy.bluepy.encrypt(buff, key)
        sendx(s1, buff)
    response = myhandler.handle_one(mydathand)
    if key != "":
        response = bluepy.bluepy.decrypt(response, key)
    if verbose:
        print "Received: '%s'" % response
    return True
    
# ------------------------------------------------------------------------
# Receive File. Return True for success.

def getfile(s1, fname, toname, key = ""):

    if verbose:
        print "getting ", fname, "to", toname
    try:  
        fh = open(toname, "w")         
    except:
        print "Cannot create local file: '" + toname + "'"
        return
    response = client(s1, "fget " + fname, key)
    aaa = response.split(" ")
    if len(aaa) < 2:
        fh.close()
        if verbose:
            print "Invalid response, server said: ", response
        return 
    if aaa[0] == "ERR":
        fh.close()
        if verbose:
            print "Server said: ", response
        return 
    mylen = 0; flen = int(aaa[1])
    #print "getting", flen,
    while mylen < flen:
        need = min(pyserv.pyservsup.buffsize,  flen - mylen)
        need = max(need, 0)
        data = myhandler.handle_one(mydathand)
        if key != "":
            data = bluepy.bluepy.decrypt(data, key)
        try:
            fh.write(data)
        except:
            if verbose:
                print "Cannot write to local file: '" + toname + "'"
            fh.close()
            return
        mylen += len(data)
        # Faulty transport, abort
        if len(data) == 0:
            break
    fh.close()
    if verbose:
        print "Got data, len =", mylen
    if  mylen != flen:
        if verbose:
            print "Faulty amount of data arrived"
        return
    return True

# ------------------------------------------------------------------------
# Ping Pong function with encryption.

def client(sock, message, key = "", rand = True):
    global mydathand, myhandler
    if verbose:
        print "Sending: '%s'" % message
    if key != "":
        if rand:
            message = message + " " * random.randint(0, 20)
        message = bluepy.bluepy.encrypt(message, key)
    sendx(sock, message)
    if verbose and key != "":
        print "   put: '%s'" % base64.b64encode(message),
    response = myhandler.handle_one(mydathand)
    if verbose and key != "":
        print "get: '%s'" % base64.b64encode(response)
    if key != "":
        #response = pycrypt.xdecrypt(response, key)
        response = bluepy.bluepy.decrypt(response, key)
    if verbose:
        print "Rec: '%s'" % response
    return response

def init_handler(sock):
    global mydathand, myhandler
    mydathand  = pydata.xHandler(sock)
    myhandler  = pydata.DataHandler()
    




