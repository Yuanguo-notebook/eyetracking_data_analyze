################################################
## 2. analyze hitting points
## get data of which object they are looking at
################################################

import matplotlib.pyplot as plt
import csv
import os
import  sys
import json
from shapely.geometry import Point, Polygon
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

################################################
# global variables
################################################
interval = 500000 # half second
scene_dict = {0:'p1', 1:'p2', 2:'scene1',  3:'scene2', 4:'scene3', 5:'scene4', 6:'scene5', 7:'scene6', 8:'scene7', 9:'scene8', 10:'scene9', 11:'scene10', 12:'scene11', 13:'scene12'}
id_set_dict = {'A': 1, 'B':2}
stamp1 = pd.read_csv("stamps/stamp1.csv")
stamp2 = pd.read_csv("stamps/stamp2.csv")
count = 0
centroid_labels = ['man', 'woman']
centroid_distance_label = 'cdist'
grid_label = 'gridid'
################################################
# remove string does not contain sym from list
################################################
def remove_from_list(alist, sym):
    for item in alist:
        if sym not in item:
            alist.remove(item)

################################################
# include string contain sym from list
################################################
def include_to_list(alist, sym):
    temp = []
    for item in alist:
        if sym  in item:
            temp.append(item)
    return temp


################################################
# convert a list of list to a list of tuple
################################################
def convert_to_tuple_list(alist):
    temp = []
    for item in alist:

        temp.append(tuple(item))
    return temp

################################################
# convert rectangle(2 points) to polygon (4points)
################################################
def convert_to_box(points):
    temp = []
    t1 = points[0]
    t2 = points[1]
    if t1[0] < t2[0]:
        x1 = t1[0]
        x2 = t2[0]
    else:
        x2 = t1[0]
        x1 = t2[0]
    if t1[1] < t2[1]:
        y1 = t1[1]
        y2 = t2[1]
    else:
        y2 = t1[1]
        y1 = t2[1]

    temp.append((x1, y1))
    temp.append((x2, y1))
    temp.append((x2, y2))
    temp.append((x1, y2))


    return temp


################################################
#middle point of two Point (shapely.geometry)
# return Point
################################################
def find_middle_point(p1, p2):
    x = (p1.x + p2.x) / 2
    y = (p1.y+ p2.y) / 2
    return Point(x, y)


################################################
# find max and min in a list
# return (max, min)
################################################
def find_max_min(l1):
    return (max(l1), min(l1))

################################################
# check input dot in which cell out of 16
# cell id
################################################
def check_which_cell(x_ref, y_ref, target):
    x_result = 0
    y_result = 0
    if target.x >= x_ref[-1] or target.y >= y_ref[-1] :
        return 'NA'
    if target.x < x_ref[0] or target.y  < y_ref[0] :
        return 'NA'
    for xr in range(len(x_ref)):
        if target.x >= x_ref[xr] and target.x  < x_ref[xr+1]:
            x_result = xr
    for yr in range(len(y_ref)):
        if target.y >= y_ref[yr] and target.y  < y_ref[yr+1]:
            y_result = yr

    return x_result, y_result



# print(os.listdir('/Users/yuanguo/MHC/BEARS LAB/images/demo1/scene1/flip'))
# assert (False)


annot_dir = '/Users/yuanguo/MHC/BEARS LAB/images/demo'
data_dir_name = '/Users/yuanguo/MHC/BEARS LAB/data/SUMMER'
print ("the folder is %s" % (data_dir_name))

