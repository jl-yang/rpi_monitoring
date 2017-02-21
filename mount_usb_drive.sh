# format
sudo mkfs -t vfat -I /dev/sda1

# create dir if not exists
mkdir -p /mount/usb

# mount
sudo mount -t vfat /dev/sda1 /mount/usb

# unmount
sudo unmount /mount/usb
