import os
import sys
from dip import ImageMatrix
import dataAug


filename = sys.argv[1]

img = ImageMatrix.from_file(filename)
resize_ratios = dataAug.get_valid_resize_ratios(img)

if len(resize_ratios):
    dataAug.generate_sample(img.resize(ratio=resize_ratios[-1]), 224).show(filename)
else:
    print('Could not find a valid contour.')

print('Finished.')
