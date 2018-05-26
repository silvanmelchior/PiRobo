#!/bin/bash


if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 
  exit 1
fi

SCRIPTPATH=$(readlink -f $0);
SCRIPTDIR=$(dirname $SCRIPTPATH);


cd $SCRIPTDIR
git pull # TODO

echo "Start Services"
./startup_II.sh
