from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

preview_class = uic.loadUiType("Ui/preview.ui")[0]
class Preview(QtWidgets.QDialog, preview_class):
    def __init__(self, file_path, show_preview_action):
        super().__init__()
        self.setupUi(self)
        self.show_preview_action = show_preview_action
        pixmap = QPixmap(file_path)
        w = pixmap.width()
        h = pixmap.height()
        self.label.setPixmap(pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.label_2.setText(f"{w}x{h}")
        self.show_preview_action.triggered.connect(self.handle_show_preview_action)
        self.move(0,0)
        self.rejected.connect(self.close_preview_window)

    def handle_show_preview_action(self, checked):
        if not checked:
            self.close()

    def set_image(self, file_path):
        pixmap = QPixmap(file_path)
        w = pixmap.width()
        h = pixmap.height()
        self.label.setPixmap(pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.label_2.setText(f"{w}x{h}")

    def close_preview_window(self):
        self.show_preview_action.setChecked(False)
