from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import  QAction, QGraphicsTextItem, QDialog
import random
import EntityPoint
import numpy as np
import groups as gr
import UnionFindA
from annotation import Annotation
from approximation_dialog import Approximation
from contractdict import ContractDict2

import main_window
import scene
import representant as rep



class MainMenu(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    count = 0

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.setupUi(self)

        self.generateButton.clicked.connect(self.generate)
        self.approximateButton.clicked.connect(self.approximate)
        self.runButton.clicked.connect(self.run)
        self.printOriginalPointsButton.clicked.connect(self.printOriginalPoints)
        self.printClustersButton.clicked.connect(self.colorClustersClustering)
        self.printApproximationButton.clicked.connect(self.printApproximation)
        self.printApproximationButtonAnnotations.clicked.connect(self.printApproximationAnnotation)

        self.points_canvas.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.points_canvas.scene = scene.PointsGraphicsScene()
        self.points_canvas.setScene(self.points_canvas.scene)

        self.points_type = 0
        self.points_list = []
        self.clusters = []
        self.colors = []
        self.attributes = []

        self.set_to_be_approximated = set()

        self.base_sets_covering = []
        self.lower_approximaton_covering = []
        self.upper_approximaton_covering = []

        self.base_sets_covering_disjoint = []
        self.lower_approximaton_covering_disjoint = []
        self.upper_approximaton_covering_disjoint = []

        self.singletons = []
        self.representants = []
        self.base_sets_clustering = []
        self.lower_approximaton_clustering = []
        self.upper_approximaton_clustering = []

        self.base_sets_clustering_annotation = []
        self.lower_approximaton_clustering_annotation = []
        self.upper_approximaton_clustering_annotation = []


        setAnnotation = QAction('&Set Annotation', self)
        setAnnotation.setShortcut('Ctrl+N')
        setAnnotation.setStatusTip('Set Annotation')
        setAnnotation.triggered.connect(self.set_annotation)


        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(setAnnotation)

        self.buttonGroup.buttonClicked.connect(lambda btn: self.points_canvas.scene.setOption(btn.text()))

  # -------------------------------------------------------------------------------------------------------------------
    def getClusters(self):
        size = len(self.best[0])
        clusters = [ [] for _ in range(size)  ]
        for i in range(size):
            j = self.best[0][i]
            clusters[j].append(self.points_list[i])

        return clusters


    def printOriginalPoints(self):

        if self.points_type == 0:
            for item in self.points_canvas.scene.items():
                if isinstance(item, EntityPoint.EntityPoint):
                    item.setBrush(Qt.black)
        elif self.points_type == 1:
            for item in self.points_canvas.scene.items():
                if isinstance(item, EntityPoint.EntityPoint):
                    item.setBrush(QColor(item.attributes[0],item.attributes[1],item.attributes[2]))

    def colorClustersClustering(self):
        self.colorClusters(self.base_sets_clustering)


    def printApproximation(self):
        dialog = Approximation(self.points_canvas.scene.items(), self.set_to_be_approximated.copy(),
                               self.lower_approximaton_clustering[::], self.upper_approximaton_clustering[::],0)
        if dialog.exec_() == QDialog.Accepted:
            print("Print Approximation with Annotation process")
        else:
            print('Cancelled')
        dialog.deleteLater()


    def printApproximationAnnotation(self):
        dialog = Approximation(self.points_canvas.scene.items(), self.set_to_be_approximated.copy(),
                               self.lower_approximaton_clustering_annotation[::], self.upper_approximaton_clustering_annotation[::],1)
        if dialog.exec_() == QDialog.Accepted:
            print("Print Approximation with Annotation process")
        else:
            print('Cancelled')
        dialog.deleteLater()


    def set_annotation(self):
        dialog = Annotation(self.singletons,self.base_sets_clustering_annotation,self.representants,self.points_type)
        if dialog.exec_() == QDialog.Accepted:
            self.base_sets_clustering_annotation = dialog.base_sets
            self.colorClusters(self.base_sets_clustering_annotation)
        else:
            print('Cancelled')
        dialog.deleteLater()

    def colorClusters(self, points):

        step = 400 / len(points) - 1
        for i in range(0, 400, int(step)):
            color = QColor.fromHsv(i, 255, 255)
            self.colors.append(color)

        for i, c in enumerate(points):
            for element in c:
                for item in self.points_canvas.scene.items():
                    if isinstance(item, EntityPoint.EntityPoint):
                        if element.id == item.id:
                            item.setBrush(self.colors[i])




    def printClusters(self):
        clusters_all = self.getClusters()
        self.clusters = [c for c in clusters_all if len(c) != 0]

        file = open("clusters.txt", 'w')

        for i in range(0,len(self.clusters)):
            if len(self.clusters[i])==1:
                s = str(self.clusters[i][0].x) + " " + str(self.clusters[i][0].y) + " " + str(1) + '\n'
                file.write(s)
            else:
                for e in self.clusters[i]:
                    s = str(e.x) + " " + str(e.y) + " " + str(i) + '\n'
                    file.write(s)
        file.close()

        self.representants = rep.getRepresentants(self.clusters,self.relation,2,2)

        self.getBaseSets()
        self.colorClusters(self.base_sets_clustering)




    def getBaseSets(self):
        self.singletons = [c for c in self.clusters if len(c) == 1]
        self.base_sets_clustering = [set(c) for c in self.clusters if len(c)>1]
        self.base_sets_clustering_annotation = [set(c) for c in self.clusters if len(c) > 1]
        print("Base sets using correlation clustering: ")
        for c in self.base_sets_clustering:
            print([str(item) for item in c])
            print()
        print("--------------------------")
        print("Singletons:")
        print([str(item[0]) for item in self.singletons])



    def generate(self):
        x = int(self.x_range.toPlainText())
        y = int(self.y_range.toPlainText())
        n = int(self.number_of_points.toPlainText())

        for i in range(0, n):
            r1 = random.randint(0, x + 1)
            r2 = random.randint(0, y + 1)

            if self.points_type == 0:
                entity = EntityPoint.EntityPoint(r1,r2,self.count)
            elif self.points_type == 1:
                red = random.randint(0, 256)
                green = random.randint(0, 256)
                blue = random.randint(0, 256)
                entity = EntityPoint.EntityPoint(r1, r2, self.count,[red,green,blue])

            entity.setPos(r1,r2)
            self.count+=1
            #self.points_canvas.scene.setCount(self.count)
            self.points_canvas.scene.addItem(entity)

            if self.points_type == 1:
                color = QColor.fromRgb(entity.attributes[0], entity.attributes[1], entity.attributes[2])
                entity.setBrush(color)

            text = QGraphicsTextItem(str(self.count-1))
            text.setPos(r1 + 2, r2 - 2)
            self.points_canvas.scene.addItem(text)


    #-------------------------------------------------------------------------------------------------------------------
    def approximate(self):
        self.set_to_be_approximated = self.points_canvas.scene.getSetToBeApproximated()
        print("The set to be approximated")
        print([item for item in self.set_to_be_approximated ])

        for bs in self.base_sets_clustering:

            if bs.issubset(self.set_to_be_approximated):
                self.lower_approximaton_clustering.append(bs)
            if  bool(bs.intersection(self.set_to_be_approximated)):
                self.upper_approximaton_clustering.append(bs)

        print("Lower approximation using correlation clustering: ")
        for bs in self.lower_approximaton_clustering:
            print([str(item) for item in bs])
            print()
        print("--------------------------")
        print("Upper approximation using correlation clustering: ")
        for bs in self.upper_approximaton_clustering:
            print([str(item) for item in bs])
            print()
        print("--------------------------")


        for bs in self.base_sets_clustering_annotation:

            if bs.issubset(self.set_to_be_approximated):
                self.lower_approximaton_clustering_annotation.append(bs)
            if  bool(bs.intersection(self.set_to_be_approximated)):
                self.upper_approximaton_clustering_annotation.append(bs)

        print("Lower approximation using correlation clustering with annotations: ")
        for bs in self.lower_approximaton_clustering_annotation:
            print([str(item) for item in bs])
            print()
        print("--------------------------")
        print("Upper approximation using correlation clustering with annotations: ")
        for bs in self.upper_approximaton_clustering_annotation:
            print([str(item) for item in bs])
            print()
        print("--------------------------")



    def define_simmilarity_rel(self):
        simm = int(self.similarity_threshold.toPlainText())
        diff = int(self.difference_threshold.toPlainText())

        self.points_canvas.scene.setSimilarity_threshold(simm)
        self.points_canvas.scene.setDifference_threshold(diff)

        self.points_list = self.points_canvas.scene.getPointsList()
        num_of_points = len(self.points_list)
        relation = np.zeros((num_of_points,num_of_points))

        for i in range(num_of_points):
            for j in range(i+1,num_of_points):
                d = self.points_list[i].distance(self.points_list[j],self.points_type)
                if d <= simm:
                    relation[i][j] = 1
                    relation[j][i] = 1
                elif d >= diff:
                    relation[i][j] = -1
                    relation[j][i] = -1
                else:
                    relation[i][j] = 0
                    relation[j][i] = 0

        np.savetxt('relation.txt', relation)
        r = np.loadtxt('relation.txt')

        return relation


    def run(self):

        print([str(e) for e in self.points_list])
        self.relation = self.define_simmilarity_rel()
        rows, columns = self.relation.shape

        graph = []

        for i in range(0,rows):
            for j in range(0,rows):
                graph.append((i,j,self.relation[i][j]))

        uf = UnionFindA.UnionFind(rows)
        c = ContractDict2(rows, graph)
        c.contract(uf, 0, rows)

        print(uf.array)
        print(gr.calculate(uf.array,self.relation,rows))
        self.best = (uf.array,10)
        self.printClusters()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = MainMenu()
    form.show()
    sys.exit(app.exec_())
