#!/usr/bin/env python

import os, sys, getopt, signal, select, string, time

# Ping pong state machine

# 1.) States

initial     = 0
auth_user   = 1
auth_pass   = 2
in_idle     = 3
got_fname   = 4
in_trans    = 5
got_file    = 6

all_in      = 100

help_str =  \
"Commands: "\
"user "\
"pass "\
"file "\
"data "\
"quit "\
"help "\

# 3.) State transition tables
       
'''state_table = [
    # String ; start state ; end state ; action function
    ("user", initial,   auth_pass,  self.get_user_func,),
    ("pass", auth_pass, in_idle,    self.get_pass_func,),
    ("file", in_idle,   got_fname,  self.get_fname_func,),
    ("data", got_fname, in_trans,   self.get_data_func,),
    ("quit", all_in,    all_in,     self.get_exit_func,),
    ("help", all_in,    all_in,     self.get_help_func,),
    ]
'''

# ------------------------------------------------------------------------
# Table driven server state machine

class StateHandler():

    def __init__(self, resp):
    
        self.curr_state = initial
        self.resp = resp
        self.resp.fname = ""
        self.state_table = [
            # String ; start state ; end state ; action function
            ("user", initial,   auth_pass,  self.get_user_func,),
            ("pass", auth_pass, in_idle,    self.get_pass_func,),
            ("file", in_idle,   got_fname,  self.get_fname_func,),
            ("data", got_fname, in_trans,   self.get_data_func,),
            ("quit", all_in,    all_in,     self.get_exit_func,),
            ("exit", all_in,    all_in,     self.get_exit_func,),
            ("help", all_in,    all_in,     self.get_help_func,),
            ]
  
    # 2.) State transition and action functions
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
        print "get_data_func", strx
        if self.resp.fname == "":
            response = "ERR No filename for data"
            self.resp.datahandler.putdata(response)
            return
        try:
           self.resp.dlen = int(strx[1])
        except:
            response = "ERR Must specify file name"
            response = "ERR No filename for data"
            self.resp.datahandler.putdata(response)
            return
        self.resp.datahandler.putdata("OK Send data")
                
        fh = open(self.resp.fname, "w")         
        # Consume buffers until got all
        mylen = 0
        while mylen < self.resp.dlen:
            need = min(1024,  self.resp.dlen - mylen)
            need = max(need, 0)
            #data = self.resp.datahandler.getdata(need)
            data = self.resp.datahandler.handle_one(self.resp)
            fh.write(data)
            #print "data", data
            
            print "need", need, "got", len(data)
            mylen += len(data)
            if len(data) == 0:
                break
            
        print "got ", mylen , bytes
        fh.close()
        self.resp.datahandler.putdata("OK Got data")
                
    def get_help_func(self, strx):
        print "get_help_func", strx
        self.resp.datahandler.putdata(help_str)
        
    # Also stop timeouts
    def get_exit_func(self, strx):
        print "get_exit_func", strx
        self.resp.datahandler.putdata("OK")
        if self.resp.datahandler.tout: 
            self.resp.datahandler.tout.cancel()
        return True
        
    # This is the function where outside stimulus comes in
    def run_state(self, strx):
        print "run_state", self.curr_state, "'" + strx + "'"
        got = False; ret = True 
        comx = strx.split()
        #print comx
        
        # Scan the state table, execute actions
        for aa in self.state_table:
            # See if command is in state or all_in
            if aa[1] ==  self.curr_state or aa[1] == all_in:
                print "in state", aa[1], "comm:", aa[0]
                if comx[0] == aa[0]:
                    ret = aa[3](comx)
                    if aa[1] != all_in:
                        self.curr_state = aa[2]
                    got = True
                    break
                    
        # Not found in the state order, complain
        if not got: 
            print "Invalid or out of sequence command:", strx
            self.resp.datahandler.putdata("ERR Invalid or out of sequence Command")
            # Do not quit, just signal error
            ret = False
            
        return ret          
    
    
    



