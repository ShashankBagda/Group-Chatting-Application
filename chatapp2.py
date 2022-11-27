import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from requests import Session
from threading import Thread
from time import sleep
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# PubNub Messaging Setup
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
channel = 'chat-channel'
pnconfig = PNConfiguration()

pnconfig.publish_key = 'pub-c-4c03cf9a-687e-46e7-b1ba-ab62e84bba78'
pnconfig.subscribe_key = 'sub-c-22fb1c63-ab41-4e2f-a9a2-5e20d62ce2c3'

pubnub = PubNub(pnconfig)
new_messages = []


def pubnub_publish(data):
    pubnub.publish().channel(channel).message(data).sync()


class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, pn_message):
        print('incoming_message', pn_message.message)
        new_messages.append(pn_message.message)


def format_message(message_body):
    return message_body.get('name') + ": " + message_body.get('message')


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(channel).execute()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# GUI Setup
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def exit_handler():
    os._exit(1)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("1.png"))
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
        self.text_area.setObjectName("plainTextEdit")
        self.text_area.setFocusPolicy(Qt.NoFocus)

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
        self.message_input.setObjectName("lineEdit")
        # max character length of a chat message
        self.message_input.setMaxLength(10000)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Project"))


app = QApplication([])
app.aboutToQuit.connect(exit_handler)

layout = QVBoxLayout()
layout.addWidget(text_area)
layout.addWidget(message_input)

window = QWidget()
window.setLayout(layout)
window.show()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Username Input
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
name, okPressed = QInputDialog.getText(
    window,
    "Username input",
    "Input your chat username",
    QLineEdit.Normal,
    ""
)

if okPressed and name != '' and len(name) < 20:
    print('Username:', name)
else:
    exit_handler()  # invalid username, exiting


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# UI Send/Receive Message Functions
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def display_new_messages():
    while new_messages:
        if len(new_messages) > 0:
            msg = new_messages.pop(0)
            msg = format_message(msg)
            text_area.appendPlainText(msg)


def send_message():
    pubnub_publish({"name": name, "message": message_input.text()})
    message_input.clear()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Qt Signals
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
message_input.returnPressed.connect(send_message)
timer = QTimer()
timer.timeout.connect(display_new_messages)
timer.start(1000)

sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
