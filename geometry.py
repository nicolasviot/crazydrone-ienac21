import math as m


class Point(object):
    """Meters coordinates, with attributes x, y: int"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({0.x}, {0.y})".format(self)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __rmul__(self, k):
        return Point(k * self.x, k * self.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def scale_line(self, angle, length):
        """Return the point reach by the line with its angle and length"""
        if 0 <= angle <= 90:
            x, y = self.x + length*m.sin((angle*m.pi)/180)*100, self.y - length*m.cos((angle*m.pi)/180)*100
        elif 90 < angle <= 180:
            x, y = self.x + length*m.sin(angle*m.pi/180)*100, self.y - length*m.cos(angle*m.pi/180)*100
        elif 0 > angle >= -90:
            x, y = self.x + length*m.cos(((90-angle)*m.pi)/180)*100, self.y - length*m.sin(((90-angle)*m.pi)/180)*100
        elif -90 > angle >= -180:
            x, y = self.x + length*m.cos((90-angle)*m.pi/180)*100, self.y - length*m.sin((90-angle)*m.pi/180)*100
        else:
            print("Angle error : Angle is not between -180 and 180 degrees")
            return None
        return Point(x, y)
