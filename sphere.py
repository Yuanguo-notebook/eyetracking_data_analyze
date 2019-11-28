

from geom3 import dot
from math import sqrt


class Sphere(object):

    
    def __init__(self, centre, radius):

        self.centre = centre
        self.radius = radius

    def intersect(self, ray):

        l = self.centre - ray.start # C-O
        tca = dot(ray.dir, l) # tca

        discrim = tca * tca - dot(l, l) + self.radius * self.radius
        if discrim >= 0:
            thc = sqrt(discrim)
            t0 = (tca - thc)
            t1 = (tca + thc)
            # we want the point in the positive direction
            if t0 < t1:

                result = t1
            else:

                result = t0

            x = ray.start.x + ray.dir.dx * result
            y = ray.start.y + ray.dir.dy * result
            z = ray.start.z + ray.dir.dz * result
        else:
            x = 0
            y = 0
            z = 0
        return [x, y, z]



