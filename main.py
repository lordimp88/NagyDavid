import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPointF, pyqtSlot
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QAction, QFileDialog, QGraphicsTextItem, QDialog, \
    QMessageBox, QInputDialog
import random
import EntityPoint
import numpy as np

import groups as gr
import UnionFindA
from annotation import Annotation
from approximation_dialog import Approximation
from contractdict import ContractDict2
import pandas as pd

import main_window
import scene
import representant as rep
import define_similarity



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
        self.attribute_intervals = []

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

        openFile = QAction('&Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)


        setAnnotation = QAction('&Set Annotation', self)
        setAnnotation.setShortcut('Ctrl+N')
        setAnnotation.setStatusTip('Set Annotation')
        setAnnotation.triggered.connect(self.set_annotation)

        defineSimilarity = QAction('&Define Similarity', self)
        defineSimilarity.setShortcut('Ctrl+M')
        defineSimilarity.setStatusTip('Define Similarity')
        defineSimilarity.triggered.connect(self.define_simmilarity_dialog)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openFile)

        fileMenu.addAction(setAnnotation)
        fileMenu.addAction(defineSimilarity)

        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(20, 360, 951, 251))
        self.table.setObjectName("table")

        self.buttonGroup.buttonClicked.connect(lambda btn: self.points_canvas.scene.setOption(btn.text()))

    # -------------------------------------------------------------------------------------------------------------------
    def file_open(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        self.points_type = 1

        x = int(self.x_range.toPlainText())
        y = int(self.y_range.toPlainText())

        df = pd.read_csv(name, header=0)
        df = df.replace('NaN', np.NaN)

        num, ok = QInputDialog.getInt(self, "Index of the decision attribute in the Information System",
                                      "The index of the decision attribue:")
        if ok:
            dec_attr_index = num

        dec_attr_list = df[df.columns[dec_attr_index]].tolist()

        # csak az azokat az oszlopokat hagyja meg, amik nem az osztályozást adják meg
        df.drop(df.columns[dec_attr_index], axis=1, inplace=True)

        msg = "Would you like to normalize the data?"
        reply = QMessageBox.question(self, 'Message', msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for i in range(len(df.columns)):
                max = df[df.columns[i]].dropna().max()
                min = df[df.columns[i]].dropna().min()
                df[df.columns[i]] = df[df.columns[i]].apply(lambda x: (x - min) / (max - min))
        else:
            pass

        # normalizálás után hozzáadjuk a decision_attribute oszlopot is a dataframe-hez és a fejlécekhez is
        self.headers = list(df.columns.values)
        self.headers.append("Class")
        se = pd.Series(dec_attr_list)
        df['Class'] = se.values

        # csere az első és utolsó (decision attribute). Így a decision attribute mindig az első helyen fog állni
        c = df.columns
        last = len(c) - 1
        df[[c[0], c[last]]] = df[[c[last], c[0]]]
        self.headers[0], self.headers[last] = self.headers[last], self.headers[0]

        # rendezzük osztályozó attribútum szerint, hogy később könnyebb legyen kiválasztani a közelítendő halmazok elemeit
        df = df.sort_values(by=df.columns[0])
        dec_attr_list = df[df.columns[dec_attr_index]].tolist()

        self.border_points_of_decision_attribute_values = [0]
        for i in range(len(dec_attr_list) - 1):
            if dec_attr_list[i] != dec_attr_list[i + 1]:
                self.border_points_of_decision_attribute_values.append(i + 1)
        self.border_points_of_decision_attribute_values.append(len(dec_attr_list))

        self.number_of_decision_attribute_values = len(set(dec_attr_list))
        print("Kul ertekek: ", self.number_of_decision_attribute_values)
        print("Hatarok: ", self.border_points_of_decision_attribute_values)

        for i in range(0, len(df.values)):
            r1 = random.randint(0, x + 1)
            r2 = random.randint(0, y + 1)
            entity = EntityPoint.EntityPoint(r1, r2, self.count, df.values[i])

            # if  "nan" in df.values[i]:
            #     entity.has_missing = True

            entity.setPos(r1, r2)
            self.count += 1
            self.points_canvas.scene.addItem(entity)
            text = QGraphicsTextItem(str(self.count - 1))
            text.setPos(r1 + 2, r2 - 2)
            self.points_canvas.scene.addItem(text)

        self.fill_table(self.headers)

        # self.find_thresholds(wine, 13, (data.manhattan, data.manhattan), 15, 16)

    # -------------------------------------------------------------------------------------------------------------------
    def fill_table(self, headers):
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(self.count)

        for i, e in enumerate(headers):
            item = QtWidgets.QTableWidgetItem()
            item.setText(e)
            self.table.setHorizontalHeaderItem(i, item)

        for i, e in enumerate(self.points_canvas.scene.getPointsList()):
            for j in range(len(headers)):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(e.attributes[j]))
                self.table.setItem(i, j, item)

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


    def define_simmilarity_dialog(self):
        dialog = define_similarity.DefineSimilarity(self.headers)
        if dialog.exec_() == QDialog.Accepted:
            self.attribute_intervals = dialog.intervals
            print("intervallumok: ",self.attribute_intervals)
        else:
            print('Cancelled')
        dialog.deleteLater()


    def too_high_difference(self,i,j):
           if self.points_type == 1:
               for k in range(1,len(self.attribute_intervals)):
                   if abs(self.points_list[i].attributes[k]-self.points_list[j].attributes[k]) >= self.attribute_intervals[k]:
                       return True
           return False

    def define_simmilarity_rel(self):
        simm = float(self.similarity_threshold.toPlainText())
        diff = float(self.difference_threshold.toPlainText())
        self.points_list = self.points_canvas.scene.getPointsList()
        num_of_points = len(self.points_list)
        relation = np.zeros((num_of_points,num_of_points))

        for i in range(num_of_points):
            for j in range(i+1,num_of_points):
                d = self.points_list[i].distance(self.points_list[j],self.points_type)
                if d > diff or np.isnan(d) or self.too_high_difference(i, j):
                    relation[i][j] = -1
                    relation[j][i] = -1
                elif d <= simm:
                    relation[i][j] = 1
                    relation[j][i] = 1
                else:
                    relation[i][j] = 0
                    relation[j][i] = 0

        print(relation)
        return relation



    def run(self):
        print("Points")
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
