#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time, syslog, stat
import pyservsup

# Ping pong state machine

# 1.) States

initial     = 0
auth_user   = 1
auth_pass   = 2
in_idle     = 3
got_fname   = 4
in_trans    = 5
got_file    = 6

# The commands in this state are allowed in all states after auth
all_in      = 100

help_str =  \
"Commands: "\
"user "\
"pass "\
"file "\
"data "\
"quit "\
"exit "\
"timeout "\
"help "\

# ------------------------------------------------------------------------
# Escape spaces

def escape(strx):
    aaa = strx.replace("%", "%%")
    aaa = aaa.replace(" ", "%20")
    return aaa
# ------------------------------------------------------------------------
# Remove dup //

def dirclean(strx):
    rrr = ""; aaa = strx.split("/")
    for aa in aaa:
        if aa != "": rrr += "/" + aa
    return rrr    

# ------------------------------------------------------------------------
# Change directory to up (..)

def chup(strx):
    # Stage 1: clean
    rrr2 = ""; rrr = dirclean(strx)
    # Stage 2: cut end
    
    # The C way
    #aaa = rrr.split("/")
    #for aa in range(len(aaa) - 1):
    #    rrr2 += "/" + aaa[aa]
    #return rrr2
    
    # The python way
    for aa in rrr.split("/")[:-1]: 
        rrr2 += "/" + aa
    return rrr2
    
# ------------------------------------------------------------------------
# Table driven server state machine

