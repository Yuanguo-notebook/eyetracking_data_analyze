import pandas as pd
import  os
import statistics
from collections import Counter
import numpy as np


def centroid(gridid):
    grid_dict = {i: gridid.count(i) for i in set(gridid)}
    sum_v = sum(grid_dict.values())
    grid_perc = {i: grid_dict[i] / sum_v for i in grid_dict.keys()}

    centroid = 0
    for i in grid_perc.keys():
        centroid += np.log10(grid_perc[i]) * grid_perc[i]
        # print('p: ', grid_perc[i], 'log10(p): ', np.log10(grid_perc[i]), 'np.log10(p) * p: ', np.log10(grid_perc[i]) * grid_perc[i])
    centroid = centroid * -1
    print(grid_perc)
    print('centroid now: ', centroid)
    return centroid


par_dict = {}
participants = pd.DataFrame()

data_dir_name = '/Users/yuanguo/MHC/BEARS LAB/data/SUMMER' #WSU21'
print ("the folder is %s" % (data_dir_name))


participants_ids = os.listdir(data_dir_name)
participants_ids.sort()
# opens eye tracking data folder which contains
# 2d hitting points we just generated
for par_id in participants_ids:
    print(par_id)
    # files are 001, 002
    if len(par_id) == 7:
        par_dict['id'] = par_id
        single_par_folder = os.listdir(data_dir_name + '/' + par_id)
        hit_folder_path = data_dir_name + '/' + par_id +'/'+ par_id+'_HIT'
        print(hit_folder_path)
        hit_files = os.listdir(hit_folder_path)
        for hit_file in hit_files:
            if 'centroid' in hit_file:
                raw = pd.read_csv(hit_folder_path + '/' + hit_file, delimiter=',')
                # print(raw.head())
                curr_cdist = list(raw['cdist'])



                pst = statistics.pstdev(curr_cdist)
                st = statistics.stdev(curr_cdist)
                mean = statistics.mean(curr_cdist)
                par_dict['pst'] = pst
                par_dict['st'] = st
                par_dict['mean'] = mean

                num_interval = 3
                unit_len = len(curr_cdist) / num_interval
                for i in range(num_interval):
                    par_dict[str('pst'+str(i))] = statistics.pstdev(curr_cdist[int(i*unit_len) : int((i+1)*unit_len)])
                    par_dict[str('st'+str(i))] = statistics.stdev(curr_cdist[int(i*unit_len) : int((i+1)*unit_len)])
                    par_dict[str('mean'+str(i))] = statistics.mean(curr_cdist[int(i*unit_len) : int((i+1)*unit_len)])



                temp_gridid = list(raw['gridid'])

                curr_gridid = [x for x in temp_gridid if str(x) != 'nan']
                sum_centroid = centroid(curr_gridid)
                par_dict['centroid'] = sum_centroid
                for i in range(num_interval):

                    temp_centroid = centroid(curr_gridid[int(i*unit_len) : int((i+1)*unit_len)])
                    par_dict[str('centroid'+str(i))] = temp_centroid
                print(par_dict)

        participants = participants.append(par_dict, ignore_index=True)
        # assert (False)
        participants.to_csv('participants_scene4_interval_690.csv', sep=',')

print('finish')