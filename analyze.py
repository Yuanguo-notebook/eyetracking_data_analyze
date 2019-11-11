################################################
## analyze hitting points
################################################

import matplotlib.pyplot as plt
import csv
import os
import  sys
import json
from shapely.geometry import Point, Polygon

# im = plt.imread('flipped_out.jpg')
# implot = plt.imshow(im)

# '''
# read hitting points file
dirname = sys.argv[1]
print ("the folder has the name %s" % (dirname))
file_list = os.listdir(dirname)
print('This folder has ', file_list, ' files.')
diction = {}
for file_name in file_list:
    if 'xml' in file_name:
        f = open(dirname + '/'+file_name.split('.')[0] + '.csv', 'r',  encoding="utf-8")
        reader = csv.reader(f)
        for row in reader:
            diction[int(row[0])] = [float(row[1]), float(row[2])]


f.close()

print(len(diction))
# '''



# read polygon file
with open('image56.json') as f:
    d = json.load(f)
    points = d['shapes'][0]['points']
    # print('points')
    print(points)

point_list = []
for point in points:
    point_list.append((point[0], point[1]))
print(point_list)

# Create a Polygon
poly = Polygon(point_list)

#  longest duration of time spent looking at the suspect
def fixation():
    start = 0
    end = 0
    length = 0
    # check if points is polygon
    for key, value in diction.items():
        p1 = Point(value[0], value[1])

        if p1.within(poly) == True:
            if start == 0:
                start = int(key)
            else:
                end = int(key)
        else:
            if end - start > length:
                length = end - start
            start = 0
            end = 0

    return length / 1000

# This could simply be calculated as the number of seconds spent looking at the suspect divided by 30
def percentage_of_time_on_suspect():

    count = 0

    for key, value in diction.items():
        p1 = Point(value[0], value[1])

        if p1.within(poly) == True:
            count += 1


    return count / len(diction)


def returns_to_suspect():
    flag = False
    count = 0
    # check if points is polygon
    for key, value in diction.items():
        p1 = Point(value[0], value[1])

        if p1.within(poly) == True and flag == True:
            flag = False

            count += 1

        else:
            flag = True
    return count
print(returns_to_suspect())


# plt.scatter([value[0]], [value[1]], s=1, color='r')
# plt.show()







print('finish')



