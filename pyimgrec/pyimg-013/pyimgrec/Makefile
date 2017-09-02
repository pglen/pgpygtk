# ------------------------------------------------------------------------
# Makefile for imgrec python module
#
# Simplified for CentOS compile. Edit path for your system.
# 
# Converted to automake dec/1/2015
#

#COPT = -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 \
#    -DMINOR_VERSION=0 -I/usr/include/pygtk-2.0 -I/usr/include/glib-2.0 \
#        -I/usr/include/python2.6 -I/usr/local/lib/glib-2.0/include \
#            -I/usr/include/libxml2 -I/usr/include/gnome-vfs-2.0 \
#             -I/usr/lib/gnome-vfs-2.0/include -I/usr/include/gconf/2 \
#              -I/usr/include/orbit-2.0 -I/usr/include/dbus-1.0 \
#                -I/usr/lib/dbus-1.0/include  
                
# Simplified for CentOS 7 compile. Edit path for your system.

#COPT = -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 \
#    -DMINOR_VERSION=0 -I/usr/include/pygtk-2.0 -I/usr/include/glib-2.0 \
#        -I/usr/include/python2.7 -I/usr/local/lib/glib-2.0/include \
#            -I/usr/include/libxml2 -I/usr/include/gnome-vfs-2.0 \
#             -I/usr/lib/gnome-vfs-2.0/include -I/usr/include/gconf/2 \
#              -I/usr/include/orbit-2.0 -I/usr/include/dbus-1.0 \
#                -I/usr/lib/dbus-1.0/include  


#COPT = -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC \
#    -DMAJOR_VERSION=1 -DMINOR_VERSION=0 \
#        -I/usr/include/python2.7  \
#            -D_REENTRANT -I/usr/include/gtk-2.0 -I/usr/lib/gtk-2.0/include -I/usr/include/pango-1.0 -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pixman-1 -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/libpng16 -I/usr/include/pango-1.0 -I/usr/include/harfbuzz -I/usr/include/pango-1.0 -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/freetype2 -I/usr/include/libpng16

COPT = -DNDEBUG -g -O3 -Wall -Wstrict-prototypes  \
    -DMAJOR_VERSION=1 -DMINOR_VERSION=0 \
        -I/usr/include/python2.7  \
            -D_REENTRANT -I/usr/include/gtk-2.0 -I/usr/lib/gtk-2.0/include -I/usr/include/pango-1.0 -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pixman-1 -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/libpng16 -I/usr/include/pango-1.0 -I/usr/include/harfbuzz -I/usr/include/pango-1.0 -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I/usr/include/freetype2 -I/usr/include/libpng16 -I/usr/include/freetype2 -I/usr/include/libpng16

# This way inference rules can be used.                
CFLAGS=${COPT}

# Add targets here
TARGS = imgrec.o line.o square.o utils.o color.o flood.o norm.o walk.o
	 
# ------------------------------------------------------------------------

all:  imgrec.so

imgrec.so:  ${TARGS} Makefile
	#./bdate.py > bdate.h
	gcc -shared  ${TARGS}  -lgtk-x11-2.0 -lgdk-x11-2.0 -lpangocairo-1.0 -latk-1.0 -lcairo -lgdk_pixbuf-2.0 -lgio-2.0 -lpangoft2-1.0 -lpango-1.0 -lgobject-2.0 -lglib-2.0 -lintl -lfontconfig -lfreetype  -lpython2.7 \
		     -o imgrec.so    

utils.o:  utils.h

clean:
	rm *.o