class StateHandler():

    def __init__(self, resp):
    
        self.curr_state = initial
        self.resp = resp
        self.resp.fname = ""
        self.resp.cwd = os.getcwd()
        self.resp.dir = ""

        self.state_table = [
            # String ; start state ; end state ; action function
            ("user",    initial,   auth_pass,  self.get_user_func,),
            ("pass",    auth_pass, in_idle,    self.get_pass_func,),
            ("file",    in_idle,   got_fname,  self.get_fname_func,),
            ("data",    got_fname, in_trans,   self.get_data_func,),
            ("ls",      all_in,    all_in,     self.get_ls_func,),
            ("lsd",     all_in,    all_in,     self.get_lsd_func,),
            ("cd",      all_in,    all_in,     self.get_cd_func,),
            ("pwd",     all_in,    all_in,     self.get_pwd_func,),
            ("stat",    all_in,    all_in,     self.get_stat_func,),
            ("quit",    all_in,    all_in,     self.get_exit_func,),
            ("exit",    all_in,    all_in,     self.get_exit_func,),
            ("timeout", all_in,    all_in,     self.get_tout_func,),
            ("help",    all_in,    all_in,     self.get_help_func,),
            ]

    # State transition and action functions
    
    def get_lsd_func(self, strx):
        #print "get_ls_func", strx
        dname = ""; sss = ""
        try:
           dname = strx[1]; 
        except:
           pass
           
        dname2 = self.resp.cwd + "/" + self.resp.dir + "/" + dname
        dname2 = dirclean(dname2)
        print "lsd", dname2
        try:
            ddd = os.listdir(dname2)
            for aa in ddd:
                if stat.S_ISDIR(os.stat(aa)[stat.ST_MODE]):
                    # Escape spaces
                    sss += escape(aa) + " "
            response = "OK " + sss
        except:
            pyservsup.put_exception("lsd")
            response = "ERR " + str(sys.exc_info()[1] )
        self.resp.datahandler.putdata(response)
        
    def get_ls_func(self, strx):
        #print "get_ls_func", strx
        dname = ""; sss = ""
        try:
            dname = strx[1]; 
        except:
            pass   
        dname2 = self.resp.cwd + "/" + self.resp.dir + "/" + dname
        dname2 = dirclean(dname2)
        try:
            ddd = os.listdir(dname2)
            for aa in ddd:
                if not stat.S_ISDIR(os.stat(aa)[stat.ST_MODE]):
                    # Escape spaces
                    sss += escape(aa) + " "
            response = "OK " + sss
        except:
            pyservsup.put_exception("ls ")
            response = "ERR " + str(sys.exc_info()[1] )
        self.resp.datahandler.putdata(response)
        
    def get_pwd_func(self, strx):
        #print "get_pwd_func", strx
        fname = ""; aaa = " "
        try:
            #sss = os.getcwd()
            dname2 = self.resp.cwd + "/" + self.resp.dir
            dname2 = dirclean(dname2)
            response = "OK " + dname2
        except OSError:
            #print sys.exc_info()
            pyservsup.put_exception("pwd")
            response = "ERR " + str(sys.exc_info()[1] )
        except:
            pyservsup.put_exception("pwd")
            response = "ERR Must specify file name"
        self.resp.datahandler.putdata(response)
        
    def get_cd_func(self, strx):
        #print "get_cd_func", strx
        try:
            dname = strx[1];    
            if dname == "..":
                self.resp.dir = chup(self.resp.dir)
            else:     
                self.resp.dir += "/" + dname
           
            self.resp.dir = dirclean(self.resp.dir)
            
            dname2 = self.resp.cwd + "/" + self.resp.dir 
            dname2 = dirclean(dname2)
            response = "OK " + dname2
        except OSError:
            pyservsup.put_exception("cd")
            response = "ERR " + str(sys.exc_info()[1] )
        except:
            pyservsup.put_exception("cd")
            response = "ERR Must specify directory name"
            print sys.exc_info()
            
        self.resp.datahandler.putdata(response)
      
    def get_stat_func(self, strx):
        #print "get_stat_func", strx
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
        #print "get_user_func", strx
        self.resp.datahandler.putdata("OK")
        pass
        
    def get_pass_func(self, strx):
        #print "get_pass_func", strx
        self.resp.datahandler.putdata("OK")
        pass
    
    def get_fname_func(self, strx):
        #print "get_fname_func", strx
        try:
            self.resp.fname = strx[1]
            response = "OK Send file '" + self.resp.fname + "'"
        except:
            response = "ERR Must specify file name"
            
        self.resp.datahandler.putdata(response)
    
    def get_data_func(self, strx):
        #print "get_data_func", strx
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
            need = min(1024,  self.resp.dlen - mylen)
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
    
        xstr = "Received file: '" + self.resp.fname + "' ", self.resp.dlen, "bytes"
        print xstr
        #syslog.syslog(xstr)

        self.resp.datahandler.putdata("OK Got data")
                
    def get_help_func(self, strx):
        print "get_help_func", strx
        self.resp.datahandler.putdata(help_str)
        
    # Also stop timeouts
    def get_exit_func(self, strx):
        #print "get_exit_func", strx
        self.resp.datahandler.putdata("OK Bye")
        
        # Cancel after sending bye
        if self.resp.datahandler.tout: 
            self.resp.datahandler.tout.cancel()
        return True

    def get_tout_func(self, strx):
        print "get_tout_func", strx
        if self.resp.datahandler.tout: 
            self.resp.datahandler.tout.cancel()
        self.resp.datahandler.putdata("OK timeout reset")
        return True
        
    # --------------------------------------------------------------------
    # This is the function where outside stimulus comes in
    def run_state(self, strx):
        got = False; ret = True 
        comx = strx.split()
        
        # Scan the state table, execute actions
        for aa in self.state_table:
            # See if command is in state or all_in is in effect
            if aa[1] ==  self.curr_state or \
                (aa[1] == all_in and self.curr_state >= in_idle):
                #print "in state", aa[1], "comm:", aa[0]
                if comx[0] == aa[0]:
                    ret = aa[3](comx)
                    if aa[1] != all_in:
                        self.curr_state = aa[2]
                    got = True
                    break
                    
        # Not found in the state table, complain
        if not got: 
            print "Invalid or out of sequence command:", strx
            self.resp.datahandler.putdata("ERR Invalid or out of sequence command")
            # Do not quit, just signal the error
            ret = False
            
        return ret          
    
    
    







