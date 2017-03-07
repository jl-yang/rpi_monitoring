from subprocess import PIPE, Popen
import glob
from datetime import datetime
import os
import sys
from shutil import copyfile


# However, usb drive should be found existing and also have a bit more space, e.g. 5 GB
CAPACITY = 1
CAPTURES_DIR = "/home/pi/workspace/"
OUTPUT_FORMAT = ".mp4"
OUTPUT_REGEX = CAPTURES_DIR + "*" + OUTPUT_FORMAT
VIDEO_FILE_NAME_FORMAT = "%Y-%m-%d_%H-%M-%S"


def is_space_full(capacity_limit, path="/"):
	output = Popen(["df", "-H", path], stdout=PIPE).communicate()[0]
	device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
	if int(float(available.split("G")[0])) <= capacity_limit:
		return True
	else:
		return False


def convert(input_name, output_name):
	output = Popen(["MP4Box", "-add", input_name, output_name], stdout=PIPE).communicate()[0]
	return output


def is_mounted():
	return os.path.ismount(USB_DRIVE_MOUNT_POINT)


if __name__ == '__main__':
	# Check usb drive is not full, remove earliest file if full
	if is_space_full(CAPACITY):			
		videos = [ video.split(CAPTURES_DIR)[1].split(OUTPUT_FORMAT)[0] for video in glob.glob(OUTPUT_REGEX) ]
		dates = []
		for video in videos:
			try:
				dates.append(datetime.strptime(video, VIDEO_FILE_NAME_FORMAT))
			except ValueError:
				continue
		if not dates:
			sys.exit(1)

		# Remove earliest video file in usb drive
		to_be_deleted = CAPTURES_DIR + min(dates).strftime(VIDEO_FILE_NAME_FORMAT) + OUTPUT_FORMAT
		try:
			os.remove(to_be_deleted)
		except OSError:
			sys.exit(1)

