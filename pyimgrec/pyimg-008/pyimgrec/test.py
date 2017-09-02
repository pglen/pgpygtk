#!/usr/bin/env python

import os, sys, getopt, signal, array
import gobject, gtk, pango, random, time

import imgrec

print "Testing imgrec"

print imgrec.__doc__
print imgrec.version()
print "OPEN_IMAGE", imgrec.OPEN_IMAGE
#print imgrec.__dict__
print 0xffffff, 0xeeeeee, 0xffffff - 0xeeeeee
print "diffcol", imgrec.diffcol(0xffffff, 0xeeeeee)





