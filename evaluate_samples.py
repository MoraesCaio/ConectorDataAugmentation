import os
import sys
from dip import ImageMatrix
import dataAug


good_cases_num, bad_cases_num = 0, 0

directory = sys.argv[1] if sys.argv[1].endswith('/') else sys.argv[1] + '/'
print(directory)
good_ones = 'good/'
bad_ones = 'bad/'

os.makedirs(directory+good_ones, exist_ok=True)
os.makedirs(directory+bad_ones, exist_ok=True)

for filename in os.listdir(directory):
    if filename.endswith('.jpg') or \
       filename.endswith('.png'):
        
        img = ImageMatrix.from_file(directory+filename)

        resize_ratios = dataAug.get_valid_resize_ratios(img)

        if len(resize_ratios) == 0:
            bad_cases_num += 1
            os.rename(directory+filename, directory+bad_ones+filename)
            
            print('Couldn\'t find valid resize ratio.')
        
        else:
            good_cases_num += 1
            os.rename(directory+filename, directory+good_ones+filename)
            print('Found a good sample.')

            resized = img.resize(ratio=resize_ratios[-1])

            for i in range(1):
                a = dataAug.generate_sample(resized, 224, proportion=0.9)
                # a.show('NEW SAMPLE')

print('Successful: ' + str(good_cases_num))
print('Failed: ' + str(bad_cases_num))
