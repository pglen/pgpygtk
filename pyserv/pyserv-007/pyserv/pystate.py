#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time, syslog, stat

import pyservsup

# Globals

version = 1.0

# Ping pong state machine

# 1.) States

initial     = 0
auth_user   = 1
auth_pass   = 2
in_idle     = 3
got_fname   = 4
in_trans    = 5
got_file    = 6

# The commands in this state are allowed always
all_in       = 100
# The commands in this state are allowed in all states after auth
auth_in      = 110

# ------------------------------------------------------------------------
# State transition and action functions

def get_lsd_func(self, strx):
    dname = ""; sss = ""
    try:
       dname = strx[1]; 
    except:
       pass
    dname2 = self.resp.cwd + "/" + self.resp.dir + "/" + dname
    dname2 = pyservsup.dirclean(dname2)
    try:
        ddd = os.listdir(dname2)
        for aa in ddd:
            if stat.S_ISDIR(os.stat(aa)[stat.ST_MODE]):
                # Escape spaces
                sss += pyservsup.escape(aa) + " "
        response = "OK " + sss
    except:
        #pyservsup.put_exception("lsd")
        response = "ERR " + str(sys.exc_info()[1] )
    self.resp.datahandler.putdata(response)
    
def get_ls_func(self, strx):
    dname = ""; sss = ""
    try:
        dname = pyservsup.unescape(strx[1]); 
    except:
        pass   
    dname2 = self.resp.cwd + "/" + self.resp.dir + "/" + dname
    dname2 = pyservsup.dirclean(dname2)
    try:
        ddd = os.listdir(dname2)
        for aa in ddd:
            try:
                aaa = dname2 + "/" + aa
                if not stat.S_ISDIR(os.stat(aaa)[stat.ST_MODE]):
                    # Escape spaces
                    sss += pyservsup.escape(aa) + " "
            except:
                print "Cannot stat ", aaa
                
        response = "OK " + sss
    except:
        #pyservsup.put_exception("ls ")
        response = "ERR No such directory"
    self.resp.datahandler.putdata(response)
    
def get_fget_func(self, strx):

    dname = ""
    if len(strx) == 1:
        response = "ERR Must specify file name"
        self.resp.datahandler.putdata(response)
        return
        
    dname = pyservsup.unescape(strx[1]); 
    dname2 = self.resp.cwd + "/" + self.resp.dir + "/" + dname
    dname2 = pyservsup.dirclean(dname2)
    flen = 0
    try:    
        flen = os.stat(dname2)[stat.ST_SIZE]
        fh = open(dname2)
    except:
        response = "ERR Cannot open file '" + dname + "'"
        self.resp.datahandler.putdata(response)
        return
    response = "OK " + str(flen)
    self.resp.datahandler.putdata(response)
    
    # Loop, break when file end or transmission error
    while 1:
        buff = fh.read(pyservsup.buffsize)
        if len(buff) == 0:
            break
        ret = self.resp.datahandler.putdata(buff)
        if ret == 0:
            break

    xstr = "Sent file: '" + dname + \
                "' " + str(flen) + " bytes"
    print xstr
    syslog.syslog(xstr)

def get_pwd_func(self, strx):
    dname2 = self.resp.dir 
    dname2 = pyservsup.dirclean(dname2)
    if dname2 == "": dname2 = "/"
    response = "OK " +  dname2
    self.resp.datahandler.putdata(response)
    
def get_ver_func(self, strx):
    response = "OK Version " + str(version)
    self.resp.datahandler.putdata(response)

def get_cd_func(self, strx):
    org = self.resp.dir
    try:
        dname = pyservsup.unescape(strx[1]); 
        if dname == "..":
            self.resp.dir = pyservsup.chup(self.resp.dir)
        else:     
            self.resp.dir += "/" + dname
            
        self.resp.dir = pyservsup.dirclean(self.resp.dir)
        dname2 = self.resp.cwd + "/" + self.resp.dir 
        dname2 = pyservsup.dirclean(dname2)
        if os.path.isdir(dname2):
            response = "OK " + self.resp.dir
        else:
            # Back out
            self.resp.dir = org
            response = "ERR Directory does not exist" 
    except:
        pyservsup.put_exception("cd")
        response = "ERR Must specify directory name"
    self.resp.datahandler.putdata(response)
  
