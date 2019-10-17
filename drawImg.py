import matplotlib.pyplot as plt

# draw dot on a image


steel = [2276.7941141185825, 451.90509750203773]
car = [2451.42114800506, 452.84288454418]
im = plt.imread('out.png')
implot = plt.imshow(im)
plt.scatter([steel[0]], [steel[1]], s=20, color='r')
plt.scatter([car[0]], [car[1]], s=20, color='b')
plt.show()