tobii_eye_folder_name = 'EYE2'
tobii_path = ''
participants_ids = os.listdir(data_dir_name)
participants_ids.sort()
# opens eye tracking data folder which contains
# 2d hitting points we just generated
for par_id in participants_ids:
    # files are 001, 002
    if len(par_id) == 7:
        single_par_folder = os.listdir(data_dir_name + '/' + par_id)
        hit_folder_path = data_dir_name + '/' + par_id +'/'+ par_id+'_HIT'
        print(hit_folder_path)

        if not os.path.exists(hit_folder_path):
            os.makedirs(hit_folder_path)
        for single_file in single_par_folder:
            if tobii_eye_folder_name in single_file:
                tobii_path = data_dir_name + '/' + par_id + '/' + single_file
                print('current in : '+tobii_path)     #/.../WSU_ED_001_EYE
                file_list = os.listdir(tobii_path)
                remove_from_list(file_list, 'csv')
                file_list.sort()                    # sort by time
                print('This folder has ', len(file_list), ' files: ',file_list )
                # we only check scene4
                i = 5
                # read timestamp and hitting point csv file
                time_eye_dict = {}
                f = open(tobii_path + '/' + file_list[i], 'r', encoding="utf-8")
                reader = csv.reader(f)
                start_timestamp = 0
                for row in reader:
                    if start_timestamp ==0:
                        start_timestamp = int(row[0])
                    time_eye_dict[int(row[0])] = [float(row[1]), float(row[2])]


                # read annotation files
                # find which set this participant was using setA or setB
                # result = pd.read_csv("result.csv")
                # set = result['set'][np.where(result['id'] == int(par_id))[0][0]]
                # if set == 'A':
                #     df = stamp1
                # else:
                #     df = stamp2

                result = pd.read_csv("PUF_result.csv")
                set = result['Set '][np.where(result['New ID'] == par_id)[0][0]]
                if set == 1:
                    df = stamp1
                    set = 'A'
                elif set == 2:
                    df = stamp2
                    set = 'B'
                print('id: ',par_id,', set: ', set, ', i: ', i)


                annot_dir_curr = annot_dir + str(id_set_dict[set])

                # find which scene
                curr_scene = scene_dict[i]
                annot_dir_curr = annot_dir_curr + '/'+curr_scene + '/' + 'flip'

                poly_file_names = os.listdir(annot_dir_curr)
                poly_json_file_names = include_to_list(poly_file_names, 'json')
                poly_json_file_names.sort()



                result_scene_dict = {'timestamp':[], 'image':[]}
                for key, value in time_eye_dict.items():
                    hitting_point = Point(value[0], value[1])
                    # plt.scatter([value[0]], [value[1]], s=0.5, color='b')
                    curr_img = 'image'
                    curr_time = (key - start_timestamp) / interval
                    curr_time = int(curr_time)
                    num = ''

                    if curr_time <= df['start1'][i]*2:
                        num= str(curr_time).zfill(2)
                    elif df['start1'][i]*2 < curr_time < df['end1'][i]*2:
                        num= str(int(df['start1'][i]*2)).zfill(2)
                    elif df['end1'][i]*2 <= curr_time <= df['start2'][i]*2:
                        num= str(int(curr_time - 2*(df['end1'][i] - df['start1'][i]))).zfill(2)
                    elif df['start2'][i]*2 < curr_time < df['end2'][i]*2:
                        num = str(int(df['start2'][i]*2- 2*(df['end1'][i] - df['start1'][i]))).zfill(2)
                    elif curr_time >= df['end2'][i]*2 and df['end2'][i] != 0:
                        num = str(int(curr_time - 2 * (df['end2'][i] - df['start2'][i]) - 2*(df['end1'][i] - df['start1'][i]))).zfill(2)
                    elif curr_time >= df['end1'][i]*2 and df['start2'][i] == 0:
                        num = str(int(curr_time - 2*(df['end1'][i] - df['start1'][i]))).zfill(2)



                    result_scene_dict['timestamp'].append(key)
                    result_scene_dict['image'].append(num)


                    if os.path.exists(annot_dir_curr + '/' + curr_img+num + '.json'):
                        curr_img += num
                    else:
                        curr_img = prev
                    ###
                    flag_img = False
                    if flag_img == True:
                    # if os.path.exists('pics0303/'+curr_scene+'_'+curr_img+'.png') == False:

                        flag_img = True
                        plt.figure()
                        im = plt.imread(annot_dir_curr + '/' + curr_img + '.jpg')
                        fig, ax = plt.subplots(1)
                        ax.imshow(im)
                        plt.scatter([value[0]], [value[1]], s=5, color='g')
                    ####

                    with open(annot_dir_curr + '/' + curr_img + '.json') as img_f:
                        d = json.load(img_f)
                        # store center of man and center of woman
                        center_collection = []
                        x_collection = []
                        y_collection = []
                        x_reference = []
                        y_reference = []
                        for shape in d['shapes']:
                            points = shape['points']
                            points = convert_to_tuple_list(points)
                            label = shape['label']
                            # if label is man or woman
                            if label in centroid_labels:
                                if len(points) > 2:
                                    poly = Polygon(points)
                                else:
                                    poly = Polygon(convert_to_box(points))
                                # find center of polygon
                                x, y = poly.exterior.coords.xy
                                x_collection += list(x)
                                y_collection += list(y)
                                center_collection.append(poly.centroid)

                                ####
                                if flag_img ==True:

                                    x, y = poly.exterior.coords.xy
                                    draw_points = np.array([x, y], np.int32).T

                                    polygon_shape = patches.Polygon(draw_points, linewidth=1, edgecolor='r', facecolor='none')
                                    ax.add_patch(polygon_shape)
                                    plt.scatter(poly.centroid.x, poly.centroid.y, s=4, color='r')
                                ####
                        # find middle point of two centers
                        centroid = find_middle_point(center_collection[0], center_collection[1])
                        # distance between gaze and centroid
                        if centroid_distance_label not in result_scene_dict:
                            result_scene_dict[centroid_distance_label] = []
                        result_scene_dict[centroid_distance_label].append(hitting_point.distance(centroid))

                        # define grid
                        max_x, min_x = find_max_min(x_collection)
                        max_y, min_y = find_max_min(y_collection)
                        borders = (max_x, min_x, max_y, min_y)

                        for idx in range(5):
                            x_reference.append(min_x + (max_x - min_x) * 0.25 * idx)
                            y_reference.append(min_y + (max_y - min_y) * 0.25 * idx)
                        if grid_label not in result_scene_dict:
                            result_scene_dict[grid_label] = []
                        result_scene_dict[grid_label].append(check_which_cell(x_reference, y_reference, hitting_point))
                        prev = curr_img
                    ########
                    if flag_img ==True:
                        for u in range(5):
                            for v in range(5):
                                plt.scatter(x_reference[u], y_reference[v], s=2, color='b')
                        plt.scatter(centroid.x, centroid.y, s=4, color='r')
                        plt.savefig('pics0303/' + curr_scene+'_'+curr_img + '.png')
                        plt.close(fig)
                        count += 1

                    ########
                curr_df = pd.DataFrame(result_scene_dict)
                curr_df.to_csv(hit_folder_path + '/'+'centroid_' + file_list[i].split('.')[0]+'_'+curr_scene+'.csv', sep=',', encoding='utf-8')







print('finish')



