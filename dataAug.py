import numpy as np
from PIL import Image
from dip import ImageMatrix
import cv2
import random


# sat_tolerance MUST HAVE an equal, or greater, value on generate_sample()'s call than the one used on get_valid_resize_ratios()'s call.
#  Otherwise, it probably won't find the same contours.

def get_valid_resize_ratios(img_mtx, sat_tolerance=0, start=.15, stop=.21, step=.005, verbose=0, show=False):
    fl_lst = []
    
    for i in np.arange(start, stop, step):
        resized = img_mtx.resize(ratio=i)
        rotated = resized.crop_max_contour()
        median = rotated.get_median_rgb_value()[:3]
        
        if verbose >= 2:
            print('Checking resized image with ratio == ' + "{0:.2f}".format(i) + ' Shape' + str(resized.shape))
        
        # Check if median color is not black
        #  and if the difference between channels is greater the sat_tolerance
        #   (for avoiding nearly monochromatic images)
        if (median != np.array([0, 0, 0])).all() and \
            np.absolute(median[0]-median[1]) >= sat_tolerance and \
            np.absolute(median[1]-median[2]) >= sat_tolerance and \
            np.absolute(median[2]-median[0]) >= sat_tolerance:
            
            fl_lst.append(i)
            
            if verbose >= 1:
                print('OK: Shape'+str(resized.shape)+' ratio = '+"{0:.2f}".format(i))
            if show:
                rotated.show('Crop without filling')

    return fl_lst

def generate_sample(img_mtx, dim, sat_tolerance=0, proportion=0.9, tup2_resize=(0.95, 1.05), tup2_rotation=(-10, 10), tup2_shine=(0.7, 1.05)):
    # Condition to make the function less error prone
    if dim % 4:
        raise Exception('Dimension should be multiple of 4.')
    
    # Resizing beyond 2 times may cause the image to be greater than the output canvas
    if tup2_resize[1] >= 2.:
        raise Exception('Maximum possible resize factor ('+str(tup2_resize[1])+') is error prone.')

    # Get a valid random resize factor
    min_resize, max_resize = tup2_resize[0], tup2_resize[1]
    valid_ratios = get_valid_resize_ratios(img_mtx, sat_tolerance, start=min_resize, stop=max_resize)
    if len(valid_ratios) == 0:
        raise Exception('Could not found a valid resize ratio for this image. Try to resize it before running this function again.')
    rnd_resize = random.choice(valid_ratios)
    
    # Get random rotation angle
    min_rotation, max_rotation = tup2_rotation[0], tup2_rotation[1]
    rnd_rotation = int(np.random.uniform(min_rotation, max_rotation+1))
    
    # Get random shine factor
    min_shine, max_shine = tup2_shine[0], tup2_shine[1]
    rnd_shine = np.random.uniform(min_shine, max_shine)

    # Creating black canvas
    background = np.ones((dim, dim, img_mtx.shape[2]), dtype='uint8') * 255
    background[:, :, :3] = 0

    # Applying random rotation
    rnd_rotated = img_mtx.rotate_cropping(rnd_rotation)

    # Adjusting to fit in canvas
    largest = rnd_rotated.shape[1] if rnd_rotated.shape[1] > rnd_rotated.shape[0] else rnd_rotated.shape[0]
    resize_ratio = dim/(1/proportion)/largest
    resized = rnd_rotated.resize(ratio=resize_ratio)

    # Applying random rotation
    rnd_resized = resized.resize(ratio=rnd_resize)
    
    # Finding suitable location to place the resulting image
    x = (dim - rnd_resized.shape[1])//2
    y = (dim - rnd_resized.shape[0])//2

    # Applying random rotation
    new_shine = rnd_resized.multiply_shine(rnd_shine)

    # Placing resulting image on canvas
    background[y:y+new_shine.shape[0], x:x+new_shine.shape[1]] = new_shine

    return background.view(ImageMatrix)
