import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsItem
from PyQt5.uic.properties import QtWidgets, QtCore

import EntityPoint
import approximation_abstract
import scene


class Approximation(QDialog, approximation_abstract.Ui_Dialog):

    def __init__(self,points,set,lower,upper,appr_type):
        super(Approximation, self).__init__()
        self.setupUi(self)

        self.points = points
        self.set = set
        self.lower = lower
        self.upper = upper
        self.appr_type = appr_type
        self.points_canvas.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.points_canvas.scene = QGraphicsScene()
        self.points_canvas.setScene(self.points_canvas.scene)

        self.printLowerButton.clicked.connect(self.printLowerApproximation)
        self.printUpperButton.clicked.connect(self.printUpperApproximation)
        self.printSetButton.clicked.connect(self.printSet)
        self.okButton.clicked.connect(self.accept)

        for item in self.points:
            if isinstance(item, EntityPoint.EntityPoint):
                e = EntityPoint.EntityPoint(item.x,item.y,item.id,item.attributes)
                e.setPos(e.x, e.y)
                self.points_canvas.scene.addItem(e)

        if self.appr_type == 0:
            self.writeLowerApproximationFile('lower_approximation_clustering.txt')
            self.writeUpperApproximationFile('upper_approximation_clustering.txt')
            self.writeSetFile('set_to_be_approximated_clustering.txt')
        elif self.appr_type == 1:
            self.writeLowerApproximationFile('lower_approximation_clustering_annotation.txt')
            self.writeUpperApproximationFile('upper_approximation_clustering_annotation.txt')
            self.writeSetFile('set_to_be_approximated_clustering.txt_annotation')



    def writeLowerApproximationFile(self,fname):
        file = open(fname, 'w')
        points_set = set([item for item in self.points if isinstance(item, EntityPoint.EntityPoint) ])
        lower_list = []
        for b in self.lower:
            lower_list += list(b)
        lower_set = set(lower_list)
        lower_complementer = points_set.difference(lower_set)

        for e in list(lower_complementer):
            s = str(e.x)+" "+str(e.y)+" "+str(3)+'\n'
            file.write(s)

        for e in list(lower_set):
            s = str(e.x) + " " + str(e.y) + " " + str(0)+'\n'
            file.write(s)

        file.close()

    def writeUpperApproximationFile(self,fname):
        file = open(fname, 'w')
        points_set = set([item for item in self.points if isinstance(item, EntityPoint.EntityPoint)])
        upper_list = []
        for b in self.upper:
            upper_list += list(b)
        upper_set = set(upper_list)
        uppper_complementer = points_set.difference(upper_set)

        for e in list(uppper_complementer):
            s = str(e.x) + " " + str(e.y) + " " + str(3) + '\n'
            file.write(s)

        for e in list(upper_set):
            s = str(e.x) + " " + str(e.y) + " " + str(0) + '\n'
            file.write(s)

        file.close()


    def writeSetFile(self,fname):
        file = open(fname, 'w')

        points_set = set([item for item in self.points if isinstance(item, EntityPoint.EntityPoint) ])
        set_complementer = points_set.difference(self.set)

        for e in list(set_complementer):
            s = str(e.x)+" "+str(e.y)+" "+str(3)+'\n'
            file.write(s)

        for e in list(self.set):
            s = str(e.x) + " " + str(e.y) + " " + str(0)+'\n'
            file.write(s)

        file.close()


    def printLowerApproximation(self):

        for item in self.points_canvas.scene.items():
            if isinstance(item, EntityPoint.EntityPoint):
                item.setBrush(Qt.black)
        base_sets = [list(c) for c in self.lower]

        for i in range (len(base_sets)):
            for element in base_sets[i]:
                for item in self.points_canvas.scene.items():
                    if isinstance(item, EntityPoint.EntityPoint):
                        if element.id == item.id:
                            item.setBrush(Qt.red)

        #self.writeLowerApproximationFile()


    def printUpperApproximation(self):

        for item in self.points_canvas.scene.items():
            if isinstance(item, EntityPoint.EntityPoint):
                item.setBrush(Qt.black)
        base_sets = [list(c) for c in self.upper]
        for c in base_sets:
            for element in c:
                for item in self.points_canvas.scene.items():
                    if isinstance(item, EntityPoint.EntityPoint):
                        if element.id == item.id:
                            item.setBrush(Qt.blue)


    def printSet(self):

        for item in self.points_canvas.scene.items():
            if isinstance(item, EntityPoint.EntityPoint):
                item.setBrush(Qt.black)
        base_sets = list(self.set)
        for element in base_sets:
            for item in self.points_canvas.scene.items():
                if isinstance(item, EntityPoint.EntityPoint):
                    if element.id == item.id:
                        item.setBrush(Qt.green)



#app = QApplication(sys.argv)
#dialog = Approximation()
#dialog.show()
#app.exec_()
