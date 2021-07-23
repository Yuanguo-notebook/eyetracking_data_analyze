################################################
## 1.convert xml to hitting points with csv file
################################################
import pandas as pd

import sys
import os


import xml.etree.ElementTree as ET
import math
from sphere import Sphere

# geom3 adopted from https://github.com/phire/Python-Ray-tracer
from geom3 import Vector3, Point3, Ray3, dot, unit
from math import sqrt

import numpy  as np

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting
# from sphere_to_cubemap.angles import *
from PIL import Image

import csv



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
    sphere = Sphere(Point3(0,0,0), 1)
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
    theta_value = math.atan2(point[1], point[0])
    phi_value = math.acos(point[2])
    if phi_value <0 :
        phi_value += np.pi

    if theta_value <0 :
        theta_value += 2*np.pi

    # project back to equirectangular
    geo_x_px = (theta_value / (2 * np.pi)) * geo_w
    geo_y_px = (phi_value / (np.pi)) * geo_h

    return [geo_x_px, geo_y_px]


dirname = sys.argv[1] # PUF WSU DATA see readme folder structure, dir should contain 001 002

print ("the folder has the name %s" % (dirname))

tobii_folder_name = 'WSU_ED'
tobii_path = ''
participants_files = os.listdir(dirname)
for par_id in participants_files:
    # files are 001, 002
    if len(par_id) == 3:
        single_par_folder = os.listdir(dirname + '/' + par_id)
        for single_file in single_par_folder:
            if tobii_folder_name in single_file:
                tobii_path = dirname  + '/' + par_id + '/' + single_file
                # create folder for coordinate on 2d image
                os.mkdir(tobii_path + '_EYE2')
                print('current in : '+tobii_path)
                file_list = os.listdir(tobii_path)
                # print('This folder has ', file_list, ' files.')

                for file_name in file_list:
                    if 'xml' in file_name:
                        f = open(tobii_path +'_EYE2'+ '/'+file_name.split('.')[0] + '.csv', 'w',  encoding="utf-8")
                        writer = csv.writer(f)

                        tree = ET.parse(tobii_path + '/'+file_name)
                        root = tree.getroot()

                        for child in root:
                            timestamp = child.attrib['TimeStamp']
                            for c in child:

                                if 'CombinedGazeRayWorld' in c.tag:
                                    str_list = c.attrib['Direction'][1:-1].split(', ')
                                    combined_ray = np.array([0.0, 0.0, 0.0])
                                    for m in range(3):
                                        combined_ray[m] = str_list[m]
                                    hitpoint_2d = get_hit_point_draw(combined_ray, 'g')
                                    projPoint_w = transform_to_equirectangular(hitpoint_2d, 3840, 1080, 'g')
                                    writer.writerow([timestamp, str(projPoint_w[0]), str(projPoint_w[1])])

                        f.close()

print('All finish')










