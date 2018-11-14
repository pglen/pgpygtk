# ------------------------------------------------------------------------
# Makefile for bluepoint2 python module
#
# Simplified for CentOS compile. Edit path for your system.

COPT =  -DNDEBUG -m32 -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 \
    -DMS_WIN32 -DMINOR_VERSION=0 -I/mingw32/include/python2.7 
                
#COPT =  -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 \
#    -DMINOR_VERSION=0 -I/mingw32/include/python2.7 
                
# This way inference rules can be used.                
CFLAGS=${COPT}

# Add targets here
TARGS = bluepoint2.o bluepy.o

# ------------------------------------------------------------------------

all:  bluepy.so

#bluepoint2.o:
#	gcc -shared  -c  bluepoint2.c

bluepy.so:  ${TARGS} Makefile                                            
	./bdate.py > bdate.h
	gcc -shared   ${TARGS}  -lpython2.7 -o bluepy.so    

clean:
	rm -f *.o
	rm -f *.so









