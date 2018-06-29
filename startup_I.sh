#!/bin/bash


if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 
  exit 1
fi

SCRIPTPATH=$(readlink -f $0);
SCRIPTDIR=$(dirname $SCRIPTPATH);

# update stage I
cd $SCRIPTDIR
sudo -u pi git pull

# continue with newly loaded files
./startup_II.sh
