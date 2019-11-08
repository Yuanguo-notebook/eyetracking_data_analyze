import cv2
import sys
import os

filename = sys.argv[1]


vidcap = cv2.VideoCapture(filename)

foldername = 'frames'

output_path = '/'.join(filename.split('.')[0].split('/')[:-1]) + '/' + foldername + '/'

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