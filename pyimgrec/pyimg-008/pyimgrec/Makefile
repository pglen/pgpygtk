# ------------------------------------------------------------------------
# Makefile for imgrec python module
#
# Simplified for CentOS compile. Edit path for your system.

#COPT = -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 \
#    -DMINOR_VERSION=0 -I/usr/include/pygtk-2.0 -I/usr/include/glib-2.0 \
#        -I/usr/include/python2.6 -I/usr/local/lib/glib-2.0/include \
#            -I/usr/include/libxml2 -I/usr/include/gnome-vfs-2.0 \
#             -I/usr/lib/gnome-vfs-2.0/include -I/usr/include/gconf/2 \
#              -I/usr/include/orbit-2.0 -I/usr/include/dbus-1.0 \
#                -I/usr/lib/dbus-1.0/include  
                
# Simplified for CentOS 7 compile. Edit path for your system.

COPT = -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 \
    -DMINOR_VERSION=0 -I/usr/include/pygtk-2.0 -I/usr/include/glib-2.0 \
        -I/usr/include/python2.7 -I/usr/local/lib/glib-2.0/include \
            -I/usr/include/libxml2 -I/usr/include/gnome-vfs-2.0 \
             -I/usr/lib/gnome-vfs-2.0/include -I/usr/include/gconf/2 \
              -I/usr/include/orbit-2.0 -I/usr/include/dbus-1.0 \
                -I/usr/lib/dbus-1.0/include  

# This way inference rules can be used.                
CFLAGS=${COPT}

# Add targets here
TARGS = imgrec.o line.o square.o utils.o color.o flood.o

# ------------------------------------------------------------------------

all:  imgrec.so

imgrec.so:  ${TARGS} Makefile
	./bdate.py > bdate.h
	gcc -shared  ${TARGS} -L/usr/local/lib  -o imgrec.so    

clean:
	rm *.o







