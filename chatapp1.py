import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
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


app = QApplication([])
app.aboutToQuit.connect(exit_handler)
text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.NoFocus)
message_input = QLineEdit()
message_input.setMaxLength(1000)  # max character length of a chat message
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
