import numpy as np
import matplotlib.pyplot as plt
import csv
import seaborn as sns
import matplotlib.colors as mcolors

colors = [(1,0,0,c) for c in np.linspace(0,1,100)]
cmapred = mcolors.LinearSegmentedColormap.from_list('mycmap', colors, N=5)



im = plt.imread('scene3/image00.jpg')
x = []
y = []

time_eye_dict = {}
f = open('scene3/scene3.csv', 'r', encoding="utf-8")
reader = csv.reader(f)

for row in reader:
    x.append(float(row[1]))
    y.append(float(row[2]))

plt.imshow(im)
plt.hist2d(x,y, bins=[np.arange(0,3840,5),np.arange(0,1080,5)], alpha = 1, cmap=cmapred)
plt.gca().invert_yaxis()

plt.show()
# plt.savefig('scene3/heat1.jpg')
