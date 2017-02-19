from subprocess import PIPE, Popen
import glob
from datetime import datetime
import os
import sys


# unit: Gigabytes
VIDEO_CAPTURE_SIZE = 3
CAPTURES_DIR = "/home/pi/workspace/"
CAPTURES_FORMAT = ".h264"
CAPTURES_REGEX = CAPTURES_DIR + "*" + CAPTURES_FORMAT
VIDEO_FILE_NAME_FORMAT = "%Y-%m-%d_%H-%M-%S"


def is_space_full():
	output = Popen(["df", "-H", "/"], stdout=PIPE).communicate()[0]
	device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
	if float(available.split("G")[0]) <= VIDEO_CAPTURE_SIZE:
		return True
	else:
		return False

# default duration is 1 hour = 60 * 60 * 1000 ms
def capture(output_name, duration=3600000):
	# no preview
	output = Popen(["raspivid", "-o", output_name, "-t", str(duration), "-n"], stdout=PIPE).communicate()[0]
	return output


if __name__ == '__main__':
	# Check if sd card space almost full
	# Remove earliest video file if full
	if is_space_full():
		captures = [ capture.split(CAPTURES_DIR)[1].split(CAPTURES_FORMAT)[0] for capture in glob.glob(CAPTURES_REGEX) ]
		dates = []
		for capture in captures:
			try:
				dates.append(datetime.strptime(capture, VIDEO_FILE_NAME_FORMAT))
			except ValueError:
				continue

		# Something is taking space, but not our captures
		if not dates:
			sys.exit()

		try:
			to_be_removed = min(dates)
			os.remove(CAPTURES_DIR + to_be_removed.strftime(VIDEO_FILE_NAME_FORMAT) + CAPTURES_FORMAT)
		except OSError:
			sys.exit(1)
		
	# Create 1 hour video capture if space is not full now
	if not is_space_full():
		output_name = CAPTURES_DIR + datetime.now().strftime(VIDEO_FILE_NAME_FORMAT) + CAPTURES_FORMAT
		capture(output_name, duration=2000)
	
	print "finally"
		

