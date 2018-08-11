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
VERIS=$SCRIPTDIR/install_log.txt;
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
  echo "video_width 1296" >> /var/www/cam_interface/uconfig
  echo "video_height 972" >> /var/www/cam_interface/uconfig

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
  echo "=== Configure Icecoder ===";

  chmod 777 $SCRIPTDIR/www/icecoder/backups
  chmod 777 $SCRIPTDIR/www/icecoder/lib
  chmod 777 $SCRIPTDIR/www/icecoder/plugins
  chmod 777 $SCRIPTDIR/www/icecoder/test
  chmod 777 $SCRIPTDIR/www/icecoder/tmp

  cp $SCRIPTDIR/copysrc/config-localhost.php $SCRIPTDIR/www/icecoder/lib/config-localhost.php
  chmod 777 $SCRIPTDIR/www/icecoder/lib/config-localhost.php
  chmod 777 $SCRIPTDIR/www/icecoder/lib/config___settings.php

  mkdir $HOMEPATH/usercode
  chmod 777 $HOMEPATH/usercode
  mkdir $HOMEPATH/build
  chmod 777 $HOMEPATH/build
  
  cp $SCRIPTDIR/copysrc/main.c $HOMEPATH/usercode/main.c
  chmod 777 $HOMEPATH/usercode/main.c

  cp $SCRIPTDIR/copysrc/main $HOMEPATH/build/main
  chmod 777 $HOMEPATH/build/main
  
  ln -s $SCRIPTDIR/inc $HOMEPATH/build/inc

  echo $VERSHOULD > $VERIS;
fi


#
# Setup Autostart
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Setup Autostart & Autoupdate ===";

  CMD=$SCRIPTDIR/startup_I.sh
  sed -i '$i'$CMD /etc/rc.local

  echo $VERSHOULD > $VERIS;
fi


#
# Set ID
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Set ID ===";

  ID=`date +%s`
  echo $ID > $SCRIPTDIR/ID.txt

  echo $VERSHOULD > $VERIS;
fi


#
# Install Python
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Install Python ===";

  apt-get update
  apt-get install -y build-essential python3-dev python3-smbus python3-serial python3-pip

  echo $VERSHOULD > $VERIS;
fi


#
# Install Drivers
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Install Drivers ===";

  apt-get update
  apt-get install -y python3-rpi.gpio

  echo $VERSHOULD > $VERIS;
fi


#
# Configure Default Wlan
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Configure Default Wlan ===";

  echo "" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "network={" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "  ssid=\"PiRobo_Ctrl\"" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "  psk=\"raspberry007\"" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "}" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "network={" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "  ssid=\"Enter_Name\"" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "  psk=\"Enter_PWD\"" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "}" >> /etc/wpa_supplicant/wpa_supplicant.conf 

  echo $VERSHOULD > $VERIS;
fi


#
# Configure Automatic Redirect
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Configure Automatic Redirect ===";

  cp $SCRIPTDIR/copysrc/redirect.php /var/www/index.php
  
  echo $VERSHOULD > $VERIS;
fi


#
# Install Drivers II
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Install Drivers II ===";

  pip3 install Pillow
  pip3 install psutil
  apt-get update
  apt-get install -y libtiff5
  
  echo $VERSHOULD > $VERIS;
fi


#
# Install Drivers III
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Install Drivers III ===";

  pip3 install wifi
  
  echo $VERSHOULD > $VERIS;
fi


#
# Configure Default Wlan II
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Configure Default Wlan II ===";

  echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" > /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "update_config=1" >> /etc/wpa_supplicant/wpa_supplicant.conf
  echo "" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "network={" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "  ssid=\"PiRobo_Ctrl\"" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "  psk=\"raspberry007\"" >> /etc/wpa_supplicant/wpa_supplicant.conf 
  echo "}" >> /etc/wpa_supplicant/wpa_supplicant.conf 

  echo $VERSHOULD > $VERIS;
fi


#
# Fixes
#
VERSHOULD=$((VERSHOULD+1));
if (( `cat $VERIS` < $VERSHOULD )); then
  echo "=== Fixes ===";

  pip3 install psutil
  echo "annotation" > /var/www/cam_interface/uconfig
  echo "video_width 1296" >> /var/www/cam_interface/uconfig
  echo "video_height 972" >> /var/www/cam_interface/uconfig

  echo $VERSHOULD > $VERIS;
fi



# TODO
# Code:
#   Code-Editor HW-access (display, joystick, external GPIOs, i2c-bus)
#   Log-Files Appache not touchscreen and status logging etc.
#   Helpful main.c (and copy as template.c) as default
# Detail Bug:
#   run-cmd on website need 2s for output if same as before
#   (and fresh installation fredy strange first use)
#   overview-page mobile layout
# Scoreboard (see ownCloud)
# Network incl. possibility to access inet
# Test:
#   Test how long battery holds
#   Test different browsers! E.g. edge on windows
#   Test with many devices in same wlan w/o inet-access (camera update rate?)
#   Test remote-update on all devices simultaneously (also how to do w/o inet?)
# Document:
#   Explanation how to use at home (WLAN, admin-interface)
#   Admin-Iface reminder that update s.t. from main screen
#   HW-documentation to build robot
#   Battery guideline allowed voltage
# Fancy:
#   Remote-Ctrl all Robots (run code, shutdown/reboot, ...)
#   Tensorflow / Reinforcement learning / ...
