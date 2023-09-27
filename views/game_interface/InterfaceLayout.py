from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QFrame

from controls.python.StylesheetLoader import StylesheetLoader
from views.game_interface.InterfaceExitButton import InterfaceExitButton


class InterfaceLayout(QFrame):
    def __init__(self,  parent=None):
        super().__init__(parent)

        StylesheetLoader(self).load_stylesheet("resources/styles/game.qss")

        self.setObjectName("interfaceLayout")
        self.setFixedSize(640, 100)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.interface_exit_button = InterfaceExitButton("")
        self.interface_layout_frame = QFrame()
        self.interface_layout_frame.setObjectName("interfaceLayoutFrame")
        self.interface_layout_frame.setFixedSize(590, 100)
        self.layout.addWidget(self.interface_exit_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.interface_layout_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
