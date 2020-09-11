################################################
## Convert xml to mat file for pupil blinks
## Created by Yuanguo Lang on 06/17/2020
## All rights reserved
################################################
import pandas as pd

import sys
import os

sys.path.insert(0, '/Users/yuanguo/MHC/BEARS LAB')
print(sys.path)
import xml.etree.ElementTree as ET
import csv

# PUF WSU DATA 2 (len=3); WSU21 ; SUMMER
dirname = '/Users/yuanguo/MHC/BEARS LAB/data/SUMMER' # PUF WSU DATA see readme folder structure, dir should contain 001 002

print ("the folder has the name %s" % (dirname))

tobii_folder_name = 'ED'
tobii_path = ''
participants_files = os.listdir(dirname)
participants_files.sort()

for par_id in participants_files:
    # files are 001, 002
    print(par_id)

    if len(par_id) == 7:
        single_par_folder = os.listdir(dirname + '/' + par_id)
        print(single_par_folder)
        for single_file in single_par_folder:
            if tobii_folder_name in single_file and 'EYE' not in single_file:
                tobii_path = dirname  + '/' + par_id + '/' + single_file

                print('current in : '+tobii_path)
                file_list = os.listdir(tobii_path)
                file_list.sort()
                # print('This folder has ', file_list, ' files.')
                f = open(tobii_path + '/' + 'pupil' + '.csv', 'w', encoding="utf-8")
                writer = csv.writer(f)
                for file_name in file_list:
                    if 'xml' in file_name:
                        print(file_name)
                        tree = ET.parse(tobii_path + '/'+file_name)
                        root = tree.getroot()
                        pupilDiameters = []
                        for child in root:
                            timestamp = child.attrib['TimeStamp']
                            for c in child:
                                if 'Left' in c.tag:
                                    for son in c:
                                        if 'PupilDiameter' in son.tag:

                                            pupilDiameters.append(son.attrib['Value'])
                        writer.writerow(pupilDiameters)



                # f.close()

print('All finish')