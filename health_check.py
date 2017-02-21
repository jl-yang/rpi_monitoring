import os
import sys


if not os.listdir("/mnt/usb"):
	sys.exit(1)
else:
	sys.exit(0) 
