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


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

def draw_sphere(centre, radius):

    # draw sphere
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]

    sphere_x = centre[0] + radius * np.cos(u) * np.sin(v)
    sphere_y = centre[1] + radius * np.sin(u) * np.sin(v)
    sphere_z = centre[2] + radius * np.cos(v)
    ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color="r", alpha=.5)

def draw_point(vec_list):
        # draw a point
    for vec in vec_list:
        ax.scatter(vec[0], vec[1], vec[2], color="g", s=100)


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
draw_sphere(center, 1)



def get_hit_point_draw(start, rot, combined_ray, linecolor):

    q = Quaternion(rot)

    q = q.inverse
    print("rot: ", rot, ", q: ", q)
    dir = q.rotate(combined_ray)
    # np.pi is 180 !!

    end = start + dir


    sphere = Sphere(Point3(0,0,0), 1, None)
    ray = Ray3(Point3(start[0], start[1], start[2]), Vector3(dir[0], dir[1], dir[2]))
    hitpoint = sphere.intersect(ray)
    print("hit: ",hitpoint)
    check_point_on_sphere(0, 0, 0, hitpoint, 1)



    ax.scatter(start[0], start[1], start[2], color="g", s=10)
    ax.scatter(end[0], end[1], end[2], color="g", s=10)
    ax.scatter(hitpoint[0], hitpoint[1], hitpoint[2], color="b", s=10)
    ax.scatter(start[0]+1.0, start[1], start[2], color="k", s=10)

    ax.plot([start[0] , end[0]], [start[1],end[1]], [start[2],end[2]], color=linecolor)
    return hitpoint

# steering wheel: [2276.7941141185825, 451.90509750203773]
start = np.array([0.40181430, 0.26433430, 0.69292290])
rot = np.array([-0.01123296, 0.49509550, -0.07804342, 0.86525340])
combined_ray = np.array([0.83448750, -0.16063100, 0.52709410])

get_hit_point_draw(start, rot, combined_ray, 'r')

# police car [2451.42114800506, 452.84288454418]
start = np.array([0.31438190, 0.31822190, 0.40630990])
rot = np.array([-0.06771180, 0.98583170, 0.04554487, 0.14654910])
combined_ray = np.array([0.29111060, 0.03512534, -0.95604440])

hitpoint = get_hit_point_draw(start, rot, combined_ray, 'b')

plt.show()

'''
# transforms a point on sphere to a point in equirectangular
# geo_w, geo_h are final projection width and length
'''
def transform_to_equirectangular(point, geo_w, geo_h):
    theta = math.atan2(point[1], point[0])
    phi = math.asin(point[2])

    # Retrieve longitude, latitude
    longitude = theta / math.pi * 180.0
    latitude = phi / math.pi * 180.0

    geo_x_px = (longitude + 180) * geo_w / 360.0
    geo_y_px = (latitude + 90) * geo_h / 360.0

    return [geo_x_px, geo_y_px]


projPoint = transform_to_equirectangular(hitpoint, 3840, 1080)
print("project point: ", projPoint)
im = plt.imread('out.png')
implot = plt.imshow(im)
plt.scatter([projPoint[0]], [projPoint[1]], s=40)

plt.show()






























