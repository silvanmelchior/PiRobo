#!/bin/bash


#
# Init
#
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 
  exit 1
fi

HOMEPATH="/home/pi"
SCRIPTPATH=$(readlink -f $0);
SCRIPTDIR=$(dirname $SCRIPTPATH);
VERIS=$SCRIPTDIR/version.txt;
VERSHOULD=1

if [ ! -f $VERIS ]; then
  echo $VERSHOULD > $VERIS;
fi


#
# Install RPi Cam Web Interface
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Install RPi Cam Web Interface ===";

  apt-get update
  cd $HOMEPATH;
  git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface;
  cd RPi_Cam_Web_Interface
  echo "#This is config file for main installer. Put any extra options in here." > ./config.txt
  echo "rpicamdir=\"cam_interface\"" >> ./config.txt
  echo "webserver=\"apache\"" >> ./config.txt
  echo "webport=\"80\"" >> ./config.txt
  echo "user=\"\"" >> ./config.txt
  echo "webpasswd=\"\"" >> ./config.txt
  echo "autostart=\"yes\"" >> ./config.txt
  echo "jpglink=\"no\"" >> ./config.txt
  echo "phpversion=\"7\"" >> ./config.txt
  echo "" >> ./config.txt
  chmod 664 ./config.txt
  ./install.sh q

  echo "annotation" > /var/www/cam_interface/uconfig
  echo "hflip 1" >> /var/www/cam_interface/uconfig
  echo "vflip 1" >> /var/www/cam_interface/uconfig

  echo $VERSHOULD > $VERIS;
fi


#
# Configure Webserver
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Configure Webserver ===";

  rm -rf /var/www/html
  ln -s $SCRIPTDIR/www /var/www/pirobo

  echo $VERSHOULD > $VERIS;
fi


#
# Configure Icecoder
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Configure Webserver ===";

  chmod 777 $SCRIPTDIR/www/icecoder/backups
  chmod 777 $SCRIPTDIR/www/icecoder/lib
  chmod 777 $SCRIPTDIR/www/icecoder/plugins
  chmod 777 $SCRIPTDIR/www/icecoder/test
  chmod 777 $SCRIPTDIR/www/icecoder/tmp

  mkdir $HOMEPATH/usercode
  chmod 777 $HOMEPATH/usercode

  echo $VERSHOULD > $VERIS;
fi



# TODO
# Control PiRobo over smartphone as before
# Log-Files Appache not touchscreen logging etc.
# Aruco
# Code-Editor & compiler





