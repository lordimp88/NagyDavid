import sys
import math

import EntityPoint


class Entity():
    def __init__(self, x, y, id, attributes = None):
        self.x=x
        self.y=y
        self.id = id
        self.attributes = attributes
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.r1 = 0
        self.r2 = 0


    def __str__(self):
        if self.attributes is None:
            return "({},{}) id: {}".format(self.x, self.y, self.id)
        else:
            return "({},{}) id: {} attributes: {}".format(self.x, self.y, self.id, self.attributes)


    def distance(self, other, type):
        #type = 0 -> random point
        #type  = 1 -> random color
        if type == 0:
            return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
        elif type == 1:
            s = 0
            for i in range(0,len(self.attributes)):
                s += (self.attributes[i]-other.attributes[i])**2
            return s**0.5

    def __str__(self):
        if self.attributes is None:
            return "({},{}) id: {}".format(self.x, self.y, self.id)
        else:
            return "({},{}) id: {} attributes: {}".format(self.x, self.y, self.id, self.attributes)

    def __hash__(self):
        return self.id

    def __eq__(self, other):

        if isinstance(other,self.__class__) and other.id == self.id:
            return True
        if isinstance(other,EntityPoint.EntityPoint) and other.id == self.id:
            return True
        return False


    def __ne__(self, other):
        return not self.__eq__(other)
