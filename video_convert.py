from subprocess import PIPE, Popen
import glob
from datetime import datetime
import os
import sys


# unit: Gigabytes, 3 GB is good to place a new converted video, waiting for output script to write to external usb drive and remove
# For capture script, threshold is 5 GB so that if space is not enough, priority will be converting script in order to convert and possibly empty space for further capturing
VIDEO_CAPTURE_SIZE = 3
CAPTURES_DIR = "/home/pi/workspace/"
CAPTURES_FORMAT = ".h264"
OUTPUT_FORMAT = ".mp4"
CAPTURES_REGEX = CAPTURES_DIR + "*" + CAPTURES_FORMAT
VIDEO_FILE_NAME_FORMAT = "%Y-%m-%d_%H-%M-%S"


def is_space_full():
	output = Popen(["df", "-H", "/"], stdout=PIPE).communicate()[0]
	device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
	if float(available.split("G")[0]) <= VIDEO_CAPTURE_SIZE:
		return True
	else:
		return False


def convert(input_name, output_name):
	output = Popen(["MP4Box", "-add", input_name, output_name], stdout=PIPE).communicate()[0]
	return output


if __name__ == '__main__':
	# Check if sd card space almost full
	# Remove earliest video file if full
	if not is_space_full():
		captures = [ capture.split(CAPTURES_DIR)[1].split(CAPTURES_FORMAT)[0] for capture in glob.glob(CAPTURES_REGEX) ]
		dates = []
		for capture in captures:
			try:
				dates.append(datetime.strptime(capture, VIDEO_FILE_NAME_FORMAT))
			except ValueError:
				continue

		# Something is wrong, cannot find any to be converted video file
		if not dates:
			sys.exit(1)
		
		# Check if any video is in need of conversion, starting from earliest one
		while len(dates) > 0:
			to_be_converted = min(dates)
			input_name = CAPTURES_DIR + to_be_converted.strftime(VIDEO_FILE_NAME_FORMAT) + CAPTURES_FORMAT
			output_name = input_name.split(CAPTURES_FORMAT)[0] + OUTPUT_FORMAT		
			
			# Check if corresponding converted file exists, if yes, then remove such entry and check next min date
			if glob.glob(output_name):
				dates.remove(to_be_converted)
				continue
			else:
				# actual conversion
				convert(input_name, output_name)
				
				# must exit now since we need space waiting for new captures, and cannot process that fast until output script moves converted videos out
				sys.exit()
	
	print "finally"
		

