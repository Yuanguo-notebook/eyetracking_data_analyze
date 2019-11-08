from PIL import Image
import sys
import os


dirname = sys.argv[1] + '/' + 'frames'
print ("the script has the name %s" % (dirname))
file_list = os.listdir(dirname)

output_path = '/'.join(dirname.split('/')[:-1]) + '/' + 'crop' + '/'

os.makedirs(output_path )
print(file_list)
for img_name in file_list:


    # Opens a image in RGB mode
    im = Image.open(dirname +'/'+ img_name)

    # Size of the image in pixels (size of orginal image)
    # (This is not mandatory)
    width, height = im.size

    # Setting the points for cropped image
    left = 0
    top = 0
    right = width
    bottom =  height / 2

    # Cropped image of above dimension
    # (It will not change orginal image)
    im1 = im.crop((left, top, right, bottom))

    # Shows the image in image viewer
    im1.save(output_path + img_name)