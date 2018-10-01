#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H-%M-%S")

# each pic per second is around 0.5M,
# then 1 month is 0.5 * 60 * 60 * 24 * 31 = 1339200M = 1307G
raspistill -w 1280 -h 720 -t 0 -tl 1000 -o "/home/pi/image_${DATE}_%09d.jpg"
