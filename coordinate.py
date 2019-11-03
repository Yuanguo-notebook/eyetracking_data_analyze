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
from PIL import Image

# set 3d environment for plotting
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# map equirectangular image to sphere
# adopted from https://stackoverflow.com/questions/53074908/map-an-image-onto-a-sphere-and-plot-3d-trajectories
def mpl_sphere(image_file):
    img = plt.imread(image_file)

    # define a grid matching the map size, subsample along with pixels
    # evenly create img.shape[0 number of points between 0  and pi
    theta = np.linspace(0, np.pi, img.shape[0])
    phi = np.linspace(0, 2*np.pi, img.shape[1])



    count = 45 # keep 45 points along theta and phi
    # get index evenly for 45 points
    theta_inds = np.linspace(0, img.shape[0] - 1, count).round().astype(int)
    phi_inds = np.linspace(0, img.shape[1] - 1, count).round().astype(int)

    # get value for 45 points
    theta = theta[theta_inds]
    phi = phi[phi_inds]

    # recreate image
    img = img[np.ix_(theta_inds, phi_inds)]
    # image = Image.fromarray(img, 'RGB')
    # image.show()


    theta,phi = np.meshgrid(theta, phi)

    R = 1


    # sphere to xyz
    x = R * np.sin(theta) * np.cos(phi)
    y = R * np.sin(theta) * np.sin(phi)
    z = R * np.cos(theta)


    print('30 30 theta: ',theta[30][30], ', phi: ', phi[30][30], ', xyz: ', x[30][30], y[30][30], z[30][30], ', xyz T: ', x.T[30][30], y.T[30][30], z.T[30][30])
    print('15 15 theta: ', theta[20][15], ', phi: ', phi[20][15], ', xyz: ', x[20][15], y[20][15], z[20][15], ', xyz T: ',
          x.T[20][15], y.T[20][15], z.T[20][15])

    ## ???? why T?
    ax.plot_surface(x.T, y.T, z.T, facecolors=img/255, cstride=1, rstride=1) # we've already pruned ourselves

    draw_point([x.T[30][30], y.T[30][30], z.T[30][30]])
    draw_point([x.T[20][15], y.T[20][15], z.T[20][15]])
    # make the plot more spherical
    ax.axis('scaled')
    # assert(False)
    return theta,phi

# draw a empty sphere
def draw_sphere(centre, radius):

    # draw sphere
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]

    sphere_x = centre[0] + radius * np.cos(u) * np.sin(v)
    sphere_y = centre[1] + radius * np.sin(u) * np.sin(v)
    sphere_z = centre[2] + radius * np.cos(v)
    ax.plot_wireframe(sphere_x, sphere_y, sphere_z, color="orange", alpha=.5)

# draw xyz axis with unit vector
def draw_axis():
    ax.plot([0, 1], [0, 0], [0, 0], color='r')  # x
    ax.plot([0, 0], [0, 1], [0, 0], color='g')  # y
    ax.plot([0, 0], [0, 0], [0, 1], color='b')  # z


def draw_point(vec):
        # draw a point
    ext = 4
    start = np.array([0.0,0.0,0.0])
    end2 = vec + (vec - start) / ext
    ax.scatter(end2[0], end2[1], end2[2], color="b", s=20)
    ax.scatter(vec[0], vec[2], vec[1], color='b', s=20)
    ax.plot([end2[0], vec[0]], [end2[1], vec[1]], [end2[2], vec[2]], color='b')


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
draw_sphere(center, 1)
draw_axis()
image_file = 'flipped_out.jpg'
theta,phi = mpl_sphere(image_file)

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
def get_hit_point_draw(start, rot, combined_ray, linecolor):


    # rotate a vector by quaternion rotation
    dir = rotate_vec_by_quaternion(rot, combined_ray)
    end = start + dir

    # print('start: ', start, 'dir', dir, 'end: ', end)
    #get hitting point
    sphere = Sphere(Point3(0,0,0), 1, None)
    ray = Ray3(Point3(start[0], start[1], start[2]), Vector3(dir[0], dir[1], dir[2]))
    hitpoint = sphere.intersect(ray)

    #check if hitting point is on sphere surface
    check_point_on_sphere(0, 0, 0, hitpoint, 1)

    # convert unity coordinate to python coordinate
    unity_to_python_point(start)
    unity_to_python_point(end)
    unity_to_python_point(hitpoint)

    # plotting vector
    ax.scatter(start[0], start[1], start[2], color="purple", s=10)
    ax.scatter(end[0], end[1], end[2], color="g", s=10)
    ax.scatter(hitpoint[0], hitpoint[1], hitpoint[2], color="r", s=20)
    ext = 4
    end2 = end + (end-start) / ext
    ax.scatter(end2[0], end2[1], end2[2], color="g", s=10)
    ax.plot([end2[0], end[0]], [end2[1], end[1]], [end2[2], end[2]], color=linecolor)

    ax.plot([start[0] , end[0]], [start[1],end[1]], [start[2],end[2]], color=linecolor)
    return hitpoint

