import numpy as np

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