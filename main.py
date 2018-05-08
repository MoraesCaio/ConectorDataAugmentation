import os
import sys
from dip import ImageMatrix
import dataAug


filename = sys.argv[1]

img = ImageMatrix.from_file(filename)
dataAug.generate_sample(img, 224).show(filename)

print('Finished.')
