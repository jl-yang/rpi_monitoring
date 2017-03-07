from subprocess import PIPE, Popen
import glob
from datetime import datetime
import os
import sys
import time


# unit: Gigabytes, normally it is < 3 GB, but considering space for converting is around 4 GB, 5 GB is better
VIDEO_CAPTURE_SIZE = 1
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
	output = Popen(["raspivid", "-o", output_name, "-t", str(duration), "-n", "-w", "1280", "-h", "720"], stdout=PIPE).communicate()[0]
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
		
	# Set a max retry limit as 5 times, and try after each 1 min, since it is run byt crontab hourly and raspberry pi camera can be inaccessible state when next script is executed but last script has not finished
	# Calculate elapsed time to be at least 30 mins, since normally we set duration as 1 hour
	times = 5
	while times > 0:
		start = int(time.time())

		# Create 1 hour video capture if space is not full now
		if not is_space_full():
			output_name = CAPTURES_DIR + datetime.now().strftime(VIDEO_FILE_NAME_FORMAT) + CAPTURES_FORMAT
			capture(output_name, duration=1800000)

		elapsed = int(time.time()) - start
		print elapsed
		if elapsed > 60 * 5:
			# Successful run, exit now
			break
		else:
			# Not successful attempt, sleep 1 min and retry again
			time.sleep(60)
			times -= 1

	print "finally"
		

