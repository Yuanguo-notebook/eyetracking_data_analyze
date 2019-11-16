import cv2
import sys
import os
from PIL import Image

filenamepath = sys.argv[1]
video_file_list = os.listdir(filenamepath)
videoname = ''
print(video_file_list)
for f in video_file_list:
    if 'mp4' in f:
        videoname = filenamepath + '/' + f



vidcap = cv2.VideoCapture(videoname)

framename = 'frames'
dirname = '/'.join(videoname.split('.')[0].split('/')[:-1])
output_path = dirname + '/' + framename + '/'

os.makedirs(output_path )
print(output_path)


def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(output_path + "image"+str("{0:02d}".format(count))+".jpg", image)     # save frame as JPG file
    return hasFrames
sec = 0
frameRate = 0.5 #//it will capture image in each 0.5 second
count=0
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)


# crop
framedirname = dirname + '/' + framename
print ("the script has the name %s" % (framedirname))
file_list = os.listdir(framedirname)

output_path = dirname + '/' + 'crop' + '/'

os.makedirs(output_path )
# print(file_list)
for img_name in file_list:

    if 'jpg' in img_name:
        # Opens a image in RGB mode
        im = Image.open(framedirname + '/' + img_name)

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


# flip
flipdirname = dirname + '/' + 'crop'
print ("the script has the name %s" % (flipdirname))
file_list = os.listdir(flipdirname)

output_path = dirname + '/' + 'flip' + '/'

os.makedirs(output_path )
# print(file_list)
for image_path in file_list:

    if 'jpg' in img_name:
        image_obj = Image.open(flipdirname + '/' + image_path)
        rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
        rotated_image.save(output_path + image_path)

print('finish this video')





