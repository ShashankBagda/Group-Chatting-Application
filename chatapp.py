import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
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


class UI(QMainWindow):
    window = QMainWindow

    def exit_handler():
        os._exit(1)

    def __init__(self):
        super(UI, self).__init__()

        # Load ui file
        uic.loadUi("untitled.ui", self)

        # Define widgets
        self.label = self.findChild(QLabel, "label")
        self.text_area = self.findChild(QPlainTextEdit, "text_area")
        self.message_input = self.findChild(QLineEdit, "message_input")
        # self.layout = self.findChild(QVBoxLayout, "message_input")
        # self.layout.addWidget(text_area)
        # self.layout.addWidget(message_input)
        #self.text_area = self.findChild(QPlainTextEdit, "text_area")

        # Working
        self.text_area.setFocusPolicy(Qt.NoFocus)
        # max character length of a chat message
        self.message_input.setMaxLength(1000)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Username Input
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    window.name, okPressed = QInputDialog.getText(
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
                UI.text_area.appendPlainText(msg)

    def send_message():
        pubnub_publish(
            # {"message": self.message_input.text()})
            {"name": UI.name, "message": UI.message_input.text()})
        UI.message_input.clear()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Qt Signals
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    window.message_input.returnPressed.connect(send_message)
    timer = QTimer()
    timer.timeout.connect(display_new_messages)
    timer.start(1000)

    # show
    window.show()


# Initialize the app
app = QApplication([])
#app = QApplication(sys.argv)
app.aboutToQuit.connect(UI.exit_handler)
app.window = QMainWindow
UI()
app.exec_()
