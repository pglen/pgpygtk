#!/bin/sh

# Back up current dir to another drive

MTARGET=/mnt/data
#TARGET=home/peterglen/pgsrc/pygtk/parser
TARGET=`pwd`

TT=`mount | grep $MTARGET`
#echo $TT

if [ "$TT" == "" ] ; then
    	echo "Please mount (or plug in) target drive ($MTARGET)"
        exit 1
fi
	
if [ ! -d $MTARGET ] ; then
    	echo "Please mount (or plug in) target drive ($MTARGET)"
        sleep 1
	exit 1
fi

if [ ! -d $MTARGET/$TARGET ] ; then
    	echo "Creating $MTARGET/$TARGET .... ";
	mkdir -p $MTARGET/$TARGET
fi

echo Copying from `pwd` to \'$MTARGET/$TARGET\' 

cp -auv *  $MTARGET/$TARGET
