# PiRobo

## About

This repo contains software that enables AlphaBot to be programed and controled over the web.

## Installation

Execute the following commands on the Raspberry Pi as the user 'pi':

```
cd ~
sudo apt-get install git
git clone https://github.com/silvanmelchior/PiRobo.git
cd PiRobo
sudo ./install.sh
```

Assumes a freshly installed Raspbian on the Pi (tested with raspbian stretch lite 2018-04-18) with enabled camera and i2c support

## Update

The software updates itself automatically at startup via `git pull` as user 'pi'. It assumes the following:
* All files in the git repo are owned by user 'pi' (or listed in `.gitignore`)
* All update commands are executed over the script `install.sh`
* The update commands executed in `install.sh` restart the system if needed
