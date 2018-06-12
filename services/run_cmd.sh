#!/bin/bash

stdbuf -i0 -o0 -e0 /home/pi/build/main | python3 /home/pi/PiRobo/services/run_monitor.py
