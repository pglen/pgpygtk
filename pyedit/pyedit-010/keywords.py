#!/usr/bin/env python

# Global keyword configuration for pyedit.

# ------------------------------------------------------------------------
# Add keywords to your taste. Note that we are cheating here, as the
# coloring sub system does not  parse the file, marely does a string
# compare. For example ' len(' is  unlikely to appear in any  context
# but in it's intended  place. Note that '=len(xx)' is not highlited but 
# '= len(xx)' is. Add  strings  that match your coding  style or your
# language. It is feasble to have a set of keywords that cover 
# multiple languages. (like # (hash) for bash, perl, python ...)
#
# Also note that coloring too much distracts from readability, so configure
# this conservatively.

# Keywords for coloring:
keywords =  ("def ", "import ", "from ", "for ", "while ", " len(",      
            "return ", "range(", "if ", "elif ", "not ", " abs(",       
            " any(", " all(", " min(", " max(",  " map(", " print ",    
            " open(", " in ", " break ", "[]", "()", "{}", " pass", "pass ",
            " True", " False", "True;", "False;", 
            "global ")

# Keywords for class releted enrties:
clwords =  "class ", " self.", "try:", "except:"

# Keywords for summary extraction: (left side window)
sumkeywords = "class ", "def ", "TODO"

# Keywords for autocorrect. This corrects strings as we type.
# As a 'C' programmer I kept typin' "else" ... this feature 
# corrects it to "else:"  (trailing colon for python)
# It is contraindicatory to support bad habits, but for productivity ....
# ... all is forgiven. (Especially if your next assmnt is in 'C')
#
# Syntax: from_str, to_str ....
# Make sure tostr is longer than from_str

acorr = [   ( "else",   "else:"                 ),
            ( "fo",     "for "                  ),
            ( "whi",    "while  "               ),
            ( "Tr",     "True  "                ),
            ( "Fa",     "False  "               ),
            ( "Fn",     "def funcname():  "     ),
            ( "br",     "break"                 ),
        ]

# EOF



