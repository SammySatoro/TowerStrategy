from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton

class GameInterfaceButton(QPushButton):
    def __init__(self, text, icon_file: str = None, parent=None):
        super().__init__(text, parent)
        self.icon_file = icon_file
        self.setObjectName("gameInterfaceButton")
        # self.setStyleSheet(f"background-image: url({self.icon_file});")

        self.setIcon(QIcon(self.icon_file))
        self.setFixedSize(64, 64)
        self.setIconSize(QSize(self.size().width(), self.size().height()))
        self.pressed.connect(self.on_left_mouse_click)
        self.released.connect(self.on_left_mouse_release)

    def on_left_mouse_click(self):
        self.setIconSize(QSize(self.size().width() - 6, self.size().height() - 6))

    def on_left_mouse_release(self):
        self.setIconSize(QSize(self.size().width() + 6, self.size().height() + 6))

