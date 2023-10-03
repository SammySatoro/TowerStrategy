from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton

from controls.python.StylesheetLoader import StylesheetLoader


class GameInterfaceButton(QPushButton):
    def __init__(self, text, icon_file: str = None, parent=None):
        super().__init__(text, parent)
        self.icon_file = icon_file
        self.setObjectName("gameInterfaceButton")
        self.setFixedSize(64, 64)
        if self.icon_file == None:
            StylesheetLoader(self).load_stylesheet("resources/styles/game.qss")
        else:
            self.set_icon(self.icon_file)
            self.pressed.connect(self.on_left_mouse_click)
            self.released.connect(self.on_left_mouse_release)

    def set_icon(self, icon_file: str):
        self.setIcon(QIcon(icon_file))
        self.setIconSize(QSize(self.size().width(), self.size().height()))

    def on_left_mouse_click(self):
        self.setIconSize(QSize(self.size().width() - 6, self.size().height() - 6))

    def on_left_mouse_release(self):
        self.setIconSize(QSize(self.size().width() + 6, self.size().height() + 6))

