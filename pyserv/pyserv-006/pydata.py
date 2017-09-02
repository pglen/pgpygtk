#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time, struct 
import socket, threading, SocketServer, traceback, syslog

# Walk thru the server (chunk) state machine 
# Chunk is our special buffer (short [16 bit])len + (str)message
# 1. Get length
# 2. Get data
# 3. Reply
# Set alarm after every transaction, so timeout is monitored
# Transmission needs to be 16 bit clean

pgdebug = 0

class DataHandler():
    
    def __init__(self):
        #print  "DataHandler __init__"
        self.src = None; self.tout = None
        self.timeout = 5
        
    def handler_timeout(self):
        self.tout.cancel()
        if pgdebug > 0:
            print "handler_timeout %s" % self.name 
            #print self.par.client_address, self.par.server.socket
        # Force closing connection
        self.par.request.send("Timeout occured, disconnecting.\n")
        self.par.request.shutdown(socket.SHUT_RDWR)
    
    def putdata(self, response):
        if self.tout: self.tout.cancel()
        self.tout = threading.Timer(self.timeout, self.handler_timeout)
        self.tout.start()
        # Send out our special buffer (short)len + (str)message
        strx = struct.pack("!h", len(response)) + response
        self.par.request.send(strx)
          
    def getdata(self, amount):
        if self.tout: self.tout.cancel()
        self.tout = threading.Timer(self.timeout, self.handler_timeout)
        self.tout.start()
        return self.par.request.recv(amount)

    # Where the outside stimulus comes in ...
    # State 0 - initial => State 1 - len arrived => State 2 data coming 
    # Receive our special buffer (short)len + (str)message
    
    def handle_one(self, par):    
        self.par = par
        cur_thread = threading.currentThread()
        self.name = cur_thread.getName()
        state = 0; xlen = 0; data = ""; ldata = ""
        while 1:
            if state == 0:
                xdata = self.getdata(max(2-len(ldata), 0))
                if len(xdata) == 0: break
                ldata += xdata    
                if len(ldata) == 2:
                    state = 1; 
                    xlen = struct.unpack("!h", ldata)[0]
                    if pgdebug > 7:
                        print "got len =", xlen
            elif state == 1:
                data2 = self.getdata(max(xlen-len(data), 0))
                if len(data2) == 0:
                    break
                data += data2
                if pgdebug > 7:
                    print "got data, len =", len(data2)
                if len(data) == xlen:
                    state = 3
            elif state == 3:
                # Done, return buffer
                state = 0
                break
            else:
                if pgdebug > 0:
                    print "Unkown state"
        if self.tout: self.tout.cancel()
        return data

