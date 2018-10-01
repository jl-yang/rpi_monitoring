#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H-%M-%S")

raspivid -w 1280 -h 720 -t 0 -o "/home/pi/image_${DATE}.h264" --timed 1000,1000

