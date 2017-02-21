from subprocess import PIPE, Popen
import glob
from datetime import datetime
import os
import sys
from shutil import copyfile


# However, usb drive should be found existing and also have a bit more space, e.g. 5 GB
USB_DRIVE_CAPACITY = 5
CAPTURES_DIR = "/home/pi/workspace/"
USB_DRIVE_MOUNT_POINT = "/mnt/usb/"
CAPTURES_FORMAT = ".h264"
OUTPUT_FORMAT = ".mp4"
OUTPUT_REGEX = CAPTURES_DIR + "*" + OUTPUT_FORMAT
STORAGE_REGEX = USB_DRIVE_MOUNT_POINT + "*" + OUTPUT_FORMAT
VIDEO_FILE_NAME_FORMAT = "%Y-%m-%d_%H-%M-%S"


def is_space_full(capacity_limit, path="/"):
	output = Popen(["df", "-H", path], stdout=PIPE).communicate()[0]
	device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
	if float(available.split("G")[0]) <= capacity_limit:
		return True
	else:
		return False


def convert(input_name, output_name):
	output = Popen(["MP4Box", "-add", input_name, output_name], stdout=PIPE).communicate()[0]
	return output


def is_mounted():
	return os.path.ismount(USB_DRIVE_MOUNT_POINT)


if __name__ == '__main__':
	# Check usb drive is mounted
	if is_mounted() is False:
		sys.exit()

	# Check usb drive is not full, remove earliest file if full
	if is_space_full(USB_DRIVE_CAPACITY, USB_DRIVE_MOUNT_POINT):			
		videos = [ video.split(USB_DRIVE_MOUNT_POINT)[1].split(OUTPUT_FORMAT)[0] for video in glob.glob(STORAGE_REGEX) ]
		dates = []
		for video in videos:
			try:
				dates.append(datetime.strptime(video, VIDEO_FILE_NAME_FORMAT))
			except ValueError:
				continue
		if not dates:
			sys.exit(1)

		# Remove earliest video file in usb drive
		to_be_deleted = USB_DRIVE_MOUNT_POINT + min(dates).strftime(VIDEO_FILE_NAME_FORMAT) + OUTPUT_FORMAT
		try:
			os.remove(to_be_deleted)
		except OSError:
			sys.exit(1)

	# Though we already removed a file, however, usb drive capacity needs to be double checked now
	if not is_space_full(USB_DRIVE_CAPACITY, USB_DRIVE_MOUNT_POINT):
		# Now find the converted video, instead of raw video file
		outputs = [ output.split(CAPTURES_DIR)[1].split(OUTPUT_FORMAT)[0] for output in glob.glob(OUTPUT_REGEX) ]
		dates = []
		for output in outputs:
			try:
				dates.append(datetime.strptime(output, VIDEO_FILE_NAME_FORMAT))
			except ValueError:
				continue

		# Something is wrong, cannot find any converted video file
		if not dates:
			sys.exit(1)
		
		# Check if any video is in need of outputting, starting from earliest one
		output_source = CAPTURES_DIR + min(dates).strftime(VIDEO_FILE_NAME_FORMAT) + OUTPUT_FORMAT
		output_raw = CAPTURES_DIR + min(dates).strftime(VIDEO_FILE_NAME_FORMAT) + CAPTURES_FORMAT
		output_target = USB_DRIVE_MOUNT_POINT + min(dates).strftime(VIDEO_FILE_NAME_FORMAT) + OUTPUT_FORMAT

		# Remove corresponding raw file
		try:
			os.remove(output_raw)
		except OSError:
			print "Unable to delete raw video file " + output_raw
		
		# Actual outputting
		try:
			copyfile(output_source, output_target)
		except IOError:
			print "Error"
			sys.exit(1)

		# Remove source video file
		try:
			os.remove(output_source)
		except OSError:
			print "Error"
			sys.exit(1)
	
		print "finally"