def get_stat_func(self, strx):
    fname = ""; aaa = " "
    try:
        fname = strx[1]; sss = os.stat(strx[1])
        for aa in sss:
            aaa += str(aa) + " "
        response = "OK " + fname + aaa
    except OSError:
        print sys.exc_info()
        response = "ERR " + str(sys.exc_info()[1] )
    except:
        response = "ERR Must specify file name"
    self.resp.datahandler.putdata(response)
  
def get_user_func(self, strx):
    if len(strx) == 1:
        self.resp.datahandler.putdata("ERR must specify user name")
        return
    self.resp.user = strx[1]
    self.resp.datahandler.putdata("OK Enter pass for '" + self.resp.user + "'")
    
def get_pass_func(self, strx):
    stry = "Logon  '" + self.resp.user + "' " + \
                str(self.resp.client_address) 
    print stry        
    syslog.syslog(stry)
    self.resp.datahandler.putdata("OK")

def get_fname_func(self, strx):
    try:
        self.resp.fname = strx[1]
        response = "OK Send file '" + self.resp.fname + "'"
    except:
        response = "ERR Must specify file name"
    self.resp.datahandler.putdata(response)

def get_data_func(self, strx):
    if self.resp.fname == "":
        response = "ERR No filename for data"
        self.resp.datahandler.putdata(response)
        return
    try:
       self.resp.dlen = int(strx[1])
    except:
        response = "ERR Must specify file name"
        self.resp.datahandler.putdata(response)
        return
        
    self.resp.datahandler.putdata("OK Send data")
    try:  
        fh = open(self.resp.fname, "w")         
    except:
        response = "ERR Cannot save file on server"
        self.resp.datahandler.putdata(response)
        return
    
    # Consume buffers until we got all
    mylen = 0
    while mylen < self.resp.dlen:
        need = min(pyservsup.buffsize,  self.resp.dlen - mylen)
        need = max(need, 0)
        data = self.resp.datahandler.handle_one(self.resp)
        try:
            fh.write(data)
        except:
            response = "ERR Cannot write data on server"
            self.resp.datahandler.putdata(response)
            return
        mylen += len(data)
        
        # Faulty transport, abort
        if len(data) == 0:
            break
    fh.close()
    
    if  mylen != self.resp.dlen:
        response = "ERR faulty amount of data arrived"
        self.resp.datahandler.putdata(response)
        return

    xstr = "Received file: '" + self.resp.fname + \
                "' " + str(self.resp.dlen) + " bytes"
    print xstr
    syslog.syslog(xstr)

    self.resp.datahandler.putdata("OK Got data")
            
def get_help_func(self, strx):
    #print "get_help_func", strx
    hstr = "OK "
    if len(strx) == 1:
        for aa in state_table:
            hstr += aa[0] + " "
    else:
        for aa in state_table:
            if strx[1] == aa[0]:
                hstr = "OK " + aa[4]
                break
        if hstr == "OK ":
            hstr = "ERR no help for command '" + strx[1] + "'"
            
    self.resp.datahandler.putdata(hstr)
    
# Also stop timeouts
def get_exit_func(self, strx):
    #print "get_exit_func", strx
    self.resp.datahandler.putdata("OK Bye")
    
    # Cancel **after** sending bye
    if self.resp.datahandler.tout: 
        self.resp.datahandler.tout.cancel()
    return True

def get_tout_func(self, strx):
    print "get_tout_func", strx
    if self.resp.datahandler.tout: 
        self.resp.datahandler.tout.cancel()
    self.resp.datahandler.putdata("OK timeout reset")
    return True

