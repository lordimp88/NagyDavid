import sys
import math

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem

import Entity


class EntityPoint(QGraphicsItem):
    def __init__(self, x, y, id, attributes = None):
        super(EntityPoint, self).__init__()
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.rectF = QRectF(0, 0, 4, 4)
        self.x=x
        self.y=y
        self.id = id
        self.attributes = attributes
        self.brush = QBrush(Qt.black)
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.r1 = 0
        self.r2 = 0


    def setBrush(self, brush):
        self.brush = brush
        self.update()

    def boundingRect(self):
        return self.rectF

    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.rectF, self.brush)

    #def paint2(self, painter=None, style=None, widget=None):
    #    painter.fillRect(self.rectF, Qt.red)

    def __str__(self):
        if self.attributes is None:
            return "({},{}) id: {}".format(self.x, self.y, self.id)
        else:
            return "({},{}) id: {} attributes: {}".format(self.x, self.y, self.id, self.attributes)


    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))


    def __hash__(self):
        return self.id

    def __eq__(self, other):

        if isinstance(other,self.__class__) and other.id == self.id:
            return True
        if isinstance(other,Entity.Entity) and other.id == self.id:
            return True
        return False


    def __ne__(self, other):
        return not self.__eq__(other)