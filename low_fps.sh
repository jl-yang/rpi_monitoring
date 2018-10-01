#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H-%M-%S")

raspivid -w 1280 -h 720 -fps 5 -t 0 -o "/home/pi/test_${DATE}.h264"

