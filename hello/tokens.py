#!/usr/bin/env python

import sys, os, pygtk, gobject, pango, gtk
import tokenize

 
class InputStream(object):
    ''' Simple Wrapper for File-like objects. [c]StringIO doesn't provide
        a readline function for use with generate_tokens.
        Using a iterator-like interface doesn't succeed, because the readline
        function isn't used in such a context. (see <python-lib>/tokenize.py)
    '''
    def __init__(self, data):
        self.__data = [ '%s\n' % x for x in data.splitlines() ]
        self.__lcount = 0
    def readline(self):
        try:
            line = self.__data[self.__lcount]
            self.__lcount += 1
        except IndexError:
            line = ''
            self.__lcount = 0
        return line

class Tokenize():

    def __init__(self, data):
        for x in tokenize.generate_tokens(InputStream(data).readline):
            # x has 5-tuples
            tok_type, tok_str = x[0], x[1]
            srow, scol = x[2]
            erow, ecol = x[3]
            print x[0], x[1], x[2], x[3]

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    strx = sys.argv[1]    
    f = open(strx)
    buf = f.read()
    f.close()
   
    Tokenize(buf)
    #main()

