#!/bin/bash


if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 
  exit 1
fi

SCRIPTPATH=$(readlink -f $0);
SCRIPTDIR=$(dirname $SCRIPTPATH);

# update stage II
./install.sh

# start services
python3 $SCRIPTDIR/services/web_service.py &
python3 $SCRIPTDIR/services/hw_service.py &

