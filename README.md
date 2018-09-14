# rpi_monitoring
Monitoring with raspberry pi and pi camera 24X7, keep latest weekly capture in usb drive. Each capture is 1 hour duration. Assum rpi sd card size is larger than 16G, usb drive size larger than 500G

# dependencies
### MP4Box
sudo apt-get install gpac

# crontab configurations
 - sudo crontab -e
 - 0 * * * * python /home/pi/workspace/rpi_monitoring/video_capture.py
 - 0 * * * * python /home/pi/workspace/rpi_monitoring/video_convert.py
 - 0 * * * * python /home/pi/workspace/rpi_monitoring/health_check.py

