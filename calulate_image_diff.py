import dhash
from wand.image import Image


with Image(filename='/home/pi/image_2018-09-30_00-59-07_000000028.jpg') as img:
    row, col = dhash.dhash_row_col(img)
print(dhash.format_hex(row, col))

print("\n")

with Image(filename='/home/pi/image_2018-09-30_00-59-07_000000029.jpg') as img:
    row, col = dhash.dhash_row_col(img)
print(dhash.format_hex(row, col))
