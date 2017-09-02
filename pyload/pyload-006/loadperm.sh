#!/bin/bash

# Fix permissions of the devices and sys entries

DDEV=`ls /dev/input/by-path/*kbd`
POWS=/sys/power/state
#echo $DDEV, $POWS
sudo chmod g+rw     $POWS
sudo chown .shutdown $POWS
sudo chmod g+r       $DDEV
sudo chown .shutdown $DDEV



