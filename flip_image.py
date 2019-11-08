from PIL import Image
import sys
import os


dirname = sys.argv[1] + '/' + 'crop'
print ("the script has the name %s" % (dirname))
file_list = os.listdir(dirname)

output_path = '/'.join(dirname.split('/')[:-1]) + '/' + 'flip' + '/'

os.makedirs(output_path )
print(file_list)
for image_path in file_list:


    image_obj = Image.open(dirname +'/'+ image_path)
    rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_image.save(output_path + image_path)
    # rotated_image.show()


