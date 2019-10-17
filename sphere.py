

from sphere_to_cubemap.geom3 import Vector3, Point3, Ray3, dot, unit
from math import sqrt
from sphere_to_cubemap.hit import Hit

class Sphere(object):
    """A ray-traceable sphere"""
    
    def __init__(self, centre, radius, material):
        """Create a sphere with a given centre point, radius
        and surface material"""
        self.centre = centre
        self.radius = radius
        self.material = material


    def normal(self, p):
        """The surface normal at the given point on the sphere"""
        return unit(p - self.centre)

    def intersect(self, ray):
        """The ray t value of the first intersection point of the
        ray with self, or None if no intersection occurs"""
        hit = None
        q = self.centre - ray.start
        vDotQ = dot(ray.dir, q)
        squareDiffs = dot(q, q) - self.radius * self.radius
        discrim = vDotQ * vDotQ - squareDiffs
        if discrim >= 0:
            root = sqrt(discrim)
            t0 = (vDotQ - root)
            t1 = (vDotQ + root)
            if t0 < t1:
                
                result = t1
            else:
                
                result = t0
            
            x = ray.start.x + ray.dir.dx * result
            y = ray.start.y + ray.dir.dy * result
            z = ray.start.z + ray.dir.dz * result

        return [x, y, z]