# No rotation police car
# -0.3,0.3,0.6  0.0,1.0,0.0,0.1  0.3,0.0,-1.0
#
# Wheel
# -0.2,0.3,0.6  0.1,0.8,-0.1,0.5   0.9,-0.3,-0.4
# steering wheel:
start = np.array([0.0,0.0,0.0])

# rot = np.array([0.0, 0.7, 0, 0.7])
# original rotation of camera 90 on y(unity), we need to rotate another 90 degree,
rot = np.array([0.0, 1.0, 0, 0.0])
combined_ray = np.array([0.88023610, -0.29249220, -0.37367440])
hitpoint_wheel =get_hit_point_draw(start, rot, combined_ray, 'g')

# police car
start_car = np.array([0.0,0.0,0.0])
rot_car = np.array([0.0, 1.0, 0, 0.0])
combined_ray_car = np.array([0.27734380, -0.00733450, -0.96074280])

hitpoint_cal = get_hit_point_draw(start_car, rot_car, combined_ray_car, 'r')



plt.show()


# transforms a point on sphere to a point in equirectangular
# geo_w, geo_h are final projection width and length



def transform_to_equirectangular(point, geo_w, geo_h, color):

    # from -pi to pi, so need to add 2pi if it is negative
    phi_value = math.atan2(point[1], point[0])
    theta_value = math.acos(point[2])
    if phi_value <0 :
        phi_value += 2*np.pi
    # print('theta: ', theta, 'phi: ', phi)

    # get index of current theta value
    theta_index = int(45 * (theta_value / np.pi))
    phi_index = int(45 * (phi_value / (2 * np.pi)))
    # print(theta[0][theta_index])
    # print(phi[phi_index][0])

    # get the transpose value for theta and phi
    theta_value2 = theta[0][int(phi_index)]
    phi_value2 = phi[theta_index][0]

    # project back to equirectangular
    geo_x_px = ( theta_value2 / np.pi )* geo_w
    geo_y_px = (phi_value2 / (2*np.pi)) * geo_h

    # print('x: ', geo_x_px, 'y: ', geo_y_px)
    plt.scatter([geo_x_px], [geo_y_px], s=40, color=color)
    return [geo_x_px, geo_y_px]

im = plt.imread('flipped_out.jpg')
implot = plt.imshow(im)
projPoint_w = transform_to_equirectangular(hitpoint_wheel, 3840, 1080, 'g')
projPoint_c = transform_to_equirectangular(hitpoint_cal, 3840, 1080, 'r')
# o1 = transform_to_equirectangular([ -0.34795935955178103, -0.7656758639930804, -0.540984986296999], 3840, 1080, 'b')
# o2 = transform_to_equirectangular([ -0.8415633601907285, 0.24952675995369641, 0.47906941757066945], 3840, 1080, 'k')

# o1 = transform_to_equirectangular([ -0.34795935955178103, -0.7656758639930804, -0.540984986296999], 3840, 1080, 'b')
# o2 = transform_to_equirectangular([-0.5353761780076146, 0.8323126199294079, 0.14362468704301562], 3840, 1080, 'orange')

plt.show()



























