# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(973, 758)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.generateButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateButton.setGeometry(QtCore.QRect(10, 260, 75, 23))
        self.generateButton.setObjectName("generateButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 21, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 47, 21))
        self.label_2.setObjectName("label_2")
        self.x_range = QtWidgets.QTextEdit(self.centralwidget)
        self.x_range.setGeometry(QtCore.QRect(50, 10, 51, 31))
        self.x_range.setObjectName("x_range")
        self.y_range = QtWidgets.QTextEdit(self.centralwidget)
        self.y_range.setGeometry(QtCore.QRect(50, 50, 51, 31))
        self.y_range.setObjectName("y_range")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 141, 21))
        self.label_3.setObjectName("label_3")
        self.number_of_points = QtWidgets.QTextEdit(self.centralwidget)
        self.number_of_points.setGeometry(QtCore.QRect(160, 100, 51, 31))
        self.number_of_points.setObjectName("number_of_points")
        self.points_canvas = QtWidgets.QGraphicsView(self.centralwidget)
        self.points_canvas.setGeometry(QtCore.QRect(260, 50, 631, 301))
        self.points_canvas.setObjectName("points_canvas")
        self.selectButton = QtWidgets.QRadioButton(self.centralwidget)
        self.selectButton.setGeometry(QtCore.QRect(20, 140, 82, 17))
        self.selectButton.setObjectName("selectButton")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.selectButton)
        self.ChooseButton = QtWidgets.QRadioButton(self.centralwidget)
        self.ChooseButton.setGeometry(QtCore.QRect(20, 170, 161, 17))
        self.ChooseButton.setObjectName("ChooseButton")
        self.buttonGroup.addButton(self.ChooseButton)
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(10, 230, 75, 23))
        self.runButton.setObjectName("runButton")
        self.approximateButton = QtWidgets.QPushButton(self.centralwidget)
        self.approximateButton.setGeometry(QtCore.QRect(130, 230, 75, 23))
        self.approximateButton.setObjectName("approximateButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(120, 20, 71, 21))
        self.label_4.setObjectName("label_4")
        self.similarity_threshold = QtWidgets.QTextEdit(self.centralwidget)
        self.similarity_threshold.setGeometry(QtCore.QRect(200, 10, 51, 31))
        self.similarity_threshold.setObjectName("similarity_threshold")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(120, 60, 81, 21))
        self.label_5.setObjectName("label_5")
        self.difference_threshold = QtWidgets.QTextEdit(self.centralwidget)
        self.difference_threshold.setGeometry(QtCore.QRect(200, 50, 51, 31))
        self.difference_threshold.setObjectName("difference_threshold")
        self.GenerateRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.GenerateRadioButton.setGeometry(QtCore.QRect(20, 200, 81, 21))
        self.GenerateRadioButton.setObjectName("GenerateRadioButton")
        self.buttonGroup.addButton(self.GenerateRadioButton)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(260, 10, 633, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.printOriginalPointsButton = QtWidgets.QPushButton(self.widget)
        self.printOriginalPointsButton.setObjectName("printOriginalPointsButton")
        self.horizontalLayout.addWidget(self.printOriginalPointsButton)
        self.printClustersButton = QtWidgets.QPushButton(self.widget)
        self.printClustersButton.setObjectName("printClustersButton")
        self.horizontalLayout.addWidget(self.printClustersButton)
        self.printClustersButtonAnnotation = QtWidgets.QPushButton(self.widget)
        self.printClustersButtonAnnotation.setObjectName("printClustersButtonAnnotation")
        self.horizontalLayout.addWidget(self.printClustersButtonAnnotation)
        self.printApproximationButton = QtWidgets.QPushButton(self.widget)
        self.printApproximationButton.setObjectName("printApproximationButton")
        self.horizontalLayout.addWidget(self.printApproximationButton)
        self.printApproximationButtonAnnotations = QtWidgets.QPushButton(self.widget)
        self.printApproximationButtonAnnotations.setObjectName("printApproximationButtonAnnotations")
        self.horizontalLayout.addWidget(self.printApproximationButtonAnnotations)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 973, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.generateButton.setText(_translate("MainWindow", "Generate"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">X:</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Y:</span></p></body></html>"))
        self.x_range.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">200</p></body></html>"))
        self.y_range.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">200</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Number of points:</span></p></body></html>"))
        self.selectButton.setText(_translate("MainWindow", "Select"))
        self.ChooseButton.setText(_translate("MainWindow", "Choose to be approximated"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.approximateButton.setText(_translate("MainWindow", "Approximate"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Similarity</span></p><p><span style=\" font-size:12pt;\">:</span></p></body></html>"))
        self.similarity_threshold.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">50</p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Difference:</span></p></body></html>"))
        self.difference_threshold.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">80</p></body></html>"))
        self.GenerateRadioButton.setText(_translate("MainWindow", "Generate"))
        self.printOriginalPointsButton.setText(_translate("MainWindow", "Points"))
        self.printClustersButton.setText(_translate("MainWindow", "Base Sets without Annotations"))
        self.printClustersButtonAnnotation.setText(_translate("MainWindow", "Base Sets with Annotations"))
        self.printApproximationButton.setText(_translate("MainWindow", "Approximation"))
        self.printApproximationButtonAnnotations.setText(_translate("MainWindow", "Approximation with Annotations"))

