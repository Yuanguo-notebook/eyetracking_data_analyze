import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from csaps import csaps
import csv
from based_noise_blinks_detection import based_noise_blinks_detection


f = open('participants_pupil' + '.csv', 'a', encoding="utf-8")
writer = csv.writer(f)
for j in range(1, 21):

    print("{0:0=2d}".format(j))
    # # PUF WSU DATA 2 (len=3); WSU21 ; SUMMER
    # filename = '/Users/yuanguo/MHC/BEARS LAB/data/WSU21/PUF_0' + '{0:0=2d}'.format(i) + '/PUF_0'+'{0:0=2d}'.format(i)+'_ED'+'/pupil.csv'
    filename = '/Users/yuanguo/MHC/BEARS LAB/data/PUF WSU DATA 2/0' + '{0:0=2d}'.format(j) + '/WSU_ED_0' + '{0:0=2d}'.format(
        j) + '/pupil.csv'

    print(filename)
    with open(filename, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    for i in range(14):

        pupilDiameters = []
        print('current: ', j, i)
        temp = np.array(data[i], dtype="float32") * 1000
        n = temp.shape[0]
        x = np.linspace(0.0, n - 1, n)
        where_are_NaNs = np.isnan(temp)
        temp[where_are_NaNs] = 0
        temp = np.transpose(temp)
        y = temp

        temp = np.rint(temp)

        blinks = based_noise_blinks_detection(temp, 600)

        c = np.empty((len(blinks["blink_onset"]) + len(blinks["blink_offset"]),))
        c[0::2] = blinks["blink_onset"]
        c[1::2] = blinks["blink_offset"]
        print(c)

        # remove blinks
        x_clean = x
        y_clean = y
        delete_range = np.array([])
        for i in range(int(c.shape[0] / 2)):
            delete_range = np.append(delete_range, np.linspace(c[2 * i]-1, c[2 * i + 1]-1, int(c[2 * i + 1] - c[2 * i] + 1)))
        delete_range = delete_range.astype(int)

        x_clean = np.delete(x_clean, delete_range)
        y_clean = np.delete(y_clean, delete_range)

        # use cubic spline
        spline = csaps(x_clean, y_clean)
        xi1 = np.linspace(x[0], x[-1], n)
        yi1 = spline(xi1)
        mean = np.mean(yi1)
        std = np.std(yi1)

        pupilDiameters.append(mean)
        pupilDiameters.append(std)
        print(pupilDiameters)
        writer.writerow(pupilDiameters)

        f, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 7))
        ax1.plot(x, y, 'o')
        for i in range(int(c.shape[0] / 2)):
            ax1.axvspan(c[2 * i], c[2 * i + 1], color='red', alpha=0.5)

        ax2.plot(x_clean, y_clean, 'o', xi1, yi1, '.-')

        f.savefig(str(j)+'_'+str(i)+'.png')
        plt.close(f)
    assert (False)