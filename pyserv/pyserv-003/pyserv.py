#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time
import tarfile, subprocess, commands, struct, gobject
import socket, threading, SocketServer, traceback, syslog

#import gobject, pango, gst
#import warnings
#warnings.simplefilter("ignore")
#import gtk
#warnings.simplefilter("default")
    
create_proj = False             
install_proj = False            
list_proj = False             
verbose = False  
quiet  = False  
force = False 
version = 1.0
pgdebug = 0

# Globals
mydata = {}
mystate = {}
myhandlers = {}
server = None

def put_debug(xstr):
    try:
        if os.isatty(sys.stdout.fileno()):
            print xstr
        else:
            syslog.syslog(xstr)
    except:
        print "Failed on debug promt"
        print sys.exc_info()

# ------------------------------------------------------------------------

def put_exception(xstr):

    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b)
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt: 
                cumm += "  File: " + aa[0] + " Line: " + \
                     str(aa[1]) + " Context: " + aa[2] + " " + aa[3]
        except:
            print "Could not print trace stack. ", sys.exc_info()
            
    put_debug(cumm)    
    #syslog.syslog("%s %s %s" % (xstr, a, b))

# Walk thru the server (chunk) state machine 
# 1. Get length
# 2. Get data
# 3. Reply
# Set alarm after every transaction, so timeout is monitored

class DataHandler():
    
    def __init__(self, par):
        #print  "DataHandler __init__"
        self.src = None; self.tout = None
        
    def handler_timeout(self):
        self.tout.cancel()
        put_debug("handler_timeout %s" % self.name )
        #print self.par.client_address, self.par.server.socket
        # Force closing connection
        self.par.request.send("Timeout occured, disconnecting.\n")
        self.par.request.shutdown(socket.SHUT_RDWR)
    
    def putdata(self, response):
        if self.tout: self.tout.cancel()
        self.tout = threading.Timer(2, self.handler_timeout)
        self.tout.start()
        self.par.request.send(response)
          
    def getdata(self, amount):
        if self.tout: self.tout.cancel()
        self.tout = threading.Timer(2, self.handler_timeout)
        self.tout.start()
        return self.par.request.recv(amount)

    def got_data(self, data):
        if pgdebug > 5:
            put_debug( "got data '" + data + "'")
        #response = "%s: %s" % (name, str.upper(data))
        response = "%s" % str.upper(data)
        if pgdebug > 5:
            put_debug("Replied with '" + response + "'")
        self.putdata(response)

    def handle(self, par):    
        self.par = par
        cur_thread = threading.currentThread()
        self.name = cur_thread.getName()
        
        state = 0; xlen = 0; data = ""; ldata = ""
        
        #print "*** Handling connection on", self.name, \
        #    "From", self.par.client_address
        
        while 1:
            if state == 0:
                xdata = self.getdata(2-len(ldata))
                if len(xdata) == 0: break
                ldata += xdata    
                if len(ldata) == 2:
                    state = 1; 
                    xlen = struct.unpack("!h", ldata)[0]
                    #print "got len =", xlen
                
            elif state == 1:
                data2 = self.getdata(xlen-len(data))
                if len(data2) == 0:
                    break
                data += data2
                if len(data) == xlen:
                    state = 3
            
            elif state == 3:
                self.got_data(data)    
                state = 0
            else:
                print "Unkown state"
    
        if self.tout: self.tout.cancel()
        
        return False
        
# ------------------------------------------------------------------------

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, a1, a2, a3):
        self.a2 = a2
        #print a1 #print a2 #print a3
        SocketServer.BaseRequestHandler.__init__(self, a1, a2, a3)
        #print  SocketServer
        
    def setup(self):
        cur_thread = threading.currentThread()
        self.name = cur_thread.getName()
        if verbose:
            print "Connection from ", self.a2, "as", self.name
            
        mydata[self.name] = 0
        mystate[self.name] = 0
        self.datahandler = DataHandler(self)
        myhandlers[self.name] = self.datahandler
        
    def handle(self):
        try:
            while 1:
                ret = self.datahandler.handle(self)
                if not ret: break
        except:
            print sys.exc_info()
        
    def finish(self):
        del mydata[self.name]
        del mystate[self.name]
        del myhandlers[self.name]
        if verbose:
            print "Closed socket on", self.name
    
# ------------------------------------------------------------------------
# Override stock methods

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    
    def stop(self):
        self._BaseServer__shutdown_request = True
        if verbose:
            print "Stop called"
        pass
        
# ------------------------------------------------------------------------

def help():

    print
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options]"
    print
    print "Options:    -d level  - Debug level 0-10"
    print "            -v        - Verbose"
    print "            -q        - Quiet"
    print "            -h        - Help"
    print
    sys.exit(0)

# ------------------------------------------------------------------------
        
def terminate(arg1, arg2):

    global mydata, mystate
    if mydata != {}:
        print "Dumping connection info:"
        print mydata, mystate
        
    server.stop()
    
    if not quiet:
        print "Terminated pyserv.py."
    sys.exit(2)

# ------------------------------------------------------------------------

if __name__ == '__main__':

    opts = []; args = []

    syslog.openlog("pyserv.py")
    
    '''syslog.openlog("pyserv", \
                syslog.LOG_PID | syslog.LOG_CONS | \
                    syslog.LOG_NDELAY | syslog.LOG_NOWAIT | \
                    syslog.LOG_PERROR)
    syslog.setlogmask( syslog.LOG_EMERG | syslog.LOG_ALERT | \
                    syslog.LOG_CRIT | syslog.LOG_ERR | \
                    syslog.LOG_WARNING | syslog.LOG_NOTICE | \
                    syslog.LOG_INFO | syslog.LOG_DEBUG)
    '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:qhvVf")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
                if verbose:
                    print "Debug level:", pgdebug
                if pgdebug > 10 or pgdebug < 0:
                    raise(ValueError, \
                        "Debug range needs to be between 0-10")
            except:
                put_exception("Command line error:")
                sys.exit(3)

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True            
        if aa[0] == "-q": quiet = True            
        if aa[0] == "-f": force = True            
        if aa[0] == "-V": 
            print os.path.basename(sys.argv[0]), "Version", version
            sys.exit(0)
                
    # Set termination handlers
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    
    # Port 0 would mean to select an arbitrary unused port
    HOST, PORT = "localhost", 9999
    #HOST, PORT = "192.168.1.13", 9999
            
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.allow_reuse_address = True

    # Start a thread with the server -- that thread will then start one
    # or more threads for each request
    server_thread = threading.Thread(target=server.serve_forever)
    
    # Exit the server thread when the main thread terminates
    server_thread.setDaemon(True)
    server_thread.start()

    if not quiet:    
        print "Server running:", server.server_address
 
    # Block       
    server.serve_forever()



