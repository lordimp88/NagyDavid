import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPen, QBrush, QTransform
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem

import EntityPoint
import Entity

class PointsGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0, 0, 200, 200)
        self.opt = ""
        self.similarity_threshold=0
        self.difference_threshold=0
        self.count = 0
        self.set_to_be_approximated = set()

    def setSimilarity_threshold(self,x):
        self.similarity_threshold=x

    def setDifference_threshold(self,x):
        self.difference_threshold=x

    def setOption(self, opt):
        self.opt = opt

    def getPointsList(self):
        points_list = []
        for p in self.items():
            if isinstance(p, EntityPoint.EntityPoint):
                e = Entity.Entity(p.x,p.y,p.id,p.attributes)
                points_list.append(e)
        return points_list[::-1]


    def getSetToBeApproximated(self):
        return self.set_to_be_approximated


    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        if self.opt == "Generate":
            entity = EntityPoint.EntityPoint(x,y,self.count)
            self.count +=1
            entity.setPos(x, y)
            self.addItem(entity)
            text = QGraphicsTextItem(str(self.count - 1))
            text.setPos(x + 2, y - 2)
            self.addItem(text)

        elif self.opt == "Select":
            item = self.itemAt(event.scenePos(),QTransform())

            if isinstance(item, EntityPoint.EntityPoint):
                print(str(item))

            pen = QPen(QtCore.Qt.red)
            pen2 = QPen(QtCore.Qt.blue)
            circle_x = x - int(self.similarity_threshold)
            circle_y = y - int(self.similarity_threshold)
            self.addEllipse(circle_x, circle_y, int(self.similarity_threshold) * 2,
                                                int(self.similarity_threshold) * 2, pen)
            circle_x = x - int(self.difference_threshold)
            circle_y = y - int(self.difference_threshold)
            self.addEllipse(circle_x, circle_y, int(self.difference_threshold) * 2,
                                                int(self.difference_threshold) * 2, pen2)


        elif self.opt == "Choose to be approximated":
            for item in self.items():
                if isinstance(item, EntityPoint.EntityPoint):
                    d = ((x-item.x)**2+(y-item.y)**2)**0.5
                    if d < 5:
                        e = Entity.Entity(item.x, item.y, item.id, item.attributes)
                        self.set_to_be_approximated.add(e)
                        print(str(e), " added!")

