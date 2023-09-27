from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QFrame

from controls.python.StylesheetLoader import StylesheetLoader
from widgets.Color import Color
from widgets.MenuButton import MenuButton


class InterfaceGame(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.color = Color("red")
        self.layout.addWidget(self.color)

        self.setLayout(self.layout)