# ------------------------------------------------------------------------
# Help stings
user_help = "Usage: user logon_name"
pass_help = "Usage: pass logon_pass"
file_help = "Usage: file fname -- Specify name for upload"
fget_help = "Usage: fget fname -- Download (get) file"
data_help = "Usage: data datalen -- Specify length of file to follow"
vers_help = "Usage: ver -- Get protocol version. alias: vers"
quit_help = "Usage: quit -- Terminate connection. alias: exit"
help_help = "Usage: help [command] -- Offer help on command"
lsls_help = "Usage: ls [dir] -- List files in dir"
lsls_help = "Usage: lsd [dir] -- List dirs in dir"
lsld_help = "Usage: help command -- Offer help on command"
cdcd_help = "Usage: cd dir -- Change to dir. Capped to server root"
pwdd_help = "Usage: pwd -- Show current dir"
stat_help = "Usage: stat fname  -- Get file stat. Field list:\n"\
"   1.  ST_MODE Inode protection mode.\n"\
"   2.  ST_INO Inode number.\n"\
"   3.  ST_DEV Device inode resides on.\n"\
"   4.  ST_NLINK  Number of links to the inode.\n"\
"   5.  ST_UID User id of the owner.\n"\
"   6.  ST_GID Group id of the owner.\n"\
"   7.  ST_SIZE Size in bytes of a plain file.\n"\
"   8.  ST_ATIME Time of last access.\n"\
"   9.  ST_MTIME Time of last modification.\n"\
"   10. ST_CTIME Time of last metadata change."\

tout_help = "Usage: timeout  -- Reset timeout"

xxxx_help = "Usage: no data"


# ------------------------------------------------------------------------
# Table driven server state machine.
# The table is searched for a mathing start_state, and the corresponding 
# function is executed. The new state set to end_state

state_table = [
            # Command ; start_state ; end_state ; action function
            ("user",    initial,    auth_pass,  get_user_func,  user_help),
            ("pass",    auth_pass,  in_idle,    get_pass_func,  pass_help),
            ("file",    in_idle,    got_fname,  get_fname_func, file_help),
            ("fget",    in_idle,    in_trans,   get_fget_func,  fget_help),
            ("data",    got_fname,  in_trans,   get_data_func,  data_help),
            ("ver",     all_in,     all_in,     get_ver_func,   vers_help),
            ("vers",    all_in,     all_in,     get_ver_func,   vers_help),
            ("quit",    all_in,     all_in,     get_exit_func,  quit_help),
            ("exit",    all_in,     all_in,     get_exit_func,  quit_help),
            ("help",    all_in,     all_in,     get_help_func,  help_help),
            ("ls",      auth_in,    auth_in,    get_ls_func,    lsls_help),
            ("lsd",     auth_in,    auth_in,    get_lsd_func,   lsld_help),
            ("cd",      auth_in,    auth_in,    get_cd_func,    cdcd_help),
            ("pwd",     auth_in,    auth_in,    get_pwd_func,   pwdd_help),
            ("stat",    auth_in,    auth_in,    get_stat_func,  stat_help),
            ("timeout", auth_in,    auth_in,    get_tout_func,  tout_help),
            ]
# ------------------------------------------------------------------------

class StateHandler():

    def __init__(self, resp):
        # Fill in class globals 
        self.curr_state = initial
        self.resp = resp
        self.resp.fname = ""
        self.resp.cwd = os.getcwd()
        self.resp.dir = ""
        syslog.openlog("pyserv.py")
    
    # --------------------------------------------------------------------
    # This is the function where outside stimulus comes in.
    # All the workings of the state protocol are handle here.
    # Return True for signalling session terminate request
    
    def run_state(self, strx):
        got = False; ret = True 
        comx = strx.split()
        
        # Scan the state table, execute actions, set new states
        for aa in state_table:
            # See if command is in state or all_in is in effect
            # or auth_in and stat > auth is in effect -- use early out
            cond = aa[1] == self.curr_state
            if not cond:
                cond = cond or (aa[1] == auth_in and self.curr_state >= in_idle) 
            if not cond:
                cond = cond or aa[1] == all_in
            if cond:
                if comx[0] == aa[0]:
                    # Execute relevant function
                    ret = aa[3](self, comx)
                    # Only set state if not all_in / auth_in
                    if aa[1] != all_in and aa[1] != auth_in:
                        self.curr_state = aa[2]
                    got = True
                    break
                    
        # Not found in the state table for the current state, complain
        if not got: 
            print "Invalid or out of sequence command:", strx
            self.resp.datahandler.putdata("ERR Invalid or out of sequence command")
            # Do not quit, just signal the error
            ret = False
        return ret          
    




