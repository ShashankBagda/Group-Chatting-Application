# Form implementation generated from reading ui file 'd:\GitHub\PWP-Project\untitled.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("d:\\GitHub\\PWP-Project\\1.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.text_area = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.text_area.setGeometry(QtCore.QRect(10, 159, 780, 321))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.text_area.setFont(font)
        self.text_area.setTabChangesFocus(False)
        self.text_area.setReadOnly(True)
        self.text_area.setBackgroundVisible(False)
        self.text_area.setCenterOnScroll(False)
        self.text_area.setObjectName("text_area")
        self.message_input = QtWidgets.QLineEdit(self.centralwidget)
        self.message_input.setGeometry(QtCore.QRect(10, 490, 780, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.message_input.setFont(font)
        self.message_input.setText("")
        self.message_input.setObjectName("message_input")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(False)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Project"))