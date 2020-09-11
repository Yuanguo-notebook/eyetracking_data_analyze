from based_noise_blinks_detection import based_noise_blinks_detection
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

import csv
def countzero(t):
	c = 0
	for i in t:
		if i == 0:
			c += 1
	if c != 0:
		print('c: ',c)

f = open('participants_pupil' + '.csv', 'a', encoding="utf-8")
writer = csv.writer(f)
for i in range(21, 56):
	print("{0:0=2d}".format(i))
	# # PUF WSU DATA 2 (len=3); WSU21 ; SUMMER
	filename = '/Users/yuanguo/MHC/BEARS LAB/data/WSU21/PUF_0' + '{0:0=2d}'.format(i) + '/PUF_0'+'{0:0=2d}'.format(i)+'_ED'+'/pupil.csv'
	print(filename)
	with open(filename, newline='') as csvfile:
		data = list(csv.reader(csvfile))
	pupilDiameters = []


	for i in range(14):
		temp = np.array(data[i], dtype="float32")*1000
		where_are_NaNs = np.isnan(temp)
		temp[where_are_NaNs] = 0
		temp = np.transpose(temp)
		temp = np.rint(temp)


		blinks = based_noise_blinks_detection(temp, 500)

		c = np.empty((len(blinks["blink_onset"]) + len(blinks["blink_offset"]),))
		c[0::2] = blinks["blink_onset"]
		c[1::2] = blinks["blink_offset"]
		print(c)
		print(i, len(c)/2)
		pupilDiameters.append(str(int(len(c)/2)))
	writer.writerow(pupilDiameters)

