################################################
## convert xml to hitting points with csv file
################################################


import sys
import os
#
# sys.path.append('/Users/yuanguo/MHC/BEARS\ LAB/sphere_to_cubemap')
sys.path.insert(0, '/Users/yuanguo/MHC/BEARS LAB')
print(sys.path)
import xml.etree.ElementTree as ET
import math
from sphere_to_cubemap.sphere import Sphere

# geom3 adopted from https://github.com/phire/Python-Ray-tracer
from sphere_to_cubemap.geom3 import Vector3, Point3, Ray3, dot, unit
from math import sqrt
from sphere_to_cubemap.hit import Hit
import numpy  as np

from pyquaternion import Quaternion
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting
from sphere_to_cubemap.angles import *
from PIL import Image

import csv

# map equirectangular image to sphere
# adopted from https://stackoverflow.com/questions/53074908/map-an-image-onto-a-sphere-and-plot-3d-trajectories
count = 3000
def mpl_sphere(image_file):
    img = plt.imread(image_file)

    # define a grid matching the map size, subsample along with pixels
    # evenly create img.shape[0 number of points between 0  and pi
    theta = np.linspace(0, np.pi, img.shape[0])
    phi = np.linspace(0, 2*np.pi, img.shape[1])



    # count = 3000 # keep 45 points along theta and phi
    # get index evenly for 45 points
    theta_inds = np.linspace(0, img.shape[0] - 1, count).round().astype(int)
    phi_inds = np.linspace(0, img.shape[1] - 1, count).round().astype(int)

    # get value for 45 points
    theta = theta[theta_inds]
    phi = phi[phi_inds]

    # recreate image
    img = img[np.ix_(theta_inds, phi_inds)]
    # image = Image.fromarray(img, 'RGB')
    # image.show()


    theta,phi = np.meshgrid(theta, phi)

    R = 1


    # sphere to xyz
    x = R * np.sin(theta) * np.cos(phi)
    y = R * np.sin(theta) * np.sin(phi)
    z = R * np.cos(theta)



    return theta,phi


#check if point is on surface of sphere
def check_point_on_sphere(cx, cy, cz, point, r):

    x1 = math.pow((point[0] - cx), 2)
    y1 = math.pow((point[1] - cy), 2)
    z1 = math.pow((point[2] - cz), 2)

    c = (x1 + y1 + z1) == math.pow(r, 2)
    if c == True:
        print("point: ", point, " lies on sphere: ", cx, cy, cz)
    else:
        print("point: ", point, " does not lies on sphere!!: ", cx, cy, cz, ", diff: ", (x1 + y1 + z1 - math.pow(r, 2)))
    return c

'''
let's get the hitting point by pose, camera rotation and gazeRay


'''

center = [0, 0, 0]

image_file = 'flipped_out.jpg'
theta,phi = mpl_sphere(image_file)

# switch y and z axis
def unity_to_python_point(old):

    y = old[1]
    z = old[2]
    old[1] = z
    old[2] = y

    return old



# rotate a vector by quaternion rotation
# https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
def rotate_vec_by_quaternion(quat, vec):
    quatx = quat[0]
    quaty = quat[1]
    quatz = quat[2]
    quatw = quat[3]

    x = vec[0]
    y = vec[1]
    z = vec[2]


    result_x = (1 - 2*(quaty**2)-2*(quatz**2))*x + (2*quatx*quaty-2*quatz*quatw)*y + (2*quatx*quatz+2*quaty*quatw)*z
    result_y = (2*quatx*quaty+2*quatz*quatw)*x + (1-2*(quatx**2)-2*(quatz**2))*y + (2*quaty*quatz-2*quatx*quatw)*z
    result_z = (2*quatx*quatz-2*quaty*quatw)*x + (2*quaty*quatz+2*quatx*quatw)*y + (1-2*(quatx**2)-2*(quaty**2))*z
    result = np.array([0.0, 0.0, 0.0])
    result[0] = result_x
    result[1] = result_y
    result[2] = result_z
    return result

# use start point and ray vector to get hitting point on sphere
# draw that gaze vector
def get_hit_point_draw(combined_ray, linecolor):
    start = np.array([0.0, 0.0, 0.0])

    rot = np.array([0.0, 1.0, 0, 0.0])
    # rotate a vector by quaternion rotation
    dir = rotate_vec_by_quaternion(rot, combined_ray)
    end = start + dir

    #get hitting point
    sphere = Sphere(Point3(0,0,0), 1, None)
    ray = Ray3(Point3(start[0], start[1], start[2]), Vector3(dir[0], dir[1], dir[2]))
    hitpoint = sphere.intersect(ray)

    #check if hitting point is on sphere surface
    # check_point_on_sphere(0, 0, 0, hitpoint, 1)

    # convert unity coordinate to python coordinate
    unity_to_python_point(start)
    unity_to_python_point(end)
    unity_to_python_point(hitpoint)

    return hitpoint




# transforms a point on sphere to a point in equirectangular
# geo_w, geo_h are final projection width and length

def transform_to_equirectangular(point, geo_w, geo_h, color):

    # from -pi to pi, so need to add 2pi if it is negative
    phi_value = math.atan2(point[1], point[0])
    theta_value = math.acos(point[2])
    if phi_value <0 :
        phi_value += 2*np.pi

    # get index of current theta value
    theta_index = int(count * (theta_value / np.pi))
    phi_index = int(count * (phi_value / (2 * np.pi)))


    # get the transpose value for theta and phi
    theta_value2 = theta[0][int(phi_index)]
    phi_value2 = phi[theta_index][0]

    # project back to equirectangular
    geo_x_px = ( theta_value2 / np.pi )* geo_w
    geo_y_px = (phi_value2 / (2*np.pi)) * geo_h

    # plt.scatter([geo_x_px], [geo_y_px], s=40, color=color)
    return [geo_x_px, geo_y_px]

# im = plt.imread('flipped_out.jpg')
# implot = plt.imshow(im)


dirname = sys.argv[1]
print ("the folder has the name %s" % (dirname))
file_list = os.listdir(dirname)
print('This folder has ', file_list, ' files.')

for file_name in file_list:
    if 'xml' in file_name:
        f = open(dirname + '/'+file_name.split('.')[0] + '.csv', 'w',  encoding="utf-8")
        writer = csv.writer(f)



        tree = ET.parse(dirname + '/'+file_name)
        root = tree.getroot()

        for child in root:
            timestamp = child.attrib['TimeStamp']
            for c in child:

                if 'CombinedGazeRayWorld' in c.tag:
                    # print(c.attrib)
                    # print(c.attrib['Direction'])
                    str_list = c.attrib['Direction'][1:-1].split(', ')
                    combined_ray = np.array([0.0, 0.0, 0.0])
                    for m in range(3):
                        combined_ray[m] = str_list[m]
                    hitpoint_wheel = get_hit_point_draw(combined_ray, 'g')
                    projPoint_w = transform_to_equirectangular(hitpoint_wheel, 3840, 1080, 'g')
                    # f.write(timestamp + '|' + str(projPoint_w[0]) + ',' + str(projPoint_w[1]) + '\n')
                    writer.writerow([timestamp, str(projPoint_w[0]), str(projPoint_w[1])])

f.close()
print('finish')

# plt.show()








