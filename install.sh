#!/bin/bash

#
# Init
#
ABSPATH=$(readlink -f $0);
ABSDIR=$(dirname $ABSPATH);
VERFILE=$ABSDIR/version.txt;
VERSHOULD=1

if [ ! -f $VERFILE ]; then
  echo $VERSHOULD > $VERFILE;
fi

#
# Autostart
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERFILE` < $VERSHOULD )); then
  echo $VERSHOULD > $VERFILE;
  echo "=== Setup Autostart ===";
fi

#
# Install A
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERFILE` < $VERSHOULD )); then
  echo $VERSHOULD > $VERFILE;
  echo "=== Install A ===";
fi

