#!/usr/bin/env python

import sys, math

# ------------------------------------------------------------------------
# Transfer function for neunet. Calculate logaritmic taper, preserve sign

# ------------------------------------------------------------------------
# The hyperbolic function

def tfunc(val):
    ret = 0.
    try:
        cc = float(val)
        ll = math.tanh(20 * cc)
        ret =  ll 
    except ValueError:
        print "Value error:", val, sys.exc_info()
        pass
    except:
        print val, sys.exc_info()
        pass
        
    #if val < 0:
    #    ret = -ret;

    return ret

def tfunc2(val):
    ret = 0.
    try:
        cc = float(val)
        ll = 1. / (1. + math.exp(-cc))
        ret =  ll
    except ValueError:
        print val, sys.exc_info()
        pass
    except:
        print "Exception", val, sys.exc_info()
        pass
    #if val < 0:
    #     ret = -ret;
        
    return ret

# ------------------------------------------------------------------------
# The traditional exponent

def tfunc3(val):
    ret = 0.
    try:
        cc = float(val)
        ll = math.log(1 + 100 * abs(cc))
        ret =  ll / 4
    except ValueError:
        print val, sys.exc_info()
        pass
    except:
        print val, sys.exc_info()
        pass
    if val < 0:
        ret = -ret;
    return ret

# ------------------------------------------------------------------------




