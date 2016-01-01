from PyQt4.QtGui import *
from PyQt4.QtCore import *

import socket

import main_ui
import console

from libs.modechat import get

class mainPopup(QWidget, main_ui.Ui_Form):

    def __init__(self, args):
        QWidget.__init__(self)
        self.setupUi(self)

        self.sock = args['sock']
        self.socket = args['socket']
        self.ipAddress = args['ipAddress']
        self.icon = args['icon']

        self.setWindowTitle('Connected to - %s - Socket #%s' % (self.ipAddress, self.socket))
        self.setWindowIcon(QIcon(self.icon))

        self.console = console.Console()
        self.gridLayout.addWidget(self.console)

        self.connect(self.console, SIGNAL("returnPressed"), self.runCommand)

    # run shell command
    def runCommand(self):
        try:
            command = self.console.command[1:] if self.console.command.startswith(' ') else self.console.command
            data = get(self.sock, command, mode='mshell')
            data = data.replace('\n', '<br>')

            self.console.append('<br><font color=#3CFFFF>'+data+'</font>')
            self.console.newPrompt()

        except socket.error, socket.timeout:
            # Error with connection
            self.close()
